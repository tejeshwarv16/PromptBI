import requests
import json
import pandas as pd
import os

# Define the local models we will use for different tasks
INTENT_MODEL = 'phi3:medium'
GENERATION_MODEL = 'phi3:medium'

# The local URL for the Ollama API
OLLAMA_API_URL = "http://localhost:11434/api/chat"

def get_ai_intent(user_prompt):
    """
    Sends the user's prompt to a local AI to get a list of actions.
    """
    system_prompt = """
    You are an expert multi-task-detection assistant. Your task is to analyze a user's prompt
    and break it down into a sequence of one or more actions.

    The possible intents are: 'load_data', 'ask_question', 'visualize_data'.

    You must respond with only a single, minified JSON object containing a list called "actions".
    Each action in the list should have an "intent" and any necessary parameters.
    - For 'load_data', include a "filename".
    - For 'visualize_data' and 'ask_question', include the original "prompt" that corresponds to that action.

    Example 1:
    User prompt: "Load sales_report.xlsx"
    Your response: {"actions": [{"intent": "load_data", "filename": "sales_report.xlsx"}]}

    Example 2:
    User prompt: "Load sales_report.xlsx and then visualize sales by region"
    Your response: {"actions": [{"intent": "load_data", "filename": "sales_report.xlsx"}, {"intent": "visualize_data", "prompt": "visualize sales by region"}]}
    
    Example 3:
    User prompt: "what is the total profit"
    Your response: {"actions": [{"intent": "ask_question", "prompt": "what is the total profit"}]}
    """
    try:
        payload = {
            "model": INTENT_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "format": "json",
            "stream": False
        }
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        response_data = response.json()
        ai_response_json = response_data['message']['content']
        return json.loads(ai_response_json)
    except requests.exceptions.ConnectionError:
        return {"error": "Connection failed. Is the Ollama application running?"}
    except Exception as e:
        return {"error": f"Failed to parse AI response: {e}"}

def load_file_to_dataframe(filename):
    """
    Loads a data file (.csv, .xlsx) into a Pandas DataFrame.
    """
    file_path = os.path.join('data', filename)
    if not os.path.exists(file_path):
        return None, {"error": f"File not found: {filename}"}
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            return None, {"error": "Unsupported file type. Please use .csv or .xlsx."}
        df = df.fillna(value='')
        return df, None
    except Exception as e:
        return None, {"error": f"Error reading file: {str(e)}"}

def get_automated_insights(df):
    """
    Sends a sample of the dataframe to a local LLM to generate insights.
    """
    data_sample = df.head().to_csv()
    system_prompt = f"""
    You are a data analyst. Below is a sample of a dataset.
    Provide a brief, bulleted list of 2-3 key insights or observations.
    """
    try:
        payload = {"model": GENERATION_MODEL, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": data_sample}], "stream": False}
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        response_data = response.json()
        return response_data['message']['content']
    except Exception as e:
        return "Could not generate insights."

def get_chart_details(prompt, df_columns):
    """
    Asks the AI to determine chart details from a prompt and data columns.
    """
    columns_str = ", ".join(df_columns)
    system_prompt = f"""
    You are a chart generation assistant. Based on the user's prompt and the available data columns, 
    determine the best chart type and columns.
    Available columns: [{columns_str}]
    Possible chart types: 'bar', 'line', 'pie'.
    Respond with a single, minified JSON object: {{"chart_type": "type", "x_column": "x", "y_column": "y", "title": "title"}}
    """
    try:
        payload = {"model": INTENT_MODEL, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}], "format": "json", "stream": False}
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        response_data = response.json()
        return json.loads(response_data['message']['content'])
    except Exception as e:
        return {"error": "Could not determine chart details."}

def get_qa_answer(prompt, df):
    """
    Asks the AI to generate a line of Pandas code to answer a question.
    """
    df_head_str = df.head().to_string()
    system_prompt = f"""
    You are a Python Pandas programmer. Given a dataframe `df`, write a single line of code to answer the user's question.
    The result must be a single value. Respond with only the code.
    Dataframe head:
    {df_head_str}
    """
    try:
        payload = {"model": GENERATION_MODEL, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}], "stream": False}
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        code_to_execute = response.json()['message']['content'].strip()
        forbidden_keywords = ['import', 'os', 'sys', 'eval', 'exec', '__']
        if any(keyword in code_to_execute for keyword in forbidden_keywords):
            return None, {"error": "Generated code contains restricted keywords."}
        return code_to_execute, None
    except Exception as e:
        return None, {"error": "Could not generate code to answer question."}