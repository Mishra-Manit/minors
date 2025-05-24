# Talking Head Flask Application

This is a Flask-based web application that implements a talking head avatar with text-to-speech capabilities.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Features

- Text-to-speech capability
- 3D avatar visualization
- Real-time lip sync
- Backend processing capability through Flask

## Note
Make sure to replace the Google Cloud TTS API key in the HTML file with your own key for production use.

## Structure
- `app.py` - Main Flask application
- `templates/index.html` - Frontend interface
- `requirements.txt` - Python dependencies 