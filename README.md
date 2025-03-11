# AgentAI

An AI-powered automation agent built with LangChain and Llama 2, featuring a FastAPI backend and Streamlit frontend.

## Overview

AgentAI is a versatile automation platform that combines large language models with task automation capabilities. The system processes natural language requests, generates suggestions, and executes automated workflows while maintaining a conversation history.

## Features

- **Natural Language Processing**: Powered by Meta's Llama-2-13b model
- **Task Automation**: Workflow execution using Prefect
- **Data Validation**: Built-in data validation using Great Expectations
- **Conversation Logging**: Automatic logging of all interactions
- **Web Interface**: User-friendly Streamlit frontend
- **REST API**: FastAPI-based backend services

## Architecture

- **Frontend**: Streamlit application ([`frontend/app.py`](frontend/app.py))
- **Backend**: 
  - FastAPI server ([`backend/main.py`](backend/main.py))
  - LLM integration ([`backend/agent.py`](backend/agent.py))
  - Task automation ([`backend/tasks.py`](backend/tasks.py))
  - Data monitoring ([`backend/monitoring.py`](backend/monitoring.py))

## Setup

### Prerequisites

- Docker
- NVIDIA GPU with CUDA support
- Docker Compose

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AgentAI
```

2. Configure environment:
   - Update `backend/config.json` with your Hugging Face token
   - Adjust model parameters if needed

3. Build and run using Docker Compose:
```bash
docker-compose up --build
```

## Usage

### Web Interface

Access the Streamlit interface at `http://localhost:8501`:
- Run tasks using natural language
- Validate data files
- View conversation history

### API Endpoints

- `GET /run-task`: Execute automation tasks
- `GET /validate-data`: Validate data files
- `GET /conversations`: Retrieve conversation history

## Development

### Development Environment

The project includes a devcontainer configuration for VS Code:
- CUDA-enabled development environment
- Pre-configured Python extensions
- Automatic dependency installation

### Project Structure

```
AgentAI/
├── backend/
│   ├── agent.py      # LLM integration
│   ├── config.json   # Configuration
│   ├── main.py      # API endpoints
│   ├── monitoring.py # Data validation
│   └── tasks.py     # Automation workflows
├── frontend/
│   └── app.py       # Streamlit interface
├── data/
│   └── conversations.jsonl # Conversation logs
└── docker/
    └── ...          # Docker configurations
```

**Run Backend**:
   - In VSCode terminal: `uvicorn backend.main:app --host 0.0.0.0 --port 8000`
   - Test: `curl http://localhost:8000/run-task?task=process%20my%20files`

**Run Frontend**:
   - New terminal: `streamlit run frontend/app.py --server.port 8501`
   - Access via browser (forward port 8501 via SSH if needed).

<!-- **Initialize Great Expectations**:
   - Run: `great_expectations --v3-api init` inside the container.
   - Follow prompts to set up `great_expectations/` folder. -->


## License

MIT License

Copyright (c) 2025 Shiwen An
