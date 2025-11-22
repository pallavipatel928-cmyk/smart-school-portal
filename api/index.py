import json

def handler(request, response):
    """Simple API endpoint for Vercel"""
    response.status = 200
    response.headers["Content-Type"] = "application/json"
    response.send(json.dumps({
        "message": "Smart School Portal API is working!",
        "status": "success",
        "version": "1.0"
    }))