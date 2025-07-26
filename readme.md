# Prompt BI 💡

**Prompt BI** is a modern, web-based business intelligence application that allows users to upload, query, and visualize data using natural language commands.


## Features

* **Natural Language Commands**: Control the entire application through a simple, chat-like prompt interface.
* **Multi-Command Processing**: Execute multiple actions in a single prompt (e.g., "Load `sales_report.xlsx` and visualize profit by region").
* **Versatile File Support**: Load and analyze data from `.csv`, `.xlsx`, and `.txt` files.
* **Automated Insights**: Automatically generates a summary of key trends and statistics upon loading data.
* **On-Demand Visualization**: Generate bar, line, or pie charts in response to user prompts.
* **Natural Language Q&A**: Ask direct questions about your data (e.g., "What is the total sales?") and receive precise, calculated answers.

---

## Tech Stack

### Backend
* **Language**: Python 3.10
* **Framework**: Flask
* **AI**: Ollama (running `phi3:medium` locally)
* **Data Manipulation**: Pandas

### Frontend
* **Library**: React.js (with Vite)
* **API Client**: Axios
* **Charting**: Plotly.js

---

## How to Run Locally

To run this project on your own machine, follow these steps.

### Prerequisites
* [Python 3.10+](https://www.python.org/downloads/)
* [Node.js and npm](https://nodejs.org/en/download/)
* [Ollama](https://ollama.com/)

### 1. Backend Setup

```bash
# Clone the repository
git clone https://github.com/tejeshwarv16/PromptBI
cd PromptBI

# Set up the Python environment
conda create --name promptbi python=3.10
conda activate promptbi

# Navigate to the backend folder and install packages
cd backend
pip install -r requirements.txt # You will need to create this file

# Download the required AI model
ollama pull phi3:medium

# Place your data files (e.g., sales_report.xlsx) in the /backend/data/ folder.

# Run the backend server
python run.py
