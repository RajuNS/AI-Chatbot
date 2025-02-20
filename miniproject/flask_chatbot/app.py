from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = ""  # Change this to a strong secret key

# Initialize Gemini AI Client
genai.configure(api_key="")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-pro")  # Ensure the correct model is used

def get_gemini_response(prompt, history):
    """Generate AI response while handling empty outputs properly."""
    
    full_prompt = "\n".join(history + [prompt])  # Maintain history properly

    try:
        response = model.generate_content(full_prompt)

        if response.text:  # Ensure valid response exists
            formatted_response = response.text.replace("**", "").strip()  
            return formatted_response  # Preserve new lines
        else:
            return "Sorry, I can't generate a response for this input."

    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/", methods=['POST', 'GET'])
def chatbot():
    if 'history' not in session:
        session['history'] = []  # Initialize chat history

    if request.method == 'POST':
        prompt = request.form['prompt'].strip()

        if not prompt:  # Ignore empty inputs
            return jsonify({'response': "Please enter a message."})

        history = session['history'][-5:]  # Limit chat history to prevent bloating
        
        response = get_gemini_response(prompt, history)

        # Append user prompt and response separately to maintain order
        session['history'].append(f"User: {prompt}")
        session['history'].append(f"Bot: {response}")

        session.modified = True  # Mark session as modified
        return jsonify({'response': response})

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
