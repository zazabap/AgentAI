import sys
print(sys.path)

import os
import json
from fastapi import FastAPI, HTTPException
from .agent import execute_task
from .monitoring import validate_data

app = FastAPI()

@app.get("/run-task")
async def run_task(task: str):
    result = execute_task(task)
    return {"status": "success", "result": result}

@app.get("/validate-data")
async def check_data(file_path: str):
    validation_result = validate_data(file_path)
    return {"status": "success", "validation": validation_result}

@app.get("/conversations")
async def get_conversations():
    # Build the path to the conversation log file.
    log_file = os.path.join(os.path.dirname(__file__), "..", "data", "conversations.jsonl")
    
    # If the log file doesn't exist, return a 404 error.
    if not os.path.exists(log_file):
        raise HTTPException(status_code=404, detail="Conversation log file not found.")
    
    conversations = []
    try:
        # Each line in the log file is a separate JSON object.
        with open(log_file, "r") as f:
            for line in f:
                conversations.append(json.loads(line))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"conversations": conversations}
