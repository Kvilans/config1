from tkinter import Tk, Entry, END, WORD, BOTH, X
from tkinter.scrolledtext import ScrolledText
from emulator.emulator import ShellEmulator

class EmulatorGUI:
    def __init__(self, emulator):
        self.emulator = emulator
        self.window = Tk()
        self.window.title("Shell Emulator")

        self.text_area = ScrolledText(self.window, wrap=WORD)
        self.text_area.pack(padx=10, pady=10, fill=BOTH, expand=True)

        self.command_entry = Entry(self.window)
        self.command_entry.pack(padx=10, pady=10, fill=X)
        self.command_entry.bind("<Return>", self.on_enter)
        self.command_entry.focus_set()

    def on_enter(self, event):
        command = self.command_entry.get().strip()
        result = self.emulator.handle_command(command)
        self.text_area.insert(END, f"$ {command}\n{result}\n\n")
        self.text_area.see(END)
        self.command_entry.delete(0, END)

    def start(self):
        self.window.mainloop()
