#!/usr/bin/env python3
"""
Bob Hybrid - Works with both Socket Mode AND provides HTTP health endpoint for Cloud Run
Best of both worlds: Socket Mode for real-time + HTTP for Cloud Run health checks
"""

import os
import sys
import json
import logging
import threading
from datetime import datetime
from pathlib import Path
from flask import Flask, jsonify

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = Path('.env')
    if env_path.exists():
        load_dotenv()
except ImportError:
    pass

# Import the Firestore Bob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bob_firestore import BobFirestore

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('BobHybrid')

# Flask app for health checks
app = Flask(__name__)
bob_instance = None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Cloud Run"""
    global bob_instance
    if bob_instance:
        health = bob_instance.health_check()
        return jsonify(health), 200
    else:
        return jsonify({'status': 'initializing'}), 503

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        'service': 'Bob Hybrid (Socket Mode + HTTP)',
        'version': '1.0',
        'mode': 'socket_mode',
        'status': 'running'
    })

def run_flask():
    """Run Flask in a separate thread for health checks"""
    port = int(os.environ.get('PORT', 3000))
    logger.info(f"Starting HTTP server on port {port} for health checks")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def main():
    """Main entry point"""
    global bob_instance
    
    print("""
    ╔══════════════════════════════════════╗
    ║     BOB HYBRID EDITION v1.0          ║
    ║   Socket Mode + Cloud Run Ready      ║
    ║   Firestore + Vertex AI              ║
    ╚══════════════════════════════════════╝
    """)
    
    try:
        # Start Flask in a background thread for health checks
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        logger.info("✅ HTTP health check server started")
        
        # Start Bob with Socket Mode
        bob_instance = BobFirestore()
        logger.info("✅ Bob Firestore initialized")
        
        # Start Socket Mode connection
        bob_instance.start()
        
    except Exception as e:
        logger.error(f"❌ Failed to start Bob Hybrid: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())