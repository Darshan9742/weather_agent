from flask import Flask, render_template, request, jsonify
from agent import get_proactive_tip, get_reactive_tips
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/reactive_tips', methods=['POST'])
def reactive_tips_api():
    appliances = request.json.get('appliances')
    if not appliances:
        return jsonify({"error": "No appliance data provided"}), 400
    
    try:
        tips_data = get_reactive_tips(appliances)
        if "error" in tips_data:
            return jsonify(tips_data), 500
        return jsonify(tips_data), 200
    except Exception as e:
        print(f"Error generating reactive tips: {e}")
        return jsonify({"error": "Failed to generate tips."}), 500

@app.route('/api/proactive_tip', methods=['POST'])
def proactive_tip_api():
    location = request.json.get('location')
    if not location:
        return jsonify({"error": "No location provided"}), 400

    try:
        response = get_proactive_tip(location)
        # Check if the response from the LLM contains a valid output
        if 'output' in response:
            return jsonify({"tip": response['output']}), 200
        else:
            return jsonify({"error": "Failed to get a tip from the AI."}), 500
    except Exception as e:
        print(f"Error generating proactive tip: {e}")
        return jsonify({"error": "Failed to generate tip."}), 500

if __name__ == '__main__':
    app.run(debug=True)