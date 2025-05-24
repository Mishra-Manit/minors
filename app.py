from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client with better error handling
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("Warning: OPENAI_API_KEY not found in environment variables")
    print("Please set your OpenAI API key: export OPENAI_API_KEY='your_key_here'")

client = openai.OpenAI(api_key=api_key) if api_key else None

# Store debate submissions in memory (you might want to use a database in production)
debate_submissions = []

def find_user_submission(name=None):
    """Find the most recent submission, optionally by name"""
    if not debate_submissions:
        return None
    
    if name:
        # Find by name if provided
        for submission in reversed(debate_submissions):
            if submission.get('name', '').lower() == name.lower():
                return submission
    
    # Return most recent submission
    return debate_submissions[-1]

def generate_debate_rebuttal(statement_to_rebut, user_data):
    """Generate a debate rebuttal using OpenAI with smart prompt engineering"""
    
    if not client:
        return "Error: OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
    
    # Build context from user data
    political_leanings = ", ".join(user_data.get('political_inclination', []))
    context = user_data.get('context', '')
    name = user_data.get('name', 'Anonymous')
    
    # Smart prompt engineering with clear structure and constraints
    system_prompt = """You are an expert debate coach helping craft compelling rebuttals. Your responses must be:
- Plain text only (no headings, bullet points, or formatting)
- Concise but powerful (2-3 sentences maximum)
- Logically structured with strong evidence-based arguments
- Persuasive and confident in tone
- Appropriate for formal debate settings"""

    user_prompt = f"""Generate a strong rebuttal to this statement: "{statement_to_rebut}"

Context about the debater:
- Political inclinations: {political_leanings}
- Background context: {context}
- Name: {name}

Craft a rebuttal that aligns with their perspective while using solid logical reasoning and evidence. Focus on identifying weaknesses in the original statement and presenting a compelling counter-argument. Keep it concise and impactful."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error generating rebuttal: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form')
def show_form():
    return render_template('form.html')

@app.route('/submit_debate', methods=['POST'])
def submit_debate():
    try:
        name = request.form.get('name')
        political_inclination = request.form.getlist('political_inclination')
        context = request.form.get('context')
        
        submission = {
            'name': name,
            'political_inclination': political_inclination,
            'context': context
        }
        
        debate_submissions.append(submission)

        print(debate_submissions)
        
        return jsonify({
            'status': 'success',
            'message': 'Debate registration successful',
            'submission': submission
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/speak', methods=['POST'])
def speak():
    try:
        text = request.json.get('text')
        user_name = request.json.get('name')  # Optional: can specify which user's data to use
        
        if not text:
            return jsonify({
                'status': 'error',
                'message': 'No text provided for rebuttal'
            }), 400
        
        # Find user submission data
        user_data = find_user_submission(user_name)
        
        if not user_data:
            return jsonify({
                'status': 'error',
                'message': 'No user submission data found. Please fill out the form first.'
            }), 400
        
        # Generate rebuttal using OpenAI
        rebuttal = generate_debate_rebuttal(text, user_data)
        
        return jsonify({
            'status': 'success',
            'original_text': text,
            'rebuttal': rebuttal,
            'user_context': {
                'name': user_data.get('name'),
                'political_inclination': user_data.get('political_inclination')
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 