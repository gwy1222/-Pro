# -*- coding: utf-8 -*-
import sys
import os
# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from gui.main_window import MainWindow
from utils.logger import setup_logging
from core.analyzer import ResumeAnalyzer
from core.optimizer import ResumeOptimizer
import logging

class Application:
    def __init__(self):
        setup_logging()
        self.logger = logging.getLogger(__name__)
        self.main_window = MainWindow()
        self.analyzer = ResumeAnalyzer()
        self.optimizer = ResumeOptimizer()
        
        # 绑定事件
        self.main_window.jd_editor.text.bind("<<Modified>>", self._realtime_update)
        
    def _realtime_update(self, event=None):
        jd_text = self.main_window.jd_editor.get_text()
        if jd_text:
            similarity = self.analyzer.calculate_similarity(
                self.main_window.resume_text,
                jd_text
            )
            self.main_window.update_score(similarity)

if __name__ == "__main__":
    app = Application()
    app.main_window.root.mainloop()