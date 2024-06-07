from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import os
import warnings
from dotenv import load_dotenv
from typing import Optional
from rag_model import ask_question


warnings.filterwarnings("ignore", message="WatchFiles detected changes")

# Ladet die .env Datei
load_dotenv()  

app = FastAPI()

# CORS konfigurieren
origins = [
    "http://localhost:8001",
    "http://127.0.0.1:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    user_id: str
    question: str
    conversation_id: Optional[str] = None

@app.post("/chat")
async def chat(query: Query):
    print("Received query:", query.json()) 

    conversation_id = query.conversation_id
    if conversation_id is None:
        conversation_id = get_next_conversation_id()  
    print("Current conversation_id:", conversation_id)  

    history = get_conversation_history(conversation_id)
    print("Conversation History:", history) 
    answer = ask_question(history, query.question)
    if not answer:
        raise HTTPException(status_code=500, detail="Error processing the query")
    
    save_conversation(query.user_id, conversation_id, query.question, answer)
    return {"answer": answer, "conversation_id": conversation_id}

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )

def save_conversation(user_id, conversation_id, question, answer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversations (user_id, conversation_id, question, answer) VALUES (%s, %s, %s, %s)",
        (user_id, conversation_id, question, answer)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_conversation_history(conversation_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT question, answer FROM conversations WHERE conversation_id = %s ORDER BY id ASC", 
        (conversation_id,)
    )
    history = cursor.fetchall()
    cursor.close()
    conn.close()
    return history


def get_next_conversation_id():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT current_id FROM conversation_counter WHERE id = 1")
    row = cursor.fetchone()
    next_id = row['current_id']
    cursor.execute("UPDATE conversation_counter SET current_id = current_id + 1 WHERE id = 1")
    conn.commit()
    cursor.close()
    conn.close()
    return str(next_id)

@app.get("/conversations")
async def get_conversations():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM conversations")
    conversations = cursor.fetchall()
    cursor.close()
    conn.close()
    return conversations
