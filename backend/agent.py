import os
import json
import torch
from datetime import datetime
from langchain import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Load hyperparameters from JSON file (assumes hyperparameters.json is in the project root)
CONFIG_PATH = os.path.join(os.path.dirname(__file__), ".", "config.json")
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

# Set environment variables using values from the config
os.environ["HF_TOKEN"] = config.get("hf_token", "")
os.environ["HF_HOME"] = config.get("hf_home", "")

# Retrieve hyperparameters from the config file
model_id = config.get("model_id", "meta-llama/Llama-2-13b-hf")
max_length = config.get("max_length", 2048)
min_length = config.get("min_length", 512)
length_penalty = config.get("length_penalty", 0.5)
temperature = config.get("temperature", 0.7)

print(f"Using model: {model_id}")

# Load the tokenizer and model.
tokenizer = AutoTokenizer.from_pretrained(model_id, token=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    token=True,
    torch_dtype=torch.float16,    # Use half-precision for inference
    low_cpu_mem_usage=True,
    device_map="auto"             # Automatically partition the model across available GPUs
)

# Create a Hugging Face text-generation pipeline
hf_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Initialize the LangChain LLM wrapper with hyperparameters from config
llm = HuggingFacePipeline(
    pipeline=hf_pipeline,
    model_kwargs={
        "max_length": max_length,
        # "min_length": min_length,
        "length_penalty": length_penalty,
        "temperature": temperature,
        "no_repeat_ngram_size": config.get("no_repeat_ngram_size", 3),
        "repetition_penalty": config.get("repetition_penalty", 1.2),
        "top_k": config.get("top_k", 50),
        "top_p": config.get("top_p", 0.95),
        "do_sample": config.get("do_sample", True)
    }
)

# Define prompt and chain using the Runnable interface
prompt = PromptTemplate(input_variables=["task"], template="{task}")
chain = prompt | llm | StrOutputParser()

# Function to record conversation logs in a JSON Lines file under data/
def record_conversation(task, suggestion, result):
    # Define the log file path; this will be in your project's data/ folder.
    log_file = os.path.join(os.path.dirname(__file__), "..", "data", "conversations.jsonl")
    conversation_entry = {
        "timestamp": datetime.now().isoformat(),
        "task": task,
        "suggestion": suggestion,
        "result": result
    }
    # Append the new conversation as a JSON object on a new line.
    with open(log_file, "a") as f:
        f.write(json.dumps(conversation_entry) + "\n")

def execute_task(task_input):
    from .tasks import run_workflow
    suggestion = chain.invoke({"task": task_input})
    result = run_workflow(task_input, suggestion)
    # Record the conversation history
    record_conversation(task_input, suggestion, result)
    return {"suggestion": suggestion, "result": result}
