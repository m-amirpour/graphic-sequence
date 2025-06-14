"""
Graph Theory Project - Main Entry Point
Author: Muhammad Mahdi Amirpour (m-amirpour)
Created at: 2025-06-14 10:29:51 UTC
"""

import tkinter as tk
from gui import GraphSequenceGUI

def main():
    """
    Main entry point of the application.
    Creates and runs the GUI application.
    """
    root = tk.Tk()
    app = GraphSequenceGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()