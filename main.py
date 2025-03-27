from dotenv import load_dotenv
from openai import OpenAI
import re
import subprocess

load_dotenv()

import os
api_key = os.getenv("openai_key")
# print(api_key)

agent = OpenAI(
  api_key=api_key
)

pattern = ""

def send_request():
  message_log = [
    {"role": "system", "content": "You are an efficient Python programmer that prioritizes writing code as quickly as possible. When the user requests code, provide only the code with no additional explanation or commentary in the fastest way possible. If only a single function is requested, include a main that takes the necessary arguments from command line and runs the function given those arguments. For all other inquiries or text inputs, respond at your own discretion, offering detailed information, insights, or assistance as needed."},
    {"role": "user", "content": "Write a program that determines the number of vowels in a sentence!"},
  ]

  completion = agent.chat.completions.create(
      model="gpt-4o-mini",
      messages = message_log
  )
  
  gpt_out = completion.choices[0].message.content
  
  print("ChatGPT: " + str(gpt_out))
  
def understand_file():
  extracted = ""
  with open("generated_files/test.py", "r") as file:
    content = file.read()
    match = re.search(r"```python\n(.*?)\n```", content, re.DOTALL)
    if match:
      extracted = match.group(1)
      print(extracted)
    
  message_log = [
    {"role": "system", "content": "You are an efficient Python debugger that tries to figure out what is wrong with the code. Please don't explain the fixes to the code."},
    {"role": "user", "content": content},
  ]
  
  completion = agent.chat.completions.create(
    model='gpt-4o-mini',
    messages=message_log
  )
  
  gpt_out = completion.choices[0].message.content
  
  print("ChatGPT: " + str(gpt_out))
  
# send_request()
# understand_file()
  

