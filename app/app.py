from fastapi import FastAPI, HTTPException
from .schemas import PostCreate, PostResponse
from app.db import create_db_and_tables, get_async_session, Post
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

    # Cleanup code can be added here if needed

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

text_posts = {
    1: {
        "title": "The Power of Consistency",
        "content": "Small daily efforts compound into big results over time. Focus on showing up every day, even when motivation is low. Consistency beats intensity in the long run."
    },
    2: {
        "title": "Learning Never Stops",
        "content": "The moment you think you know everything is the moment growth stops. Stay curious, keep exploring, and always remain a student of life."
    },
    3: {
        "title": "Failure is Feedback",
        "content": "Failure is not the opposite of success; it is part of the journey. Each mistake teaches something valuable that moves you closer to improvement."
    },
    4: {
        "title": "Start Before You're Ready",
        "content": "Waiting for the perfect moment often leads to no action at all. Begin with what you have and improve along the way."
    },
    5: {
        "title": "Focus on the Process",
        "content": "Results are important, but the process is what shapes your skills and mindset. Enjoy the journey and the results will follow."
    },
    6: {
        "title": "Discipline Over Motivation",
        "content": "Motivation comes and goes, but discipline keeps you moving forward even on difficult days."
    },
    7: {
        "title": "Growth Happens Outside Comfort",
        "content": "Comfort zones feel safe, but they limit progress. Challenge yourself regularly to unlock new abilities."
    },
    8: {
        "title": "Value Your Time",
        "content": "Time is one of the few resources that can never be recovered. Spend it on things that truly matter."
    },
    9: {
        "title": "Progress Over Perfection",
        "content": "Perfection can slow you down. Focus on making progress step by step instead of waiting for flawless outcomes."
    },
    10: {
        "title": "Curiosity Drives Innovation",
        "content": "Many great discoveries started with a simple question. Keep asking why and how things work."
    },
    11: {
        "title": "Build Strong Habits",
        "content": "Your habits define your future. Replace small bad habits with productive ones and watch the transformation."
    },
    12: {
        "title": "Embrace Challenges",
        "content": "Challenges are opportunities in disguise. Each problem solved builds confidence and resilience."
    },
    13: {
        "title": "Think Long Term",
        "content": "Short-term discomfort often leads to long-term rewards. Keep your bigger vision in mind."
    },
    14: {
        "title": "Knowledge is an Investment",
        "content": "Every skill you learn increases your value. Invest time in learning things that expand your capabilities."
    },
    15: {
        "title": "Stay Adaptable",
        "content": "The world changes quickly. Being flexible and willing to adapt is a powerful advantage."
    },
    16: {
        "title": "Collaboration Matters",
        "content": "Great achievements rarely happen alone. Working with others brings diverse ideas and better solutions."
    },
    17: {
        "title": "Keep Things Simple",
        "content": "Complex solutions are not always better. Simplicity often leads to clarity and efficiency."
    },
    18: {
        "title": "Take Breaks to Grow",
        "content": "Rest is not a waste of time. Proper breaks improve creativity, focus, and long-term productivity."
    },
    19: {
        "title": "Celebrate Small Wins",
        "content": "Recognizing small achievements keeps motivation alive and reminds you that progress is happening."
    },
    20: {
        "title": "Stay Curious",
        "content": "Curiosity is the engine of learning. Keep exploring ideas, asking questions, and discovering new perspectives."
    }
}

@app.get("/posts")
def get_all_posts(limit : int = None):
    if limit is not None:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{id}")
def get_post(id : int) -> PostResponse:
    if id not in text_posts :
        return HTTPException(status_code=404, detail="Post not found")
    
    return text_posts.get(id)

@app.post("/posts") 
def create_post(post: PostCreate) -> PostResponse:
    new_post = {"title" : post.title, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post

@app.delete("/posts/{id}")
def delete_post(id : int) :
    if id not in text_posts : 
        return HTTPException(status_code=404, detail='Post not found')
    deleted = text_posts[id]
    del text_posts[id]
    return {text_posts[id] if id in text_posts else "Post deleted successfully": deleted}
