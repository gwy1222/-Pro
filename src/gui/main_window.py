# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog
from .components import JDEditor, ResumePreview

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ResumeGPT Pro")
        self.root.geometry("1000x700")
        
        # 左侧面板
        self.left_panel = ttk.Frame(self.root, width=300)
        self.btn_upload = ttk.Button(
            self.left_panel,
            text="上传简历",
            command=self._upload_resume
        )
        self.jd_editor = JDEditor(self.left_panel)
        
        # 右侧面板
        self.right_panel = ttk.Notebook(self.root)
        self.resume_preview = ResumePreview(self.right_panel)
        self.suggestion_tab = ttk.Frame(self.right_panel)
        
        # 布局
        self._setup_layout()
        
        # 状态变量
        self.resume_text = ""
        self.jd_text = ""

    def _setup_layout(self):
        self.left_panel.pack(side="left", fill="y", padx=10, pady=10)
        self.btn_upload.pack(fill="x", pady=5)
        self.jd_editor.pack(fill="both", expand=True)
        
        self.right_panel.pack(side="right", fill="both", expand=True)
        self.right_panel.add(self.resume_preview, text="简历预览")
        self.right_panel.add(self.suggestion_tab, text="优化建议")

    def _upload_resume(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF/DOCX", "*.pdf *.docx")]
        )
        if file_path:
            from core.parser import ResumeParser
            parser = ResumeParser()
            self.resume_text = parser.parse(file_path)
            self.resume_preview.update_content(self.resume_text, [])