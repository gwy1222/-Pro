# -*- coding: utf-8 -*-
import pdfplumber
from docx import Document
import re
import os
import logging

class ResumeParser:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.section_pattern = re.compile(
            r'(教育经历|工作经历|项目经历|技能|Education|Work Experience).*?\n(.*?)(?=\n[^。！？]+\n|$)',
            re.DOTALL
        )

    def parse(self, file_path):
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在: {file_path}")
            
            if file_path.endswith('.pdf'):
                return self._parse_pdf(file_path)
            elif file_path.endswith('.docx'):
                return self._parse_docx(file_path)
            else:
                raise ValueError("仅支持PDF/DOCX格式")
        except Exception as e:
            self.logger.error(f"解析失败: {str(e)}")
            return ""

    def _parse_pdf(self, path):
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def _parse_docx(self, path):
        doc = Document(path)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

    def extract_sections(self, text):
        sections = {}
        for match in self.section_pattern.finditer(text):
            title = match.group(1).strip()
            content = match.group(2).strip()
            sections[title] = content
        return sections