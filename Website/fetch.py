from flask import Flask, request, jsonify
import ollama

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')

    # Send message to Ollama model
    response = ollama.chat(model='your_model', messages=[{'role': 'user', 'content': user_message}])

    return jsonify({"reply": response['message']['content']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
