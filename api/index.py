import json

def handler(request, response):
    """Simple test function to verify Vercel deployment works"""
    response.status = 200
    response.headers["Content-Type"] = "application/json"
    response.send(json.dumps({
        "message": "Smart School Portal API is working!",
        "status": "success",
        "timestamp": "2025-11-21"
    }))