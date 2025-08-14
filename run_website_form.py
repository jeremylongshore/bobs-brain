#!/usr/bin/env python3
"""
Standalone runner for website form integration service
This runs ONLY the form processing, not Bob Brain
"""

import os
import sys

# Add src directory to path
sys.path.insert(0, '/app/src')

# Import and run the website form integration app
from website_form_bigquery_integration import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)