# Talking Head Flask Application

This is a Flask-based web application that implements a talking head avatar with text-to-speech capabilities and AI-powered debate rebuttal generation.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```
Or create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

3. Run the Flask application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## Features

- Text-to-speech capability
- 3D avatar visualization
- Real-time lip sync
- **AI-powered debate rebuttal generation** - Submit your political inclinations and context via the form, then generate strong rebuttals to any statement
- Backend processing capability through Flask

## API Endpoints

### GET /
Main application interface

### GET /form  
Debate registration form

### POST /submit_debate
Submit user debate information (name, political inclinations, context)

### POST /speak
Generate AI-powered debate rebuttals
- Requires: `text` (statement to rebut)
- Optional: `name` (specific user's context to use)
- Returns: Generated rebuttal based on user's political context

## Note
Make sure to replace the Google Cloud TTS API key in the HTML file with your own key for production use.
Obtain an OpenAI API key from https://platform.openai.com/api-keys

## Structure
- `app.py` - Main Flask application with OpenAI integration
- `templates/index.html` - Frontend interface
- `templates/form.html` - Debate registration form
- `requirements.txt` - Python dependencies 