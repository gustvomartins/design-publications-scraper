#!/usr/bin/env python3
"""
Entry point para a interface Streamlit do Design Publications Scraper.
Este script executa a interface web para busca manual de publicações.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

if __name__ == "__main__":
    # Run Streamlit app
    import streamlit.web.cli as stcli
    
    # Set Streamlit configuration
    os.environ['STREAMLIT_SERVER_PORT'] = '8501'
    os.environ['STREAMLIT_SERVER_ADDRESS'] = 'localhost'
    
    # Run the Streamlit app using the standalone file
    sys.argv = [
        "streamlit", "run", 
        "streamlit_app.py",
        "--server.port=8501",
        "--server.address=localhost"
    ]
    
    sys.exit(stcli.main())
