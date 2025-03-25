from dotenv import load_dotenv
from openai import OpenAI
import os
import asyncio
from swerex.deployment.local import LocalDeployment
from swerex.runtime.abstract import CreateBashSessionRequest, BashAction, Command



class Agent:
  
  def __init__(self, alpha) -> None:
    self.learning_rate = alpha
    load_dotenv()
    api_key = os.getenv("openai_key")
    self.agent = OpenAI(
      api_key=api_key
    )
    
  async def open(self, runtime, path: str, line_number=None):
    
    path_list = path.split("/")
    directory = "/".join(path_list[:-1])
    filename = path_list[-1]
    # print(path_list)
    
    current = await runtime.run_in_session(BashAction(
      command="pwd"
    ))
    # print(current.output)
    
    if directory:
      cd_command = f"cd {directory}"
      cd_response = await runtime.run_in_session(BashAction(
        command=cd_command
      ))
      print(f"Changed directory: {cd_response.output}")
      
    cat_command = f"cat {filename}"
    result = await runtime.run_in_session(BashAction(
      command=cat_command
    ))
      
    # print(result.output)
    
    if line_number is not None:
      await self.goto(deployment, line_number)
      
    return result
  
  async def goto(self, deployment, line_number):
    pass
  
  def scroll_down(self):
    pass
  
  def scroll_up(self):
    pass
    
  def search_file(self):
    pass
  
  def search_dir(self):
    pass
  
  async def find_file(self, runtime, file_name, dir):

    current = await runtime.run_in_session(BashAction(
      command="pwd"
    ))
    
    dir_list = ""
    if dir:
      cd_command = f"cd {dir}"
      cd_response = await runtime.run_in_session(BashAction(
        command=cd_command
      ))
      print(f"Changed directory: {cd_response.output}")
      
      
    files = await runtime.run_in_session(BashAction(
      command="ls"
    ))
    
    print(type(files.output))
    
    result = files.output
    result = result.split()
    print(result)
    
    if file_name in result:
      print("Found")
      return True
    
    print("Not Found")
    return False
      
    # await deployment.stop()
    
  async def edit(self, runtime, file, n, m, replacement_text):
    """
    Edit a file by replacing lines n through m with replacement_text
    
    Args:
        runtime: The runtime environment
        file: The file to edit
        n: Starting line number
        m: Ending line number
        replacement_text: Text to insert
    """
    # First check if we're in the right directory
    current = await runtime.run_in_session(BashAction(
        command="pwd"
    ))
    print(f"Current directory: {current.output.strip()}")
    
    # Create a temporary file with the vim commands
    escaped_text = replacement_text.replace("'", "'\\''")
    
    # Format the vim script correctly:
    # 1. Move to line n
    # 2. Delete m-n+1 lines
    # 3. Enter insert mode
    # 4. Add replacement text
    # 5. Exit insert mode and save
    vim_script = f"""
      :{n}
      :{n},{m}d
      i
      {escaped_text}
      ^[
      :wq
    """ 
    
    # The ^[ is a literal ESC character which needs to be handled specially
    vim_script = vim_script.replace("^[", "\x1B")
    
    # Write the vim script to a temporary file
    script_path = "/tmp/vim_commands.txt"
    await runtime.run_in_session(BashAction(
        command=f"cat > {script_path} << \n{vim_script}\nEOT"
    ))
    
    print(f"Created vim script at {script_path}")
    
    # Execute vim with the script
    print(f"Editing file: {file}")
    result = await runtime.run_in_session(BashAction(
        command=f"vim -s {script_path} {file}"
    ))
    
    # Check if vim executed successfully
    if result.exit_code == 0:
        print("File edited successfully")
    else:
        print(f"Error editing file: {result.output}")
    
    # Clean up the temporary script
    await runtime.run_in_session(BashAction(
        command=f"rm {script_path}"
    ))
    
    return result.exit_code == 0
  
  # async def edit(self, runtime, file, n, m, replacement_text):
    
  #   # Use Vim commands to edit the file
  #   output = await self.find_file(runtime, file, "generated_files")
    
  #   current = await runtime.run_in_session(BashAction(
  #     command="pwd"
  #   ))
    
  #   print(current.output)
    
  #   vim_commands = f"""
  #   {n},{m}d
  #   i
  #   {replacement_text}
  #   :wq
  #   """
    
  #   vim_script = "vim_commands.txt"
    
  #   await runtime.run_in_session(BashAction(
  #       command=f"printf '{vim_commands}' > {vim_script}"
  #   ))
    
  #   print(vim_commands)
    
  #   # vim_commands = [
  #   #     f"{n},{m}d",  # Delete lines n through m
  #   #     "i",          # Enter insert mode
  #   #     replacement_text,  # Add the replacement text
  #   #     "\x1b",       # Exit insert mode (ESC key)
  #   #     ":wq"         # Save and quit
  #   # ]
  
  #   print("Executing Vim Commands...")
    
  #   if os.path.exists(vim_script):
  #     print(f"{vim_script} exists.")
  #   else:
  #     print(f"{vim_script} does not exist.")
    
  #   result = await runtime.run_in_session(BashAction(
  #       command=f"vim -s {vim_script} {file}"
  #   ))
    
  #   print("Vim execution completed.")
    
  #   await runtime.run_in_session(BashAction(
  #       command=f"rm {vim_script}"
  #   ))
    
  #   return True
    
  async def create(self, runtime, file_name):

    file = await runtime.run_in_session(BashAction(
      command=f"touch {file_name}"
    ))
    
    if file:
      print("Success")
    else:
      print("Fail")
    
    
  def submit(self):
    pass
  
  def think(self):
    pass
  
deployment = LocalDeployment()
agent = Agent(alpha=0.5)
# asyncio.run(agent.open(deployment=deployment, path="generated_files/test.py"))
# asyncio.run(agent.find_file(deployment=deployment, dir="generated_files", file_name="test.py"))
# asyncio.run(agent.create(deployment=deployment, file_name="peek.py"))
asyncio.run(deployment.start())
runtime = deployment.runtime
asyncio.run(runtime.create_session(CreateBashSessionRequest()))
asyncio.run(agent.edit(runtime=runtime, file="test.py", n=2, m=3, replacement_text="vowels = \"aeiouAEIOU\""))
asyncio.run(deployment.stop())


