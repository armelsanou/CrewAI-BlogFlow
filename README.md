# CrewAI-BlogFlow with Open source LLM
This script focuses on structured blog content generation, so "BlogFlow" reflects its purpose well.

## 📌 Overview
FlowDemo.py implements a CrewAI workflow for generating blog content. It defines a structured state model (BlogState) to track research, drafting, and final content generation.

## 🛠️ Dependencies
Ensure the following packages are installed:

#### Caution : CrewAI requires Python >=3.10 and <3.13

pip install crewai langchain_ollama python-dotenv crewai-tools agentops 
## ⚙️ Configuration
No additional configuration is required unless modifying the model parameters.

## 🚀 Running the Script
Execute the script using:

python FlowDemo.py

## Linear Flow

![image](https://github.com/user-attachments/assets/d4f8ad07-cd51-4c88-9a28-dd6667493cc6)


## 📚 Features

Structured Content Creation workflow
State Management with BlogState
Integration with OllamaLLM (ollama/llama3.2:3b)
Dynamic Research and Drafting Process
