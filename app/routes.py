from flask import Blueprint, request, jsonify
from .chatbot import handle_chat 
from flask_cors import CORS

main = Blueprint('main', __name__)
CORS(main)

@main.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        user_message = data.get('message')
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        response = handle_chat(user_message)
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @main.route('/smartphones', methods=['GET'])
# def smartphones():
#     all_smartphones = get_all_smartphones()
#     return jsonify(all_smartphones)
