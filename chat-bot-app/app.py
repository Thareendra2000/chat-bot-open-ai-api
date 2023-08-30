from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the default route to return the index.html file
@app.route("/")
def index():
    return render_template("index.html")

# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    try:
        # Get the message from the POST request
        message = request.json.get("message")
        
        # Send the message to OpenAI's API and receive the response
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ]
        )
        
        # Check if a valid response was received
        if completion.choices and completion.choices[0].message:
            return jsonify({"response": completion.choices[0].message})
        else:
            return jsonify({"error": "Failed to generate a response."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
