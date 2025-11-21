import json
import os

def handler(request, response):
    """Simple test function to verify Vercel deployment works"""
    # Get the request path
    path = request.path if hasattr(request, 'path') else '/'
    
    response.status = 200
    response.headers["Content-Type"] = "application/json"
    response.send(json.dumps({
        "message": "Smart School Portal API is working!",
        "path": path,
        "status": "success",
        "timestamp": "2025-11-21",
        "environment": dict(os.environ)
    }, indent=2))