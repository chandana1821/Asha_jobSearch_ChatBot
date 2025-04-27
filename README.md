# Asha AI Chatbot

## Overview
Asha AI Chatbot helps job seekers find relevant jobs based on their qualifications and job roles. It leverages natural language processing (NLP) and integrates real-time job data from Adzuna and Gemini APIs.

---

## Technologies Used

### Frontend:
- **HTML/CSS**: To build the user interface.
- **JavaScript**: For frontend interactivity (sending and receiving messages).

### Backend:
- **Flask**: The Python web framework for handling server-side logic.
- **Python**: Backend language for logic implementation (API calls, data processing).

### NLP:
- **spaCy**: For basic NLP tasks such as named entity recognition (job titles, locations).
- **Gemini API**: To power intelligent conversation capabilities (context awareness, dynamic responses).

### APIs:
- **Adzuna API**: For fetching job listings based on user input.
- **Gemini API**: To enable intelligent, natural language interactions.
- **Herkey.com**: For additional conversational data if needed.

### Environment:
- **.env**: To store sensitive API keys and credentials.

---

## Chatbot Architecture

### High-Level Architecture:
- **User Interface (UI)**: The front-end chat interface where users interact with the bot (HTML, CSS, JavaScript).
- **Backend Server**: Handles API calls, data processing, and chatbot logic (Flask/Python).
- **NLP Model**: spaCy or Gemini API for natural language processing (job title extraction, intent recognition).
- **Data Source APIs**: Integration with Adzuna API (for job listings), Gemini API (for advanced conversation capabilities), and other data providers.

### Flow Diagram:
Visualize how the chatbot receives user input, processes the intent using NLP, fetches job data, and responds to the user.

---

## Setup Instructions

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-repo/asha_chatbot.git
    ```

2. **Install Dependencies**:
    Ensure you have Python 3.8+ installed.
    Install necessary libraries using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Environment Variables**:
    Create a `.env` file and add your API keys:
    ```
    ADZUNA_APP_ID=your_adzuna_app_id
    ADZUNA_APP_KEY=your_adzuna_app_key
    GEMINI_API_KEY=your_gemini_api_key
    ```

4. **Run the Flask Application**:
    Start the server by running:
    ```bash
    python app.py
    ```
    Visit `http://127.0.0.1:5000/` in your browser to interact with the chatbot.

---

## Integration Processes

### Adzuna API Integration:
Retrieve job listings by making GET requests to Adzuna API, passing parameters like job title, location, and category.

Example:
```python
response = requests.get(
    f"https://api.adzuna.com/v1/api/jobs/us/search/1?app_id={app_id}&app_key={app_key}&title={job_title}&location={location}"
)
