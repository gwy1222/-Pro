# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

class JDEditor(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.text = tk.Text(
            self,
            wrap="word",
            font=("Microsoft YaHei", 10),
            height=10
        )
        scroll = ttk.Scrollbar(self, command=self.text.yview)
        self.text.configure(yscrollcommand=scroll.set)
        
        self.text.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def get_text(self):
        return self.text.get("1.0", "end-1c")

class ResumePreview(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.text = tk.Text(
            self,
            wrap="none",
            font=("Microsoft YaHei", 10),
            undo=True
        )
        self.text.tag_configure("highlight", foreground="red")
        
        scroll_x = ttk.Scrollbar(self, orient="horizontal", command=self.text.xview)
        scroll_y = ttk.Scrollbar(self, command=self.text.yview)
        self.text.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        
        self.text.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def update_content(self, text, keywords):
        self.text.delete("1.0", "end")
        self.text.insert("1.0", text)
        for word in keywords:
            start = "1.0"
            while True:
                pos = self.text.search(word, start, stopindex="end")
                if not pos:
                    break
                end = f"{pos}+{len(word)}c"
                self.text.tag_add("highlight", pos, end)
                start = end