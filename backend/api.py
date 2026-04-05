from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import re
from dotenv import load_dotenv
from agent import AutoPPTAgent

load_dotenv()

app = FastAPI(title="Auto PPT API")

# Allow CORS since front/back might run on different ports in dev, 
# although we will serve the frontend from backend static files
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoint
@app.post("/generate")
async def generate_ppt(topic: str = Form(...), num_slides: int = Form(5)):
    if not topic:
        raise HTTPException(status_code=400, detail="Topic is required")
    
    clean_topic = "".join(c if c.isalnum() else "_" for c in topic).lower()
    clean_topic = re.sub(r'_+', '_', clean_topic).strip('_')
    output_filename = f"{clean_topic}.pptx"
    output_filepath = os.path.join(os.getcwd(), output_filename)
    
    try:
        agent = AutoPPTAgent()
        agent.generate_ppt(topic, num_slides, output_filepath)
        
        # Check if the file was actually created
        if not os.path.exists(output_filepath):
            raise HTTPException(status_code=500, detail="Generation failed: File not created")
            
        return FileResponse(
            path=output_filepath, 
            filename=output_filename, 
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount the static frontend directory explicitly
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
