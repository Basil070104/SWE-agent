# Import flask and datetime module for showing date and time
from flask import Flask, request, jsonify
# from flask_socketio import SocketIO
from flask_cors import CORS
import datetime
from dataset import Dataset
from agent import Agent
import asyncio
import queue
from swerex.deployment.local import LocalDeployment
from swerex.runtime.abstract import CreateBashSessionRequest
import logging


x = datetime.datetime.now()

# Initializing flask app
app = Flask("SWE-agent")
CORS(app)

terminal_updates_queue = []
window_queue = []
cloned_repo = ""  
logger = logging.getLogger("SWE-agent")

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

@app.route("/modify_file", methods=["POST"])
async def modify_file():
    data = request.get_json() 
    title = data.get('title_issue') 
    body = data.get('body_issue')
    dir = data.get('dir_find')
    # print(title, body, dir)
    
    deployment = LocalDeployment(logger=logger)
    await deployment.start()
    runtime = deployment.runtime
    await runtime.create_session(CreateBashSessionRequest())
    model = Agent(alpha=0.5)
    print("Modifying file")
    terminal_updates_queue.append({
        'command': f"ls -R {dir}/", 'description': "Finding all relevant file paths in the project"
    })
    cloned_repo = dir
    file = await model.modify(runtime=runtime, title=title, body=body, dir=dir)
    print("Agent is thinking...")
    terminal_updates_queue.append({
        'command': f"agent.thinking >>>", 'description': "The agent is finding the solution to the bug"
    })
    
    fix = await model.think(runtime=runtime, dir=dir, file=file, window_out=window_queue)
    terminal_updates_queue.append({
        'command': f"agent.finished >>>", 'description': """The agent has fixed the bug. Look in the editor for more information. \nYou agree to:Use the Agent only for lawful purposes;\nEnsure you have the right to clone and modify any repository you provide;\nNot use the Agent to introduce or propagate malicious code;\nMonitor any modifications made by the Agent before deploying them in production environments.
        """
    })
    print("end")
    await deployment.stop()
    print("end2")
    return {"status": "success", "message": fix}
    

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
        updates = terminal_updates_queue.pop(0) 
    else:
        updates = None 
    return jsonify(updates)  # Return the updates as JSON

@app.route("/editor_updates")
def get_editor_updates():
    # This endpoint will be polled by the frontend to get the latest updates
    if window_queue:  
        updates = window_queue.pop(0) 
    else:
        updates = None 
    return jsonify(updates)  # Return the updates as JSON
    
# Running app
if __name__ == '__main__':
    app.run(debug=False)
