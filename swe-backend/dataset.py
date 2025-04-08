import os
from dotenv import load_dotenv
import asyncio
from swerex.deployment.local import LocalDeployment
from swerex.runtime.abstract import CreateBashSessionRequest, BashAction, Command
import requests
import tempfile

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
    temp_dir = tempfile.mkdtemp(dir=os.getcwd())
    
    # Set up headers for GitHub API requests
    headers = {
        "Authorization": f"token {self.github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Get repository information
    repo_url = f"https://api.github.com/repos/{owner}/{repo}"
    repo_response = requests.get(repo_url, headers=headers)
    
    if repo_response.status_code != 200:
        raise Exception(f"Failed to get repository info: {repo_response.text}")
    
    repo_data = repo_response.json()
    
    # Get issue information if provided
    issue_data = None
    if issue_number:
        issue_url = f"{repo_url}/issues/{issue_number}"
        issue_response = requests.get(issue_url, headers=headers)
        
        if issue_response.status_code == 200:
            issue_data = issue_response.json()
    
    deployment = LocalDeployment()
    await deployment.start()
    runtime = deployment.runtime
    session = await runtime.create_session(CreateBashSessionRequest())
    clone_url = f"https://{self.github_token}@github.com/{owner}/{repo}.git"
    clone_command = f"git clone {clone_url} {temp_dir}"
    
    result = await runtime.run_in_session(BashAction(command=clone_command))
    
    if result.exit_code != 0:
      await deployment.stop()
      raise Exception(f"Failed to clone repository: {result.stderr}")
    
    await deployment.stop()
    return {
      "repo_info": repo_data,
      "issue_info": issue_data,
      "repo_path": temp_dir
    }

async def main():
    # Example usage
    dataset = Dataset()
    result = await dataset.pull("Basil070104", "test_bed")
    print(f"Repository cloned to: {result['repo_path']}")

if __name__ == "__main__":
    asyncio.run(main())