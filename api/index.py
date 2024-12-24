from flask import Flask, request, jsonify, render_template
import sys
import os

# Add parent directory to path so we can import from web
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.app import app

# This is required for Vercel
app.template_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'web', 'templates'))

# Required for Vercel serverless function
handler = app