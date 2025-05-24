from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Store debate submissions in memory (you might want to use a database in production)
debate_submissions = []

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
        # Here you can add any Python processing you need
        return jsonify({
            'status': 'success',
            'text': text
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 