from flask import Flask, request, jsonify, session
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.secret_key = ""  # Replace with a strong secret key

# Initialize Gemini AI Client
genai.configure(api_key="")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-pro")  # Ensure you're using the correct model

def get_gemini_response(prompt, history):
    """Generate AI response while handling empty outputs properly."""
    full_prompt = "\n".join(history + [prompt])  # Combine chat history and prompt
    try:
        response = model.generate_content(full_prompt)
        if response.text:  # Ensure a valid response exists
            return response.text.replace("**", "").strip()
        else:
            return "Sorry, I can't generate a response for this input."
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/api/chat", methods=["POST"])
def chatbot():
    if 'history' not in session:
        session['history'] = []  # Initialize chat history

    prompt = request.form.get('prompt', '').strip()
    if not prompt:
        return jsonify({'response': "Please enter a message."})

    # Use the last 5 history items to limit session data size
    history = session['history'][-5:]
    response = get_gemini_response(prompt, history)
    # Append both the user prompt and the AI response to session history
    session['history'].append(f"User: {prompt}")
    session['history'].append(f"Bot: {response}")
    session.modified = True

    return jsonify({'response': response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
