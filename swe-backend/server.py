# Import flask and datetime module for showing date and time
from flask import Flask, request
from flask_cors import CORS
import datetime


x = datetime.datetime.now()

# Initializing flask app
app = Flask("SWE-agent")
CORS(app)

@app.route('/')
def root():

    return "Welcome to the SWE-agent server"
    
@app.route('/data')
def get_time():

    # Returning an api for showing in  reactjs
    return {
        'Name':"geek", 
        "Age":"22",
        "Date":x, 
        "programming":"python"
        }
    
@app.route("/terminal_command")
def get_command():
    msg = {
        "command": "ls", 
        "status": "success" 
    }
    return msg

@app.route("/git_issue", methods=["POST"])
def git_issue():
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

    # Fetch issue data from GitHub
    issue_data = request.get(f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}", headers=headers).json()
    
    status = "Good" if issue_data else "Not Found"
    print(issue_data)
    return {"status": status, "data": issue_data}, 200  # Return the issue data

# Running app
if __name__ == '__main__':
    app.run(debug=True)
