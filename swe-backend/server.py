# Import flask and datetime module for showing date and time
from flask import Flask, request, jsonify
# from flask_socketio import SocketIO
from flask_cors import CORS
import datetime
from dataset import Dataset
from agent import Agent
import asyncio
import queue


x = datetime.datetime.now()

# Initializing flask app
app = Flask("SWE-agent")
CORS(app)

terminal_updates_queue = []

@app.route('/')
def root():

    return "Welcome to the SWE-agent server"
    
    
@app.route("/terminal_command")
def get_command():
    msg = {
        "command": "ls", 
        "status": "success" 
    }
    return msg

@app.route("/git_clone", methods=["POST"])
def git_clone():
    data = request.get_json() 
    url = data.get('url') 

    if not url:
        return {"status": "error", "message": "Missing URL"}, 400

    try:
        parts = url.split('/')
        owner = parts[-4] 
        repo = parts[-3].split('.')[0] 
        issue_number = parts[-1].split('/')[-1]
    except IndexError:
        return {"status": "error", "message": "Invalid URL format"}, 400
    
    print(owner, repo, issue_number)

    headers = {"Authorization": f"token {owner}"}
    
    directory = Dataset()
    
    terminal_updates_queue.append({
        'command': f"git clone {url}",
        'description': 'Cloning the repository to recreate the error/bug'
    })
    
    print(len(terminal_updates_queue))

    # Fetch issue data from GitHub
    result = asyncio.run(directory.pull(owner=owner, repo=repo, issue_number=issue_number)) 

    # print(result)
    status = "Good"
    return {"status": status, "data": result}, 200 

@app.route("/git_issue", methods=["POST"])
def git_issue():
    data = request.get_json() 
    url = data.get('url') 
    
    try:
        parts = url.split('/')
        owner = parts[-4] 
        repo = parts[-3].split('.')[0] 
        issue_number = parts[-1].split('/')[-1]
    except IndexError:
        return {"status": "error", "message": "Invalid URL format"}, 400

    if not url:
        return {"status": "error", "message": "Missing URL"}, 400
    
    directory = Dataset()
    
    terminal_updates_queue.append({
        'command': f"git get issue",
        'description': 'Scraping the Issue from the first occurrence.'
    })
    
    print(len(terminal_updates_queue))
    
    result = asyncio.run(directory.issue(owner=owner, repo=repo, issue_number=issue_number)) 

    status = "Good"
    
    return {"status": status, "data": result}, 200 

@app.route("/terminal_command", methods=["POST"])
def terminal_command_endpoint():
    data = request.get_json()
    command = data.get('command', 'ls')
    description = data.get('description')
    
    # Add command to queue to be processed
    terminal_updates_queue.append({
        'command': command, 'description': description })
    
    return jsonify({
        "message": f"Command '{command}' received and being processed",
        "status": "success"
    })

@app.route("/terminal_updates")
def get_terminal_updates():
    # This endpoint will be polled by the frontend to get the latest updates
    if terminal_updates_queue:  
        updates = terminal_updates_queue.pop() 
    else:
        updates = None 

    print(updates) 
    return jsonify(updates)  # Return the updates as JSON
    
# Running app
if __name__ == '__main__':
    app.run(debug=True)
