import tkinter as tk
from tkinter import filedialog, font, ttk

class Notepad(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Notepad")
        self.geometry("800x600")
        self.file = None

        self.text = tk.Text(self, undo=True, wrap="word")
        self.text.pack(expand=True, fill="both")

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        self.menu.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(self.menu, tearoff=0)
        edit_menu.add_command(label="Cut", command=lambda: self.text.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.text.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.text.event_generate("<<Paste>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Undo", command=lambda: self.text.event_generate("<<Undo>>"))
        edit_menu.add_command(label="Redo", command=lambda: self.text.event_generate("<<Redo>>"))
        self.menu.add_cascade(label="Edit", menu=edit_menu)

        self.wrap_var = tk.BooleanVar(value=True)
        view_menu = tk.Menu(self.menu, tearoff=0)
        view_menu.add_checkbutton(label="Word Wrap", variable=self.wrap_var, command=self.toggle_wrap)
        self.menu.add_cascade(label="View", menu=view_menu)

        self.font_family = tk.StringVar(value="Arial")
        self.font_size = tk.IntVar(value=12)

        toolbar = tk.Frame(self)
        ttk.Combobox(toolbar, textvariable=self.font_family, values=font.families(), width=15)\
            .pack(side=tk.LEFT, padx=2)
        ttk.Combobox(toolbar, textvariable=self.font_size, values=list(range(8, 41)), width=3)\
            .pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Apply Font", command=self.apply_font).pack(side=tk.LEFT, padx=2)
        toolbar.pack(fill=tk.X)

    def apply_font(self):
        self.text.config(font=(self.font_family.get(), self.font_size.get()))

    def new_file(self):
        self.file = None
        self.text.delete("1.0", tk.END)

    def open_file(self):
        file = filedialog.askopenfilename()
        if file:
            self.file = file
            with open(file, "r") as f:
                self.text.delete("1.0", tk.END)
                self.text.insert("1.0", f.read())

    def save_file(self):
        if not self.file:
            self.save_as()
        else:
            with open(self.file, "w") as f:
                f.write(self.text.get("1.0", tk.END))

    def save_as(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt")
        if file:
            self.file = file
            self.save_file()

    def toggle_wrap(self):
        self.text.config(wrap="word" if self.wrap_var.get() else "none")

if __name__ == "__main__":
    Notepad().mainloop()
