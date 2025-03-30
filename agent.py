"""RL Agent to train in a coding env

Returns:
    None: 
"""

from dotenv import load_dotenv
from openai import OpenAI
import os
import asyncio
from swerex.deployment.local import LocalDeployment
from swerex.runtime.abstract import CreateBashSessionRequest, BashAction, Command
import json
import sys
import logging
from type import Agent
import logging.config
from pathlib import Path
from window import Window

class Agent:
  
  def __init__(self, alpha) -> None:
    self.learning_rate = alpha
    load_dotenv()
    api_key = os.getenv("openai_key")
    self.agent = OpenAI(
      api_key=api_key
    )
    logging.basicConfig(filename="temp.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    logging.config.fileConfig('temp.conf')
    self.logger = logging.getLogger("agent")
    
  async def open(self, runtime, filename, line_number=None):
      
    self.logger.debug("Opening file...")
    
    cat_command = f"cat {filename}"
    result = await runtime.run_in_session(BashAction(
      command=cat_command
    ))
      
    
    if line_number is not None:
      await self.goto(runtime, line_number)
      
    return result
  
  async def goto(self, window: Window, line_number):
    window.goto(line=line_number)
    self.logger.info(f"Went to line {line_number}")
    return
  
  def scroll_down(self, window: Window, lines: int):
    window.scroll(n_lines=lines)
    self.logger.info(f"Scrolled down {lines}")
    return
  
  def scroll_up(self, window: Window, lines: int):
    window.scroll(n_lines=-lines)
    self.logger.info(f"Scrolled up {lines}")
    return
  
  def search_dir(self, runtime, dir_name):
    pass
  
  async def find_file(self, runtime, file_name):

    self.logger.debug("Finding File...")
    
    find = await runtime.run_in_session(BashAction(
      command=f"find . -name {file_name}"
    ))
    
    find_arr = find.output.split("/")
    
    dir_list = ""
    if len(find_arr) == 2:
      file = find_arr[1]
      self.logger.debug("Found")
      return True
    else:
      cd_command = f"cd {dir}"
      cd_response = await runtime.run_in_session(BashAction(
        command=cd_command
      ))
      self.logger.debug(f"Changed directory: {cd_response.output}")
      
      
    files = await runtime.run_in_session(BashAction(
      command="ls"
    ))
    
    # print(type(files.output))
    
    result = files.output
    result = result.split()
    print(result)
    
    if file_name in result:
      self.logger.debug("Found")
      return True
    
    self.logger.error("Not Found")
    return False
      
    
  
  async def edit(self, runtime, file, n, m, replacement_text):
    
    current = await runtime.run_in_session(BashAction(
      command="pwd"
    ))
    
    return True
    
  async def create(self, runtime, file_name):

    file = await runtime.run_in_session(BashAction(
      command=f"touch {file_name}"
    ))
    
    if file:
      self.logger.debug("Success")
    else:
      self.logger.error("Fail")
    
    
  def submit(self):
    """ 
      submit request to Github or run code
    """
    
    pass

  
  async def think(self, runtime, file):
    
    output = await self.find_file(runtime, file)
    result = ""
    
    window = Window(path=file, first_line=1) if output else None
    if window is None:
      self.logger.error("File did not open") 
    else:
      self.logger.info("File opened successfully")
    
    # window.print_window()
    text = window.get_window_text(line_numbers=True)
    # print(result.output)
    
    self.logger.info("Thinking...")
    
    message_log = [
      {
          "role": "system",
          "content": """You are an efficient Python debugger that identifies issues in the provided code and suggests precise fixes. 

          **Instructions for output format:**  
          - Do not explain the fixes.  
          - The First line is line number 1
          - Return the information in the following format:  
            
            {  
              "updates": [  
                { "search": X, "replacement": "corrected_code" },  
                { "search": Y, "replacement": "corrected_code" }  
              ]  
            }
            
          - 'search' is the code that needs to be replaced -> can be multilined
          - `replacement` contains the corrected code for those lines.  
          - Ensure the output structure remains consistent across responses.  
          """
      },
      {"role": "user", "content": text}
    ]

    completion = self.agent.chat.completions.create(
        model="gpt-4o-mini",
        messages = message_log
    )
    
    gpt_out = completion.choices[0].message.content
    
    # print("ChatGPT: " + gpt_out)
    
    try:
      data = json.loads(str(gpt_out))
      updates = data.get("updates", [])
      
      if not updates:
        self.logger.info("No updates Found.")
        return
      
      for update in updates:
        search = update.get("search")
        replacement = update.get("replacement")
        self.logger.info(f"Replace lines {search} with: {replacement}")
    except json.JSONDecodeError as e:
      self.logger.error("Error parsing JSON:", e)
      
    # print(type(replacement))
    
    self.logger.info("Editing...")
    
    window.replace_in_window(search=search, replace=replacement, reset_first_line="keep")
    
    # await self.edit(runtime, file, n, m, replacement)
    
    return 
  
  async def listen(self):
    pass
  
def main(file):
  deployment = LocalDeployment()
  agent = Agent(alpha=0.5)
  # asyncio.run(agent.open(deployment=deployment, path="generated_files/test.py"))
  # asyncio.run(agent.find_file(deployment=deployment, dir="generated_files", file_name="test.py"))
  # asyncio.run(agent.create(deployment=deployment, file_name="peek.py"))
  asyncio.run(deployment.start())
  runtime = deployment.runtime
  asyncio.run(runtime.create_session(CreateBashSessionRequest()))
  # asyncio.run(agent.edit(runtime=runtime, file="test.py", n=2, m=2, replacement_text="vowels = \"aeiouAEIOU\""))
  asyncio.run(agent.think(runtime=runtime, file=file))
  asyncio.run(deployment.stop())

if __name__ == "__main__":
  main(sys.argv[1])
