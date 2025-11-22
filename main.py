from fastapi import FastAPI, HTTPException
import httpx
import openai
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables from a .env file (make sure to store your OpenAI API Key here)
load_dotenv()

# Initialize OpenAI API client
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure the OPENAI_API_KEY is set in the .env file

# FastAPI app instance
app = FastAPI()

# Define request and response models
class UserMessage(BaseModel):
    message: str

class ModelResponse(BaseModel):
    response: str

# Endpoint to send message to the model and get a response
@app.post("/api/message", response_model=ModelResponse)
async def chat_with_model(user_message: UserMessage):
    # Extract user message
    user_input = user_message.message
    
    try:
        # Send the message to the OpenAI GPT-4 API
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Specify the model (you can change it to "gpt-3.5-turbo" or others)
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        
        # Extract the model's response
        model_reply = response.choices[0].message['content'].strip()
        
        # Return the response back to the user
        return ModelResponse(response=model_reply)
    
    except Exception as e:
        # Handle API errors or other issues
        raise HTTPException(status_code=500, detail=f"Error connecting to model: {str(e)}")

# Health check endpoint (optional)
@app.get("/health")
def health_check():
    return {"status": "Model endpoint is up and running!"}

