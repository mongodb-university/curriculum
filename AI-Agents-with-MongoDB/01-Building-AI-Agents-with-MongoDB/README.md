# AI Agents with MongoDB Skill

This repository contains code for an AI Agent that can:

- Answer questions about MongoDB using the MongoDB documentation as a knowledge base
- Summarize content from MongoDB documentation pages

## Project Structure

You can either:

- Run the completed agent in the root directory, or
- Follow the step-by-step implementation in the `lessons` directory

Each lesson builds upon the previous one, providing a gradual learning experience. If working through the lessons, copy the `key_param.py` file to each lesson directory (`lessons/02-*/`, `lessons/03-*/`, etc.) as you progress.

## Prerequisites

- Python 3.8 or higher
- [MongoDB Atlas account](https://www.mongodb.com/cloud/atlas/register) with a cluster, or [self-managed](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-deploy-local/) Atlas cluster
- API Keys:
  - [VoyageAI API key](https://docs.voyageai.com/docs/api-key-and-installation) for embeddings
  - [OpenAI API key](https://platform.openai.com/account/api-keys) for the language model

> [!NOTE]
> While this demo uses VoyageAI and OpenAI, you can modify the code to work with alternative providers.

## Setup Instructions

### Step 1: Navigate to the Project Directory

First, make sure you're in the correct directory:

```bash
cd AI-Agents-with-MongoDB/01-Building-AI-Agents-with-MongoDB
```

### Step 2: Configure Your API Keys

Create or edit the `key_param.py` file with your API credentials:

```python
openai_api_key = "your_openai_api_key_here"
voyage_api_key = "your_voyage_api_key_here" 
mongodb_uri = "your_mongodb_connection_string_here"
```

> **Important:** Replace the placeholder values with your actual API keys and MongoDB connection string.

### Step 3: Install the `uv` Package Manager

**Windows (PowerShell - run as Administrator if needed):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Verify installation:**
```bash
uv --version
```

### Step 4: Set Up Python Environment

**Initialize the project (run these commands one by one):**

**Windows (PowerShell):**
```powershell
# Initialize uv project
uv init

# Create virtual environment
uv venv

# Activate the environment
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
# Initialize uv project  
uv init

# Create virtual environment
uv venv

# Activate the environment
source .venv/bin/activate
```

**Verify your environment is active:** You should see `(.venv)` in your terminal prompt.

### Step 5: Install Dependencies

Install all required packages:

```bash
uv add langchain==0.3.24 langchain-openai==0.3.14 langgraph==0.3.31 langgraph-checkpoint-mongodb==0.1.3 pymongo==4.11.3 voyageai==0.3.7 datasets
```

**Verify installation:**
```bash
uv pip list
```

### Step 6: Load the Dataset (Required Before First Run)

**Important:** You must load the MongoDB documentation data before running the agent:

```bash
uv run data.py
```

This step will:
- Download MongoDB documentation datasets from Hugging Face
- Generate embeddings using VoyageAI
- Store data in your MongoDB database
- Create a vector search index

> **Note:** This process may take several minutes depending on your internet connection and the size of the dataset.

## Running the Agent

### Step 7: Customize and Run the Agent

1. **Optional:** Customize the queries in `main.py`. Examples:

   ```python
   # Ask a specific question about MongoDB
   execute_graph(app, "1", "What are some best practices for data backups in MongoDB?")
   
   # Test the agent's memory capabilities  
   execute_graph(app, "1", "What did I just ask?")
   ```

2. **Run the agent:**

   ```bash
   uv run main.py
   ```

## Troubleshooting

### Common Issues and Solutions

**Problem: `ModuleNotFoundError: No module named 'datasets'`**
- **Solution:** Make sure you installed all dependencies including `datasets`: 
  ```bash
  uv add datasets
  ```

**Problem: `sh : The term 'sh' is not recognized` (Windows)**
- **Solution:** Use the PowerShell installation command instead:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

**Problem: `No pyproject.toml found in current directory`**
- **Solution:** Make sure you're in the correct directory and run `uv init` first:
  ```bash
  cd AI-Agents-with-MongoDB/01-Building-AI-Agents-with-MongoDB
  uv init
  ```

**Problem: API key errors**
- **Solution:** Verify your API keys are correctly set in `key_param.py`:
  - OpenAI API key: Get from [OpenAI Platform](https://platform.openai.com/account/api-keys)
  - VoyageAI API key: Get from [VoyageAI](https://docs.voyageai.com/docs/api-key-and-installation)
  - MongoDB URI: Get from your MongoDB Atlas cluster

**Problem: MongoDB connection issues**
- **Solution:** 
  - Ensure your MongoDB Atlas cluster is accessible from your IP address
  - Check that your connection string includes the correct username/password
  - Verify your cluster is running and network access is configured

**Problem: Data loading takes too long or fails**
- **Solution:**
  - Ensure stable internet connection for downloading datasets
  - Check that your Atlas cluster has sufficient storage space
  - Verify VoyageAI API key is valid and has sufficient quota

> [!NOTE]
> This project uses the [`uv`](https://docs.astral.sh/uv/) package manager. If you prefer `pip` or `pipenv`, you'll need to adapt the installation commands.

## Attribution

### Datasets

- **MongoDB/mongodb-docs** by MongoDB, Inc.  
  License: CC BY 3.0  
  <https://huggingface.co/datasets/MongoDB/mongodb-docs>  
- **MongoDB/mongodb-docs-embedded** by MongoDB, Inc.  
  License: CC BY 3.0  
  <https://huggingface.co/datasets/MongoDB/mongodb-docs-embedded>  

### Models & APIs

- **VoyageAI** (`voyage-3-lite` embeddings)  
  <https://voyageai.com/>  
- **OpenAI** (GPT-4o via langchain-openai)  
  <https://openai.com>
- **MongoDB Atlas** (for database hosting)  
  <https://www.mongodb.com/cloud/atlas>
