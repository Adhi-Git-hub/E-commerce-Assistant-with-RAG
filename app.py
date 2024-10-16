from flask import Flask, render_template, request, jsonify
from ecommercebot import generate_response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('chatbot.html')

@app.route('/ask', methods=['POST'])
def ask_bot():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({"error": "Query not provided"}), 400

    # Get the response from the bot
    response = generate_response(query)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
