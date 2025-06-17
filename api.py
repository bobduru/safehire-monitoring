from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
import pandas as pd
from dotenv import load_dotenv

import uvicorn

# Load environment variables
load_dotenv()

app = FastAPI()



# CORS middleware configuration
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/prompt")
async def get_prompt(add_keywords_context: bool = True):
    from utils import create_prompt
    try:
        prompt, labels = create_prompt(add_keywords_context=add_keywords_context)
        
        return {"prompt": prompt, "labels": labels}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating prompt: {str(e)}")
    
    

@app.get("/errors")
async def get_errors():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://safehire-api.echoagency.co.uk/v1/external/associations/corrections",
                headers={
                    "X-API-KEY": os.getenv("API_KEY"),
                    "X-API-SECRET": os.getenv("API_SECRET")
                }
            )
            response.raise_for_status()
            print(response.json())
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)