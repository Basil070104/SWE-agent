import json
import os
from pathlib import Path
from typing import Any, List, Optional, Tuple, Union

class FileNotOpened(Exception):
    """Raised when no file is opened."""
    pass


class TextNotFound(Exception):
    """Raised when the text is not found in the window."""
    pass
  
def find_all(code: str, sub: str):
  start = 0
  while True:
    start = code.find(sub, start)
    if start == -1:
      return
    yield start
    start += len(sub)
    
class ReplacementInfo:
    def __init__(self, first_replaced_line: int, n_search_lines: int, n_replace_lines: int, n_replacements: int):
      self.first_replaced_line = first_replaced_line
      self.n_search_lines = n_search_lines
      self.n_replace_lines = n_replace_lines
      self.n_replacements = n_replacements

    def __repr__(self):
      return f"ReplacementInfo(first_replaced_line={self.first_replaced_line}, n_search_lines={self.n_search_lines}, n_replace_lines={self.n_replace_lines}, n_replacements={self.n_replacements})"


class InsertInfo:
  def __init__(self, first_inserted_line: int, n_lines_added: int):
    self.first_inserted_line = first_inserted_line
    self.n_lines_added = n_lines_added
    
  def __repr__(self):
    return f"InsertInfo(first_inserted_line={self.first_inserted_line}, n_lines_added={self.n_lines_added})"
  
class Window:
  def __init__(
    self,
    path: Optional[Path] = None,
    *,
    first_line: Optional[int] = None,
    window: Optional[int] = None,
    exception: bool = True
  ):
    self.path = Path(path)
    if not self.path.exists():
      msg = f"Error: File {self.path} not found"
      if exception:
        exit(1)
      raise FileNotFoundError(msg)
    
    if self.path.is_dir():
      msg = f"Error: {self.path} is a directory. You can only open files. Use cd or ls to navigate directories."
      if self._exit_on_exception:
          print(msg)
          exit(1)
      raise IsADirectoryError(msg)
    
    self.first_line = 0
    self._original_text= self.path.read_text()
    self._original_first_line = self.first_line
    self.window = 35
    self.text = self.path.read_text()

    @property
    def first_line(self) -> int:
        return self._first_line

    @first_line.setter
    def first_line(self, value: Union[int, float]):
        self._original_first_line = self.first_line
        value = int(value)
        self._first_line = max(0, min(value, self.n_lines - 1 - self.window))

    @property
    def text(self) -> str:
        return self.path.read_text()

    @text.setter
    def text(self, new_text: str):
        self._original_text = self.text
        self.path.write_text(new_text)

    @property
    def n_lines(self) -> int:
        return len(self.text.splitlines())

    @property
    def line_range(self) -> Tuple[int, int]:
        """Return first and last line (inclusive) of the display window, such
        that exactly `window` many lines are displayed.
        This means `line_range[1] - line_range[0] == window-1` as long as there are
        at least `window` lines in the file. `first_line` does the handling
        of making sure that we don't go out of bounds.
        """
        return self.first_line, min(self.first_line + self.window - 1, self.n_lines - 1)
      
  def get_window_text(
      self, *, line_numbers: bool = False, status_line: bool = False, pre_post_line: bool = False
  ) -> str:
      """Get the text in the current display window with optional status/extra information

      Args:
          line_numbers: include line numbers in the output
          status_line: include the status line in the output (file path, total lines)
          pre_post_line: include the pre/post line in the output (number of lines above/below)
      """
      start_line, end_line = [53,78]
      lines = self.text.split("\n")[start_line : end_line + 1]
      out_lines = []
      if status_line:
          # out_lines.append(f"[File: {self.path} ({self.n_lines} lines total)]")
          pass
      if pre_post_line:
          if start_line > 0:
              out_lines.append(f"({start_line} more lines above)")
      if line_numbers:
          out_lines.extend(f"{i + start_line + 1}:{line}" for i, line in enumerate(lines))
      else:
          out_lines.extend(lines)
      if pre_post_line:
          if end_line < self.n_lines - 1:
              # out_lines.append(f"({self.n_lines - end_line - 1} more lines below)")
              pass
      return "\n".join(out_lines)

    
if __name__ == "__main__":
  # positions = find_all("rebngvuierbnflaidenfalskjdfnasdufinasduifnas", "s")
  # print(next(positions))
  # print(next(positions))
  # test = ReplacementInfo(5,6,7,8)
  # print(test)
  # test = InsertInfo(5,5)
  # print(test)
  
  window = Window("aMUSED.py", first_line=50)
  lines = window.get_window_text(line_numbers=True, status_line=True, pre_post_line=False)
  print(lines)