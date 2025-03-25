from dotenv import load_dotenv
from openai import OpenAI
import os
import asyncio
from swerex.deployment.local import LocalDeployment
from swerex.runtime.abstract import CreateBashSessionRequest, BashAction, Command
import json

class Agent:
  
  def __init__(self, alpha) -> None:
    self.learning_rate = alpha
    load_dotenv()
    api_key = os.getenv("openai_key")
    self.agent = OpenAI(
      api_key=api_key
    )
    
  async def open(self, runtime, filename, line_number=None):
      
    print("Opening file...")
    
    cat_command = f"cat {filename}"
    result = await runtime.run_in_session(BashAction(
      command=cat_command
    ))
      
    
    if line_number is not None:
      await self.goto(deployment, line_number)
      
    return result
  
  async def goto(self, runtime, line_number):
    pass
  
  def scroll_down(self):
    pass
  
  def scroll_up(self):
    pass
    
  def search_file(self):
    pass
  
  def search_dir(self, runtime, dir_name):
    pass
  
  async def find_file(self, runtime, file_name, dir):

    print("Finding File...")
    
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
    
    # Use Vim commands to edit the file
    # output = await self.find_file(runtime, file, "generated_files")
    
    current = await runtime.run_in_session(BashAction(
      command="pwd"
    ))
    
    print(current.output)
    
    vim_commands = f""":{n},{m}d\ni\n{replacement_text}\n\\x1b\n:wq
    """
    
    vim_script = "vim_commands.txt"
    
    await runtime.run_in_session(BashAction(
        command=f"printf '{vim_commands}' > {vim_script}"
    ))
    
    # print(vim_commands)
  
    print("Executing Vim Commands...")
    
    result = await runtime.run_in_session(BashAction(
        command=f"vim -s {vim_script} {file}"
    ))
    
    print("Vim execution completed.")
  
    
    return True
    
  async def create(self, runtime, file_name):

    file = await runtime.run_in_session(BashAction(
      command=f"touch {file_name}"
    ))
    
    if file:
      print("Success")
    else:
      print("Fail")
    
    
  def submit(self):
    """ 
      submit request to Github or run code
    """
    
    
    pass
  
  async def think(self, runtime, file):
    
    output = await self.find_file(runtime, file, "generated_files")
    result = ""
    
    if output:
      result = await self.open(runtime, file)
    else:
      raise Exception("File was not found") 
    
    print(result.output)
    
    message_log = [
    {
        "role": "system",
        "content": """You are an efficient Python debugger that identifies issues in the provided code and suggests precise fixes. 

        **Instructions for output format:**  
        - Do not explain the fixes.  
        - Return the information in the following format:  
          
          {  
            "updates": [  
              { "n": X, "m": Y, "replacement": "corrected_code" },  
              { "n": A, "m": B, "replacement": "corrected_code" }  
            ]  
          }
          
        - `n` and `m` are the line numbers to be replaced.  
        - `replacement` contains the corrected code for those lines.  
        - Ensure the output structure remains consistent across responses.  
        """
    },
    {"role": "user", "content": result.output},
]

    completion = self.agent.chat.completions.create(
        model="gpt-4o-mini",
        messages = message_log
    )
    
    gpt_out = completion.choices[0].message.content
    
    print("ChatGPT: " + gpt_out)
    
    try:
      data = json.loads(str(gpt_out))
      updates = data.get("updates", [])
      for update in updates:
        n = update.get("n")
        m = update.get("m")
        replacement = update.get("replacement")
        print(f"Replace lines {n}-{m} with:\n{replacement}\n")
    except json.JSONDecodeError as e:
      print("Error parsing JSON:", e)
      
    print(replacement)
    
    await self.edit(runtime, file, n, m, replacement)
  
  async def listen(self):
    pass
  
deployment = LocalDeployment()
agent = Agent(alpha=0.5)
# asyncio.run(agent.open(deployment=deployment, path="generated_files/test.py"))
# asyncio.run(agent.find_file(deployment=deployment, dir="generated_files", file_name="test.py"))
# asyncio.run(agent.create(deployment=deployment, file_name="peek.py"))
asyncio.run(deployment.start())
runtime = deployment.runtime
asyncio.run(runtime.create_session(CreateBashSessionRequest()))
# asyncio.run(agent.edit(runtime=runtime, file="test.py", n=2, m=2, replacement_text="vowels = \"aeiouAEIOU\""))
asyncio.run(agent.think(runtime=runtime, file="test.py" ))
asyncio.run(deployment.stop())


