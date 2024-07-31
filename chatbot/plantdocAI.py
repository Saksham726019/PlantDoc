from fastapi import FastAPI, Request
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os
from uuid import uuid4
import secrets

# Configure the Gemma API key
os.environ["GEMMA_API_KEY"] = "AIzaSyAb6wQ5hIITUe3vG2NUEZIdp59vRJpDgKk"
genai.configure(api_key=os.environ['GEMMA_API_KEY'])

model = genai.GenerativeModel()

# Initialize the FastAPI app
app = FastAPI()

# Add CORS middleware; allows two apis to communicate with each other
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

secret_key = secrets.token_hex(24)

# Add session middleware with a strong secret key
app.add_middleware(SessionMiddleware, secret_key=secret_key)

# In-memory session store
session_store = {}


# Define the Pydantic model for the request body
class UserInput(BaseModel):
    prompt: str


# Define the function to preprocess the user input
def preprocess_input(user_input, session_id):
    context = ("The following texts are just pre-information for you. "
               "When I say 'only reply to texts after this', then after that reply to it."
               "You are an AI language model, PLantDoc AI, specialized in plant disease. "
               "You are made by a team during Drexel University's CI 102 and 103 class. "
               "The team members are: Saksham Rajbhandari, Krithi Hari, Naman Bajpai, and Manish Gurun"
               "We are discussing plant diseases and their identification. "
               "You need to give detailed information about the diseases, "
               "their symptoms, causes, and possible treatments when the user asks for it. "
               "If people ask you for details of specific diseases, make sure you do it properly."
               "For general texts such as greetings or something like that, talk normally. "
               "When they ask related to plant diseases and their identification, please be precise and helpful. "
               "But remember you are only there to help with plant disease. "
               "Be nice, gentle, polite, and interactive and use emojis if you can. "
               "Moreover, when you need to give answers in list, make it a bullet point. "
               "All these contexts don't mean be very strictly bounded by it, okay? "
               "Make sure to remember the conversations. "
               "To remember the previous conversations, look at the text with 'User:' "
               "which are the information that the user sent to you so that you will know what they are talking about. "
               "Moreover, to look at the text with 'Plant Doctor:', which are the information you sent to the user. "
               "You don't have to type 'Plant Doctor:' in your response. "
               "Only reply to texts after this: "
               )

    if session_id not in session_store:
        session_store[session_id] = [context]

    # Append the new user input to the session history
    session_store[session_id].append(f"User: {user_input}")

    # Keep only the last 10 messages in the conversation history
    if len(session_store[session_id]) > 11:  # 10 user messages + context
        session_store[session_id] = session_store[session_id][-11:]

    # Join the session history into a single string
    conversation_history = " ".join(session_store[session_id])

    return conversation_history


@app.post("/generate")
async def generate_response(user_input: UserInput, request: Request):
    # Retrieve or create a session ID
    session_id = request.session.get("session_id")
    if not session_id:
        session_id = str(uuid4())
        request.session["session_id"] = session_id

    # Preprocess the input
    preprocessed_text = preprocess_input(user_input.prompt, session_id)

    # Generate a response using the model
    response = model.generate_content(preprocessed_text)
    response_text = response.text

    # Store the response in the session history
    session_store[session_id].append(f"Shampoo Sense: {response_text}")

    # Keep only the last 10 messages in the conversation history
    if len(session_store[session_id]) > 11:  # 10 messages + context
        session_store[session_id] = session_store[session_id][-11:]

    # Return the response
    return {"response": response_text}
