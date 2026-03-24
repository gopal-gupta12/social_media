import streamlit as st
import requests
import json

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="FastAPI Feed", page_icon="📸", layout="centered")

def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
        
        /* Apply font globally */
        html, body, [class*="css"], .stMarkdown, .stText {
            font-family: 'Outfit', sans-serif !important;
        }

        /* Animated Title */
        h1 {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #FFE66D);
            background-size: 200% auto;
            color: #fff;
            background-clip: text;
            text-fill-color: transparent;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradient 3s ease infinite;
            font-weight: 800 !important;
            letter-spacing: -1px;
            padding-bottom: 0.5rem;
        }

        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        
        /* Modern Gradient Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #4ECDC4 0%, #556270 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(78, 205, 196, 0.2) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(78, 205, 196, 0.4) !important;
            filter: brightness(1.1);
        }

        /* Glassmorphic Form Container */
        [data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            margin-bottom: 2rem;
        }

        /* Avatar styling */
        .avatar-circle {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background: linear-gradient(135deg, #FF6B6B 0%, #FFE66D 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 1.2rem;
            box-shadow: 0 4px 10px rgba(255, 107, 107, 0.3);
        }
        
        hr {
            border-color: rgba(255,255,255,0.05) !important;
        }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

def login(email, password):
    response = requests.post(f"{API_URL}/auth/jwt/login", data={"username": email, "password": password})
    if response.status_code == 200:
        st.session_state.token = response.json().get("access_token")
        st.success("Welcome back! ✨")
        st.rerun()
    else:
        st.error(f"Login failed: {response.text}")

def register(email, password):
    response = requests.post(f"{API_URL}/auth/register", json={
        "email": email, 
        "password": password, 
        "is_active": True, 
        "is_superuser": False, 
        "is_verified": False
    })
    if response.status_code == 201:
        st.success("Welcome aboard! 🎉 Please log in.")
    else:
        st.error(f"Registration failed: {response.text}")

def logout():
    st.session_state.token = None
    st.rerun()

def get_feed():
    headers = {"Authorization": f"Bearer {st.session_state.token}"} if "token" in st.session_state and st.session_state.token else {}
    response = requests.get(f"{API_URL}/feed", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Could not fetch the feed. Ensure the backend is running.")
        return []

def delete_post(post_id):
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.delete(f"{API_URL}/delete/{post_id}", headers=headers)
    if response.status_code == 200:
        st.success("Post removed 🗑️")
        st.rerun()
    else:
        st.error(f"Failed to delete: {response.text}")

st.title("Nexus Feed")
st.markdown("<p style='color: #888; margin-top: -15px; margin-bottom: 30px; font-weight: 300; font-size: 1.1rem;'>Share your moments with the world.</p>", unsafe_allow_html=True)

if "token" not in st.session_state or not st.session_state.token:
    with st.sidebar:
        st.header("Gateway")
        st.markdown("<p style='color: #888; font-size: 0.9rem;'>Enter your credentials to access the nexus.</p>", unsafe_allow_html=True)
        choice = st.radio("Mode", ["Sign In", "Create Account"], horizontal=True)
        email = st.text_input("Email", placeholder="you@domain.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if choice == "Sign In":
            if st.button("Authenticate", use_container_width=True):
                login(email, password)
        else:
            if st.button("Join Nexus", use_container_width=True):
                register(email, password)
    
    st.info("👋 You must authenticate to view the feed or upload content.")

else:
    st.sidebar.button("Log Out", on_click=logout, use_container_width=True)
    
    # Upload Form
    with st.form("upload_form", clear_on_submit=True):
        st.markdown("<h3 style='margin-bottom:0;'>✨ Create New Post</h3>", unsafe_allow_html=True)
        
        upload_file = st.file_uploader("Select Media", type=["jpg", "jpeg", "png", "mp4", "mov", "avi"], help="Upload an image or video")
        caption = st.text_input("Caption", placeholder="What's on your mind?")
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Publish Post")
        
        if submitted and upload_file is not None:
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            files = {"file": (upload_file.name, upload_file.getvalue(), upload_file.type)}
            data = {"caption": caption}
            
            with st.spinner("🚀 Broadcasting to Nexus..."):
                response = requests.post(f"{API_URL}/upload", headers=headers, files=files, data=data)
            
            if response.status_code == 200:
                st.success("Successfully broadcasted! 🎉")
                st.rerun()
            else:
                st.error(f"Upload failed: {response.text}")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render Feed
    posts = get_feed()
    
    if not posts:
        st.markdown("""
        <div style='text-align:center; padding: 3rem; background: rgba(255,255,255,0.02); border-radius: 16px; border: 1px dashed rgba(255,255,255,0.1);'>
            <h2 style='color: #4ECDC4;'>Silence...</h2>
            <p style='color: #888;'>Be the first to echo in the Nexus.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for post in posts:
            with st.container(border=True):
                user_email = post.get("email", "Unknown Hacker")
                user_initial = user_email[0].upper() if user_email else "?"
                created_at = post.get("created_at", "")[:10]
                
                # Header: Avatar + Meta
                col1, col2 = st.columns([1, 12])
                with col1:
                    st.markdown(f"<div class='avatar-circle'>{user_initial}</div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<strong style='font-size: 1.1rem; color: #fff;'>{user_email}</strong><br><span style='color: #666; font-size: 0.85rem;'>{created_at}</span>", unsafe_allow_html=True)
                
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                
                # Caption
                if post.get("caption"):
                    st.markdown(f"<div style='font-size: 1.1rem; line-height: 1.5; margin-bottom: 1rem; color: #eee;'>{post.get('caption')}</div>", unsafe_allow_html=True)
                
                # Media
                file_type = post.get("file_type", "")
                url = post.get("url")
                
                if file_type == "photo" and url:
                    st.image(url, use_container_width=True)
                elif file_type == "video" and url:
                    st.video(url)
                elif url:
                    st.markdown(f"<a href='{url}' target='_blank' style='color: #4ECDC4;'>📎 View Attached Media</a>", unsafe_allow_html=True)
                
                # Delete action natively aligned
                if post.get("is_owner"):
                    st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)
                    col1, col2 = st.columns([10, 2])
                    with col2:
                        if st.button("Delete", key=f"delete_{post.get('id')}", help="Permanently remove this post"):
                            delete_post(post.get('id'))
                else:
                    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
