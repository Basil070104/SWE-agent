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
    # self.deployment = LocalDeployment()
    # asyncio.run(self.deployment.start())
    # self.runtime = self.deployment.runtime
    
    
  async def open(self, runtime, filename, line_number=None):
      
    self.logger.debug("Opening file...")
    
    cat_command = f"cat {filename}"
    result = await runtime.run_in_session(BashAction(
      command=cat_command
    ))
      
    
    if line_number is not None:
      await self.goto(runtime, line_number)
      
    return result.output
  
  #actions the agent can do
  
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
  
  async def find_file(self, runtime, dir, file_name):
    self.logger.debug("Finding File...")

    # Use the provided directory in the find command
    find_command = f"find {dir} -name {file_name}"
    find = await runtime.run_in_session(BashAction(command=find_command))

    # Check if the find command returned any results
    if find.output:
        find_arr = find.output.splitlines()  # Split by lines to get each found file

        # Log and return if the file is found
        for file in find_arr:
            self.logger.debug(f"Found file: {file}")
            return await self.open(runtime=runtime, filename=file), file

    self.logger.error("File not found in the specified directory.")
    return False, None
      
    
  
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

  async def modify(self, runtime, title: str, body: str, dir: str):
    result = await runtime.run_in_session(BashAction(
      command=f"ls -R {dir}/"
    ))
    
    content = {"title" : title, "body" : body, "dir_info" : result.output}
    json_content = json.dumps(content)
    
    # print(json_content)
    
    self.logger.info("Figuring out which file to modify...")
    
    message_log = [
      {
          "role": "system",
          "content": """ You are trying to figure out from this github issue which file we need to modify
          in this directory. Only return the file name.
          """
      },
      {"role": "user", "content": json_content}
    ]
    
    completion = self.agent.chat.completions.create(
        model="gpt-4o-mini",
        messages = message_log
    )
    
    gpt_out = completion.choices[0].message.content
    
    # print(gpt_out)
    self.logger.info(f"File to be modified is: {gpt_out}")
    
    return gpt_out
  
  async def think(self, runtime, dir, file, window_out: list):
    
    output, path = await self.find_file(runtime, dir, file)
    result = ""
    window = Window(path=path, first_line=1) if output else None
    if window is None:
      self.logger.error("File did not open") 
    else:
      self.logger.info("File opened successfully")
      
    
    # window.print_window()
    text = window.get_window_text(line_numbers=True)
    out = window.get_window_text(line_numbers=False)
    window_out.append({'text': out, 'file' : file})
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
    print("before")
    completion = self.agent.chat.completions.create(
        model="gpt-4o-mini",
        messages = message_log
    )
    print("here")
    gpt_out = completion.choices[0].message.content
    
    print("ChatGPT: " + gpt_out)
    
    try:
      data = json.loads(str(gpt_out))
      updates = data.get("updates", [])
      
      if not updates:
        self.logger.info("Your command ran successfully and did not produce any output.")
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
    
    out = window.get_window_text()
    window_out.append({'text': out, 'file': file})
    
    # await self.edit(runtime, file, n, m, replacement)
    return gpt_out
  
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
  # asyncio.run(agent.think(runtime=runtime, dir="tmp3exlaa_r", file=file))
  asyncio.run(agent.modify(runtime=runtime, title="vowel file", body="the vowels file is not working correctly", dir="tmp3exlaa_r"))
  # asyncio.run(agent.find_file(runtime=runtime, dir="tmp3exlaa_r", file_name=file))
  # print(result)
  asyncio.run(deployment.stop())

if __name__ == "__main__":
  main(sys.argv[1])
