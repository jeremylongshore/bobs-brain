#!/usr/bin/env python3
"""
StartAI Tools - Portfolio & Dashboard with Login
Complete web app with authentication and document upload
"""

from flask import Flask, render_template_string, request, redirect, session, jsonify, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from google.cloud import storage, bigquery
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Configure login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# File upload config
UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'csv', 'json', 'md'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Simple user store (in production, use database)
users = {
    'jeremy': {
        'id': '1',
        'username': 'jeremy',
        'password': generate_password_hash('StartAI2025!'),  # Change this password!
        'email': 'jeremy@startaitools.com'
    }
}

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    for username, user_data in users.items():
        if user_data['id'] == user_id:
            return User(user_data['id'], username, user_data['email'])
    return None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# HTML Templates
LANDING_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jeremy Longshore - StartAI Tools Portfolio</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .nav {
            background: rgba(255,255,255,0.95);
            padding: 20px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .logo {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }
        
        .nav-links {
            display: flex;
            gap: 30px;
            align-items: center;
        }
        
        .nav-links a {
            color: #333;
            text-decoration: none;
            transition: color 0.3s;
        }
        
        .nav-links a:hover {
            color: #667eea;
        }
        
        .social-section {
            background: #1a1a2e;
            padding: 60px 40px;
            text-align: center;
            color: white;
        }
        
        .social-links {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 30px;
            flex-wrap: wrap;
        }
        
        .social-link {
            color: white;
            text-decoration: none;
            padding: 12px 24px;
            border: 2px solid white;
            border-radius: 30px;
            transition: all 0.3s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        
        .social-link:hover {
            background: white;
            color: #1a1a2e;
            transform: translateY(-3px);
        }
        
        .projects-section {
            background: #f8f9fa;
            padding: 80px 40px;
        }
        
        .projects-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .project-card {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        
        .project-card:hover {
            transform: translateY(-10px);
        }
        
        .project-header {
            background: linear-gradient(135deg, #667eea, #764ba2);
            padding: 20px;
            color: white;
        }
        
        .project-content {
            padding: 25px;
        }
        
        .tech-stack {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
        }
        
        .tech-tag {
            background: #e2e8f0;
            color: #2d3748;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 14px;
        }
        
        .login-btn {
            background: #667eea;
            color: white;
            padding: 10px 25px;
            border-radius: 25px;
            text-decoration: none;
            transition: all 0.3s;
        }
        
        .login-btn:hover {
            background: #5a67d8;
            transform: translateY(-2px);
        }
        
        .hero {
            padding: 100px 40px;
            text-align: center;
            color: white;
        }
        
        .hero h1 {
            font-size: 48px;
            margin-bottom: 20px;
            animation: fadeInUp 0.8s;
        }
        
        .hero p {
            font-size: 20px;
            margin-bottom: 40px;
            opacity: 0.9;
            animation: fadeInUp 0.8s 0.2s both;
        }
        
        .cta-buttons {
            display: flex;
            gap: 20px;
            justify-content: center;
            animation: fadeInUp 0.8s 0.4s both;
        }
        
        .cta {
            padding: 15px 35px;
            border-radius: 30px;
            text-decoration: none;
            font-size: 18px;
            transition: all 0.3s;
            display: inline-block;
        }
        
        .cta-primary {
            background: white;
            color: #667eea;
        }
        
        .cta-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .cta-secondary {
            background: transparent;
            color: white;
            border: 2px solid white;
        }
        
        .cta-secondary:hover {
            background: white;
            color: #667eea;
        }
        
        .features {
            background: white;
            padding: 80px 40px;
            text-align: center;
        }
        
        .features h2 {
            font-size: 36px;
            color: #333;
            margin-bottom: 50px;
        }
        
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 40px;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .feature-card {
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
        }
        
        .feature-icon {
            font-size: 48px;
            margin-bottom: 20px;
        }
        
        .feature-card h3 {
            color: #333;
            margin-bottom: 15px;
        }
        
        .feature-card p {
            color: #666;
            line-height: 1.6;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .stats {
            background: #f8f9fa;
            padding: 60px 40px;
            text-align: center;
        }
        
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 40px;
            max-width: 800px;
            margin: 0 auto;
        }
        
        .stat {
            padding: 20px;
        }
        
        .stat-number {
            font-size: 42px;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            color: #666;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <nav class="nav">
        <div class="logo">🚀 StartAI Tools</div>
        <div class="nav-links">
            <a href="#features">Features</a>
            <a href="#about">About</a>
            <a href="#contact">Contact</a>
            <a href="/login" class="login-btn">Login to Dashboard</a>
        </div>
    </nav>
    
    <section class="hero">
        <h1>Jeremy Longshore</h1>
        <h2 style="font-size: 32px; margin: 20px 0; font-weight: normal;">AI-Powered Equipment Intelligence</h2>
        <p>Creator of Bob's Brain • Full-Stack Developer • AI/ML Engineer</p>
        <div class="cta-buttons">
            <a href="/login" class="cta cta-primary">Access Bob's Brain Dashboard</a>
            <a href="#projects" class="cta cta-secondary">View My Projects</a>
        </div>
    </section>
    
    <section class="features" id="features">
        <h2>Powerful Features</h2>
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <h3>Bob's Brain AI</h3>
                <p>Intelligent diagnostic assistant that learns from every interaction, providing instant equipment troubleshooting</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h3>Knowledge Graph</h3>
                <p>Neo4j-powered relationship mapping between equipment, error codes, parts, and solutions</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📡</div>
                <h3>Live Data Scraping</h3>
                <p>Continuously learns from YouTube, Reddit, forums, and technical bulletins</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📈</div>
                <h3>ML Pipeline</h3>
                <p>Upload documents and research to train Bob with your specific equipment knowledge</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💰</div>
                <h3>Cost Analysis</h3>
                <p>Real repair costs from actual cases, helping you make informed decisions</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔧</div>
                <h3>Part Finder</h3>
                <p>Instant access to part numbers, prices, and compatibility information</p>
            </div>
        </div>
    </section>
    
    <section class="projects-section" id="projects">
        <h2 style="font-size: 36px; text-align: center; margin-bottom: 50px;">🚀 Featured Projects</h2>
        <div class="projects-grid">
            <div class="project-card">
                <div class="project-header">
                    <h3>🤖 Bob's Brain - AI Assistant</h3>
                </div>
                <div class="project-content">
                    <p>Intelligent equipment diagnostic system powered by Gemini 2.5 Flash. Learns from real repair data and provides instant troubleshooting.</p>
                    <div class="tech-stack">
                        <span class="tech-tag">Python</span>
                        <span class="tech-tag">Gemini AI</span>
                        <span class="tech-tag">Neo4j</span>
                        <span class="tech-tag">BigQuery</span>
                        <span class="tech-tag">Cloud Run</span>
                    </div>
                </div>
            </div>
            
            <div class="project-card">
                <div class="project-header">
                    <h3>🔍 Diagnostic Pro MVP3</h3>
                </div>
                <div class="project-content">
                    <p>Complete vehicle diagnostic platform with real-time error code lookup, repair cost estimates, and technician knowledge base.</p>
                    <div class="tech-stack">
                        <span class="tech-tag">React</span>
                        <span class="tech-tag">TypeScript</span>
                        <span class="tech-tag">Firebase</span>
                        <span class="tech-tag">REST API</span>
                    </div>
                </div>
            </div>
            
            <div class="project-card">
                <div class="project-header">
                    <h3>📡 Unified Scraper System</h3>
                </div>
                <div class="project-content">
                    <p>Automated data collection from 40+ sources including YouTube, Reddit, forums. Uses yt-dlp, PRAW, and custom scrapers.</p>
                    <div class="tech-stack">
                        <span class="tech-tag">Python</span>
                        <span class="tech-tag">yt-dlp</span>
                        <span class="tech-tag">PRAW</span>
                        <span class="tech-tag">BeautifulSoup</span>
                        <span class="tech-tag">Async</span>
                    </div>
                </div>
            </div>
            
            <div class="project-card">
                <div class="project-header">
                    <h3>🔗 Neo4j Knowledge Graph</h3>
                </div>
                <div class="project-content">
                    <p>Graph database with 258+ nodes mapping relationships between equipment, error codes, parts, and solutions.</p>
                    <div class="tech-stack">
                        <span class="tech-tag">Neo4j</span>
                        <span class="tech-tag">Cypher</span>
                        <span class="tech-tag">GraphQL</span>
                        <span class="tech-tag">Python</span>
                    </div>
                </div>
            </div>
            
            <div class="project-card">
                <div class="project-header">
                    <h3>🔄 Circle of Life ML</h3>
                </div>
                <div class="project-content">
                    <p>Continuous learning pipeline that improves Bob's responses using feedback loops and BigQuery ML models.</p>
                    <div class="tech-stack">
                        <span class="tech-tag">BigQuery ML</span>
                        <span class="tech-tag">TensorFlow</span>
                        <span class="tech-tag">Python</span>
                        <span class="tech-tag">Cloud Pub/Sub</span>
                    </div>
                </div>
            </div>
            
            <div class="project-card">
                <div class="project-header">
                    <h3>💬 Slack Integration</h3>
                </div>
                <div class="project-content">
                    <p>Real-time Slack bot integration allowing team collaboration with Bob's Brain for instant equipment diagnostics.</p>
                    <div class="tech-stack">
                        <span class="tech-tag">Slack API</span>
                        <span class="tech-tag">WebSockets</span>
                        <span class="tech-tag">Flask</span>
                        <span class="tech-tag">OAuth</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="social-section">
        <h2 style="font-size: 36px; margin-bottom: 20px;">Connect With Me</h2>
        <p style="font-size: 18px; opacity: 0.9;">Let's build something amazing together</p>
        <div class="social-links">
            <a href="https://diagnosticpro.io" target="_blank" class="social-link">
                🔧 DiagnosticPro.io
            </a>
            <a href="https://jeremylongshore.com" target="_blank" class="social-link">
                🌐 jeremylongshore.com
            </a>
            <a href="https://linkedin.com/in/jeremylongshore" target="_blank" class="social-link">
                💼 LinkedIn
            </a>
            <a href="https://twitter.com/jeremylongshore" target="_blank" class="social-link">
                🐦 X (Twitter)
            </a>
            <a href="https://github.com/jeremylongshore" target="_blank" class="social-link">
                💻 GitHub
            </a>
            <a href="https://upwork.com/freelancers/jeremylongshore" target="_blank" class="social-link">
                💰 Upwork Profile
            </a>
        </div>
    </section>
    
    <section class="stats">
        <h2 style="font-size: 36px; text-align: center; margin-bottom: 40px; color: #333;">Bob's Brain Statistics</h2>
        <div class="stat-grid">
            <div class="stat">
                <div class="stat-number">258+</div>
                <div class="stat-label">Knowledge Nodes</div>
            </div>
            <div class="stat">
                <div class="stat-number">38</div>
                <div class="stat-label">Error Codes</div>
            </div>
            <div class="stat">
                <div class="stat-number">40+</div>
                <div class="stat-label">Data Sources</div>
            </div>
            <div class="stat">
                <div class="stat-number">24/7</div>
                <div class="stat-label">AI Available</div>
            </div>
            <div class="stat">
                <div class="stat-number">< $30</div>
                <div class="stat-label">Monthly Cost</div>
            </div>
            <div class="stat">
                <div class="stat-number">99.95%</div>
                <div class="stat-label">Uptime</div>
            </div>
        </div>
    </section>
    
    <footer style="background: #2c3e50; color: white; text-align: center; padding: 30px;">
        <p>© 2025 Jeremy Longshore | StartAI Tools | Built with ❤️ and AI</p>
        <p style="margin-top: 10px; opacity: 0.8;">Powered by Google Cloud Platform • Gemini 2.5 Flash • Neo4j</p>
    </footer>
</body>
</html>
"""

LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - StartAI Tools</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            width: 100%;
            max-width: 400px;
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .login-header h1 {
            color: #333;
            margin-bottom: 10px;
        }
        
        .login-header p {
            color: #666;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 500;
        }
        
        input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .login-btn {
            width: 100%;
            padding: 14px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        .login-btn:hover {
            background: #5a67d8;
        }
        
        .error {
            color: #e53e3e;
            margin-top: 10px;
            text-align: center;
        }
        
        .back-link {
            text-align: center;
            margin-top: 20px;
        }
        
        .back-link a {
            color: #667eea;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <h1>🚀 StartAI Tools</h1>
            <p>Login to your dashboard</p>
        </div>
        
        <form method="POST" action="/login">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit" class="login-btn">Login</button>
            
            {% if error %}
            <div class="error">{{ error }}</div>
            {% endif %}
        </form>
        
        <div class="back-link">
            <a href="/">← Back to home</a>
        </div>
    </div>
</body>
</html>
"""

DASHBOARD_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - StartAI Tools</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f7fa;
        }
        
        .sidebar {
            position: fixed;
            left: 0;
            top: 0;
            width: 250px;
            height: 100vh;
            background: #2c3e50;
            padding: 20px;
        }
        
        .sidebar h2 {
            color: white;
            margin-bottom: 30px;
        }
        
        .sidebar-menu {
            list-style: none;
        }
        
        .sidebar-menu li {
            margin-bottom: 15px;
        }
        
        .sidebar-menu a {
            color: #ecf0f1;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            border-radius: 5px;
            transition: background 0.3s;
        }
        
        .sidebar-menu a:hover {
            background: #34495e;
        }
        
        .main-content {
            margin-left: 250px;
            padding: 20px;
        }
        
        .header {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .welcome {
            font-size: 24px;
            color: #333;
        }
        
        .logout-btn {
            background: #e74c3c;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            transition: background 0.3s;
        }
        
        .logout-btn:hover {
            background: #c0392b;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .card h3 {
            color: #333;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .upload-section {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 30px;
        }
        
        .upload-zone {
            border: 2px dashed #cbd5e0;
            border-radius: 10px;
            padding: 40px;
            text-align: center;
            transition: border-color 0.3s;
        }
        
        .upload-zone:hover {
            border-color: #667eea;
        }
        
        .upload-btn {
            background: #667eea;
            color: white;
            padding: 12px 30px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            font-size: 16px;
            margin-top: 20px;
        }
        
        .upload-btn:hover {
            background: #5a67d8;
        }
        
        .file-input {
            display: none;
        }
        
        .neo4j-btn {
            background: #48bb78;
            color: white;
            padding: 15px 30px;
            border-radius: 8px;
            text-decoration: none;
            display: inline-block;
            margin: 10px 10px 10px 0;
            transition: background 0.3s;
        }
        
        .neo4j-btn:hover {
            background: #38a169;
        }
        
        .stat-number {
            font-size: 36px;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }
        
        .stat-label {
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>🚀 StartAI Tools</h2>
        <ul class="sidebar-menu">
            <li><a href="#dashboard">📊 Dashboard</a></li>
            <li><a href="#upload">📤 Upload Documents</a></li>
            <li><a href="#neo4j">🔗 Neo4j Graph</a></li>
            <li><a href="#bob">🤖 Bob's Brain</a></li>
            <li><a href="#scrapers">📡 Scrapers</a></li>
            <li><a href="#analytics">📈 Analytics</a></li>
        </ul>
    </div>
    
    <div class="main-content">
        <div class="header">
            <div class="welcome">Welcome, {{ current_user.username }}! 👋</div>
            <a href="/logout" class="logout-btn">Logout</a>
        </div>
        
        <div class="dashboard-grid">
            <div class="card">
                <h3>📊 System Status</h3>
                <div class="stat-number">Active</div>
                <div class="stat-label">All systems operational</div>
            </div>
            
            <div class="card">
                <h3>🔗 Knowledge Nodes</h3>
                <div class="stat-number">258</div>
                <div class="stat-label">Equipment, codes, parts</div>
            </div>
            
            <div class="card">
                <h3>📡 Data Sources</h3>
                <div class="stat-number">40+</div>
                <div class="stat-label">YouTube, Reddit, Forums</div>
            </div>
        </div>
        
        <div class="upload-section" id="upload">
            <h3>📤 Upload Documents to Bob's Brain</h3>
            <p style="color: #666; margin-bottom: 20px;">Upload PDFs, documents, or research papers to enhance Bob's knowledge</p>
            
            <div class="upload-zone">
                <form id="upload-form" method="POST" action="/upload" enctype="multipart/form-data">
                    <div>
                        <svg width="64" height="64" style="fill: #cbd5e0; margin-bottom: 20px;">
                            <use href="#upload-icon"></use>
                        </svg>
                    </div>
                    <p style="color: #666; margin-bottom: 10px;">Drag & drop files here or click to browse</p>
                    <p style="color: #999; font-size: 14px;">Supports: PDF, TXT, DOC, DOCX, CSV, JSON, MD</p>
                    <input type="file" id="file-input" name="file" class="file-input" multiple>
                    <button type="button" class="upload-btn" onclick="document.getElementById('file-input').click()">
                        Choose Files
                    </button>
                </form>
            </div>
            
            <div id="upload-status"></div>
        </div>
        
        <div class="card" id="neo4j">
            <h3>🔗 Neo4j Knowledge Graph</h3>
            <p style="color: #666; margin-bottom: 20px;">Access your equipment knowledge graph</p>
            
            <a href="https://console.neo4j.io" target="_blank" class="neo4j-btn">
                Open Neo4j Console
            </a>
            <a href="#" onclick="showQueries()" class="neo4j-btn" style="background: #ed8936;">
                Sample Queries
            </a>
            
            <div style="margin-top: 20px; padding: 15px; background: #f7fafc; border-radius: 8px;">
                <strong>Quick Stats:</strong><br>
                • 15 Equipment models<br>
                • 38 Error codes<br>
                • 20 Parts with prices<br>
                • 35 Common problems<br>
                • Connected relationships
            </div>
        </div>
    </div>
    
    <script>
        // File upload handling
        document.getElementById('file-input').addEventListener('change', function(e) {
            const files = e.target.files;
            if (files.length > 0) {
                const formData = new FormData();
                for (let i = 0; i < files.length; i++) {
                    formData.append('files', files[i]);
                }
                
                fetch('/upload', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('upload-status').innerHTML = 
                        '<div style="color: green; margin-top: 20px;">✅ ' + data.message + '</div>';
                })
                .catch(error => {
                    document.getElementById('upload-status').innerHTML = 
                        '<div style="color: red; margin-top: 20px;">❌ Upload failed</div>';
                });
            }
        });
        
        function showQueries() {
            alert(`Sample Neo4j Queries:
            
1. Find all equipment:
   MATCH (e:Equipment) RETURN e

2. Error codes for Ford trucks:
   MATCH (e:Equipment)-[:THROWS_CODE]->(c:ErrorCode)
   WHERE e.brand = 'Ford'
   RETURN e.model, c.code, c.description

3. Expensive parts (>$1000):
   MATCH (p:Part) WHERE p.price > 1000 
   RETURN p ORDER BY p.price DESC`);
        }
    </script>
</body>
</html>
"""

# Routes
@app.route('/')
def home():
    return LANDING_PAGE

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and check_password_hash(users[username]['password'], password):
            user = User(users[username]['id'], username, users[username]['email'])
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return render_template_string(LOGIN_PAGE, error='Invalid username or password')
    
    return render_template_string(LOGIN_PAGE)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template_string(DASHBOARD_PAGE)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    uploaded_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            uploaded_files.append(filename)
            
            # Here you would process the file and add to Bob's knowledge
            # For now, just save it
            
    return jsonify({
        'message': f'Successfully uploaded {len(uploaded_files)} files',
        'files': uploaded_files
    })

@app.route('/api/stats')
@login_required
def get_stats():
    # Return current system stats
    return jsonify({
        'nodes': 258,
        'error_codes': 38,
        'parts': 20,
        'equipment': 15,
        'data_sources': 40
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)