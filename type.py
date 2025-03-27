from pydantic import BaseModel
from typing_extensions import TypedDict
from typing import Any, Literal

class UserProfile(BaseModel):
  name: str
  age: int
  email: str

class Agent(TypedDict, total=False):
  # same as `APIStats` from models.py
  model_stats: dict[str, float]
  exit_status: str | None
  submission: str | None
  # same as `ReviewerResult`
  review: dict[str, Any]
  edited_files30: str
  edited_files50: str
  edited_files70: str
  # only if summarizer is used
  summarizer: dict
  swe_agent_hash: str
  swe_agent_version: str
  swe_rex_version: str
  swe_rex_hash: str
  
