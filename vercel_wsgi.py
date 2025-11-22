import os
import sys
from pathlib import Path

# Add project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

def handler(request, response):
    """Simple Vercel function to test deployment"""
    try:
        # Simple response without Django for now
        response.status = 200
        response.headers["Content-Type"] = "text/html"
        return [b"""
        <html>
        <head><title>Smart School Portal</title></head>
        <body>
            <h1>Smart School Portal is Deployed!</h1>
            <p>Your application is successfully deployed on Vercel.</p>
            <p><a href="/admin/">Go to Admin Panel</a></p>
            <p><a href="/dashboard/">Go to Dashboard</a></p>
        </body>
        </html>
        """]
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        
        response.status = 500
        response.headers["Content-Type"] = "text/plain"
        return [f"Error: {str(e)}".encode()]

# For Vercel compatibility
app = handler