"""
Image Combiner — entry point.
"""

import tkinter as tk
from gui import ImageCombinerApp


def main():
    root = tk.Tk()
    ImageCombinerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
