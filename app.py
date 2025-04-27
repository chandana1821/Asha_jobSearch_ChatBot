from flask import Flask, request, jsonify, render_template
import requests
import spacy
import json
import openai

# Initialize Flask app
app = Flask(__name__)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Adzuna API credentials
APP_ID = "your_ID"
APP_KEY = "your_key"

# Initialize OpenAI client (NEW)
client = openai.OpenAI(api_key="your_key")  # 🔥 PUT your actual API key here

# Common job titles (you can extend this list)
COMMON_JOB_TITLES = [
    "developer", "designer", "engineer", "analyst", "manager", "tester", "intern", "researcher"
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()

    # Handle greetings and casual replies first
    conv_response = handle_conversation(user_message)
    if conv_response:
        return conv_response

    try:
        # Extract job title and location from user input
        job, location = extract_job_details(user_message)

        if not job:
            # Fallback to OpenAI if no job title found
            ai_reply = ask_openai(user_message)
            return jsonify({"reply": ai_reply})

        # Search jobs on Adzuna
        jobs = search_adzuna_jobs(job, location)

        if not jobs:
            reply = f"🔍 No current openings found for '{job}' in {location or 'your location'}."
        else:
            reply = f"✅ Here are some '{job}' jobs for you:\n\n"
            for idx, job_data in enumerate(jobs[:5], 1):
                title = job_data.get("title", "No title")
                company = job_data.get("company", {}).get("display_name", "Unknown company")
                job_url = job_data.get("redirect_url", "#")
                reply += f"{idx}. {title} at {company}\n🔗 {job_url}\n\n"

        return jsonify({"reply": reply})

    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "⚠️ I'm having trouble fetching job info right now. Try again shortly!"})


def extract_job_details(message):
    """Extract job title and location using spaCy"""
    doc = nlp(message.lower())
    job = None
    location = None

    for token in doc:
        if token.pos_ == "NOUN" and token.text in COMMON_JOB_TITLES:
            job = token.text
            break

    for ent in doc.ents:
        if ent.label_ == "GPE":  # GPE = location entity
            location = ent.text
            break

    return job, location


def search_adzuna_jobs(job, location=""):
    """Fetch jobs using Adzuna API"""
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": 5,
        "what": job,
        "content-type": "application/json"
    }

    if location:
        params["where"] = location

    try:
        response = requests.get("adzuna-link", params=params, timeout=5)
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception as e:
        print("Adzuna Error:", e)
        return []


def handle_conversation(message):
    """Handle casual conversation like greetings, thanks, etc."""
    msg = message.lower().strip()

    if not msg:
        return jsonify({"reply": "Hi there! 👋 How can I assist your job search today?"})

    if any(msg.startswith(greet) for greet in ["hi", "hello", "hey"]):
        return jsonify({"reply": "👋 Hello! I'm Asha. You can ask about jobs like 'developer in Mumbai' or 'UI designer in Delhi'."})

    if any(kw in msg for kw in ["thank", "thanks", "tq", "ok", "okay", "kk"]):
        return jsonify({"reply": "You're welcome! 😊 Let me know if you want more job suggestions."})

    if msg in ["how are you", "how's it going"]:
        return jsonify({"reply": "I'm doing great! 🤖 I'm here to help you find the perfect job."})

    return None  # If not a casual conversation, continue job logic


def ask_openai(message):
    """Fetch casual conversation fallback from OpenAI GPT"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Asha, a friendly job assistant chatbot that also handles casual conversation."},
                {"role": "user", "content": message}
            ],
            max_tokens=150,
            temperature=0.7
        )
        ai_text = response.choices[0].message.content.strip()
        return ai_text
    except Exception as e:
        print("OpenAI Error:", e)
        return "Oops! I'm having a little trouble thinking clearly. 😅 Try again in a moment."


if __name__ == "__main__":
    app.run(debug=True)
