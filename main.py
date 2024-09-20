from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure Google Generative AI API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set in the environment")

genai.configure(api_key=GOOGLE_API_KEY)

# FastAPI app setup
app = FastAPI()

# Allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any domain for testing
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Flashcards generation endpoint
@app.post("/generate-flashcards/")
async def generate_flashcards(summary: str = Form(...)):
    """
    Generate flashcards from the provided summary using Google Generative AI.
    Returns a list of flashcards in Question || Answer format.
    """
    if not summary:
        return {"error": "No summary provided to generate flashcards"}

    try:
        # Use the Generative AI to generate flashcards
        model = genai.GenerativeModel("gemini-1.5-flash")
        flashcard_result = model.generate_content([summary, "Generate flashcards in a Question || Answer format."])

        # Split the result into flashcards assuming it generates them in "Question || Answer" pairs
        flashcards = [
            {"question": fc.split("||")[0].strip(), "answer": fc.split("||")[1].strip()}
            for fc in flashcard_result.text.split("\n") if "||" in fc
        ]

        return {"flashcards": flashcards}

    except Exception as e:
        return {"error": f"Error generating flashcards: {str(e)}"}


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint to ensure the service is running properly.
    """
    return {"status": "ok", "message": "Flashcard generator is healthy"}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Flashcard Generator API!"}

