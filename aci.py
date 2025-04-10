"""
Agent-Computer Interface
"""
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import tkinter.font as tkFont
# from agent import Agent

class TerminalExplanationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SWE-Agent")
        # root.attributes('-fullscreen', True)
        self.root.geometry("1800x1000")
        
        # Configure the main window to be responsive
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create a main frame to hold everything
        main_frame = ttk.Frame(root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Configure grid weights for the main frame
        main_frame.grid_columnconfigure(0, weight=2) 
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(3, weight=1)  
        
        # Create a label for the code section
        code_label = ttk.Label(main_frame, text="Code", font=("Arial", 12, "bold"))
        code_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        # Create a text widget for the code with a monospace font
        code_font = tkFont.Font(family="Courier", size=10)
        self.code_text = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD, 
            font=code_font, 
            bg="#2d2d2d", 
            fg="#ffffff",
            insertbackground="#ffffff"
        )
        self.code_text.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        
        # Terminal section
        terminal_label = ttk.Label(main_frame, text="Terminal", font=("Arial", 12, "bold"))
        terminal_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        self.terminal_text = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD, 
            font=code_font,  
            bg="#1e1e1e",   
            fg="#00ff00",   
            insertbackground="#00ff00"
        )
        self.terminal_text.grid(row=3, column=0, sticky="nsew")
        
        # Explanation section
        explanation_label = ttk.Label(main_frame, text="Explanation", font=("Arial", 12, "bold"))
        explanation_label.grid(row=0, column=1, sticky="w", pady=(0, 5), padx=(10, 0))
        self.explanation_text = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD, 
            font=("Arial", 10)
        )
        self.explanation_text.grid(row=1, column=1, rowspan=3, sticky="nsew", padx=(10, 0))
        
    
root = tk.Tk()
app = TerminalExplanationGUI(root)
# agent = Agent(alpha=0.5)
root.mainloop()