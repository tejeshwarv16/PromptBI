from flask import Blueprint, jsonify, request
from . import services
import json
import pandas as pd

bp = Blueprint('main', __name__)

data_cache = {
    'df': None,
    'filename': None
}

@bp.route('/process-prompt', methods=['POST'])
def process_prompt():
    data = request.get_json()
    prompt = data.get('prompt', None)
    if not prompt:
        return jsonify([{"type": "error", "data": "Prompt is missing"}]), 400

    plan = services.get_ai_intent(prompt)
    actions = plan.get('actions', [])
    results = []

    for action in actions:
        intent = action.get('intent')

        if intent == 'load_data':
            filename = action.get('filename')
            if not filename:
                results.append({"type": "error", "data": "Filename not specified for load_data."})
                continue
            
            df, error = services.load_file_to_dataframe(filename)
            if error:
                results.append(error)
                break # Stop processing if file load fails
            
            data_cache['df'] = df
            data_cache['filename'] = filename
            
            insights = services.get_automated_insights(df)
            data_json = df.to_json(orient='split')
            
            results.append({"type": "insights", "data": insights})
            results.append({"type": "table", "data": json.loads(data_json)})

        elif intent == 'visualize_data' or intent == 'ask_question':
            if data_cache['df'] is None:
                results.append({"type": "answer", "data": "Please load a dataset first."})
                continue
            
            df = data_cache['df']
            action_prompt = action.get('prompt')

            if intent == 'visualize_data':
                chart_details = services.get_chart_details(action_prompt, df.columns.tolist())
                if 'error' in chart_details:
                    results.append(chart_details)
                else:
                    results.append({"type": "chart", "spec": chart_details})
            
            elif intent == 'ask_question':
                code, error = services.get_qa_answer(action_prompt, df)
                if error:
                    results.append(error)
                else:
                    try:
                        result = eval(code, {'pd': pd}, {'df': df})
                        results.append({"type": "answer", "data": f"The answer is: {result}"})
                    except Exception as e:
                        results.append({"type": "error", "data": f"Failed to execute query: {e}"})
        else:
            results.append({"type": "error", "data": f"Unknown intent: {intent}"})

    return jsonify(results)