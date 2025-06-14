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