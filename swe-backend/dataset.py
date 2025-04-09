import os
from dotenv import load_dotenv
import asyncio
from swerex.deployment.local import LocalDeployment
from swerex.runtime.abstract import CreateBashSessionRequest, BashAction, Command
import requests
import tempfile
import subprocess
import json

class Dataset:
  
  def __init__(self) -> None:
    load_dotenv()
    self.github_token = os.getenv("github_token")
    if not self.github_token:
      raise ValueError("GitHub token not found in environment variables")
    
  async def pull(self, owner, repo, issue_number=None):
    """
    Pull a GitHub repository and optionally fetch issue information
    
    Args:
        owner (str): GitHub repository owner/organization
        repo (str): Repository name
        issue_number (int, optional): Issue number to fetch information about
    
    Returns:
        dict: Repository information and path to the cloned repository
    """
    # Create a temporary directory for cloning
    temp_dir = tempfile.mkdtemp(dir=os.getcwd())
    
    # Set up headers for GitHub API requests
    headers = {
        "Authorization": f"token {self.github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Get repository information
    repo_url = f"https://api.github.com/repos/{owner}/{repo}"
    print(repo)
    # repo_response = requests.get(repo_url, headers=headers)
    
    # if repo_response.status_code != 200:
    #     raise Exception(f"Failed to get repository info: {repo_response.text}")
    
    # repo_data = repo_response.json()
    
    # Get issue information if provided
    issue_data = None
    if issue_number:
        issue_url = f"{repo_url}/issues/{issue_number}"
        issue_response = requests.get(issue_url, headers=headers)
        
        if issue_response.status_code == 200:
            issue_data = issue_response.json()
    
    # Create local deployment
    deployment = LocalDeployment()
    await deployment.start()
    runtime = deployment.runtime
    # Create bash session
    await runtime.create_session(CreateBashSessionRequest())
    
    # Clone the repository
    clone_url = f"https://{self.github_token}@github.com/{owner}/{repo}.git"
    clone_command = f"git clone {clone_url} {temp_dir}"
    
    result = await runtime.run_in_session(BashAction(command=clone_command))
    
    if result.exit_code != 0:
      await deployment.stop()
      raise Exception(f"Failed to clone repository: {result.stderr}")
    
    await deployment.stop()
    return {
        # "repo_info": repo_data,
        "issue_info": issue_data,
        "repo_path": f"Repository Path : {temp_dir}"
    }
    
  async def issue(self, owner, repo, issue_number):
    """
    Fetch details of a specific GitHub issue

    Args:
        owner (str): GitHub repository owner/organization
        repo (str): Repository name
        issue_number (int or str): Issue number to fetch

    Returns:
        dict: Issue data as a JSON object
    """

    deployment = LocalDeployment()
    await deployment.start()
    runtime = deployment.runtime

    # Create bash session
    await runtime.create_session(CreateBashSessionRequest())

    # Construct the curl command
    issue_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    # issue_url = "https://api.github.com/repos/octocat/Hello-World/issues/1"
    curl_command = (
        f'curl -L '
        f'-H "Accept: application/vnd.github+json" '
        f'-H "Authorization: Bearer {self.github_token}" '
        f'-H "X-GitHub-Api-Version: 2022-11-28" '
        f'{issue_url}'
    )

    result = await runtime.run_in_session(BashAction(command=curl_command))

    await deployment.stop()

    if result.exit_code != 0:
        raise Exception(f"Failed to fetch issue: {result.stderr}")

    output= result.model_dump_json()
    modify = json.loads(output)
    return modify["output"]

    

async def main():
    # Example usage
    dataset = Dataset()
    # result = await dataset.pull("Basil070104", "test_bed")
    # print(f"Repository cloned to: {result['repo_path']}")
    result = await dataset.issue("Basil070104", "test_bed", "1")
    print(result["output"])

if __name__ == "__main__":
    asyncio.run(main())