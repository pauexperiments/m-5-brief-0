from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Any
from loguru import logger
import sys
import os
from modules.calculation import calculate


APP_NAME = "m-5-brief-0"

app = FastAPI()


# Logs

logger.remove()
logger.add(sys.stdout, level="INFO", format="[{time}] {level} - {message}")
M_5_BRIEF_0_BACKEND_LOG_PATH = os.getenv("M_5_BRIEF_0_BACKEND_LOG_PATH")
if M_5_BRIEF_0_BACKEND_LOG_PATH:
    logger.add(f"{M_5_BRIEF_0_BACKEND_LOG_PATH}", rotation="1 week", retention="4 weeks", level="INFO", format="[{time}] {level} - {message}")


# Middleware to log requests and responses
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Appel {request.method} {request.url}")
    try:
        body = await request.body()
        logger.info(f"Body: {body.decode('utf-8')}")
    except Exception as e:
        logger.warning(f"Issue with body: {e}")
    try:
        response = await call_next(request)
        logger.info(f"Status: {response.status_code}")
        return response
    except Exception as exc:
        logger.error(f"Error: {exc}")
        raise

# Routes

@app.get("/")
def root():
    return {"name": APP_NAME}    

@app.get("/health")
def health():
    logger.info("/health")
    return {"status": "ok"}

@app.get("/calculation")
def calculation(n: int):
    logger.info(f"/calculation?n={n}")
    return {"results": calculate(n)}