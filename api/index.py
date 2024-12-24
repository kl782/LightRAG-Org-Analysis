from flask import Flask, request, jsonify, render_template
import sys
import os
from pathlib import Path

app = Flask(__name__)

# Set template folder - make it absolute from the api directory
template_dir = str(Path(__file__).resolve().parent.parent / 'web' / 'templates')
app.template_folder = template_dir

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze_company', methods=['POST'])
def analyze_company():
    try:
        data = request.json
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
            
        # For now, just return a test response
        return jsonify({
            'status': 'success',
            'message': 'API endpoint working',
            'received_url': data['url']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Required for Vercel
app = app.wsgi_app
