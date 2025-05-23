from fastapi import FastAPI, HTTPException, Request
from typing import List, Dict, Union
from fastapi.middleware.cors import CORSMiddleware 
from email_sender import send_emails
import uvicorn

app = FastAPI(
    title="Email Sender API",
    description="API to send emails using Gmail SMTP",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = [
    "http://localhost:8080",
    "https://flow-forge-campaigns.lovable.app"  
],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/send-emails", response_model=dict)
async def send_emails_endpoint(request: Request):
    """
    Send emails to multiple recipients.
    
    Request body should be a list of email objects, where each object has:
    - email: single email address or list of email addresses
    - subject: email subject
    - body: email body content
    """
    try:
        # Get the request body
        email_list = await request.json()
        
        # Validate the request structure
        if not isinstance(email_list, list):
            raise HTTPException(status_code=400, detail="Request body must be a list")
            
        # Process each email
        for email_data in email_list:
            if not isinstance(email_data, dict):
                raise HTTPException(status_code=400, detail="Each email entry must be an object")
                
            if 'email' not in email_data or 'subject' not in email_data or 'body' not in email_data:
                raise HTTPException(status_code=400, detail="Each email entry must contain 'email', 'subject', and 'body' fields")
        
        # Send the emails
        send_emails(email_list)
        return {"status": "success", "message": "Emails sent successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
