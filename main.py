import os
import asyncio
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn

from orchestrator import Orchestrator
from utils.health_checker import HealthChecker

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Agentic Loop Content Automation")

# Initialize components
health_checker = HealthChecker()
orchestrator = Orchestrator()

class StartResponse(BaseModel):
    status: str
    message: str
    task_id: str

@app.get("/health")
async def health_check():
    """Check health status of all agents"""
    try:
        health_status = await health_checker.check_all_agents()
        if health_status["healthy"]:
            return JSONResponse(content={"status": "healthy", "details": health_status})
        else:
            return JSONResponse(
                status_code=503,
                content={"status": "unhealthy", "details": health_status}
            )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={"status": "error", "message": str(e)}
        )

@app.post("/start", response_model=StartResponse)
async def start_automation(background_tasks: BackgroundTasks):
    """Start the content automation process"""
    try:
        # Check health first
        health_status = await health_checker.check_all_agents()
        if not health_status["healthy"]:
            raise HTTPException(
                status_code=503,
                detail="System is not healthy. Please check /health endpoint for details."
            )
        
        # Generate task ID
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Start orchestrator in background
        background_tasks.add_task(orchestrator.run, task_id)
        
        return StartResponse(
            status="started",
            message="Content automation process has been started",
            task_id=task_id
        )
        
    except Exception as e:
        logger.error(f"Failed to start automation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Agentic Loop Content Automation API", "endpoints": ["/health", "/start"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
