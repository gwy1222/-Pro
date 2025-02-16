# -*- coding: utf-8 -*-
import pdfplumber
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba
import tkinter as tk
from tkinter import filedialog


#1.简历解析模块
def parse_resume(file_path):
    """PDF简历解析"""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# # 测试你的简历
my_resume = parse_resume("./data/my_resume/resume_gwy_20250214.pdf")
# print("简历解析成功！前100字：\n", my_resume[:200])

#2.职位描述处理
def analyze_jd(jd_text):
    """提取JD关键词"""
    # 中文分词
    jieba.enable_paddle()
    words = jieba.lcut(jd_text, use_paddle=True)
    
    # 计算TF-IDF
    tfidf = TfidfVectorizer(tokenizer=lambda x: jieba.lcut(x))
    tfidf.fit([jd_text])
    keywords = tfidf.get_feature_names_out()
    
    return keywords[:10]  # 返回TOP10关键词

# 示例测试
jd_sample = "需要熟练掌握Python和机器学习，有数据分析经验"
# print("JD关键词：", analyze_jd(jd_sample))

#匹配度计算
def calculate_score(resume, jd):
    """简易匹配度算法"""
    resume_words = set(jieba.lcut(resume))
    jd_words = set(jieba.lcut(jd))
    
    hit = len(resume_words & jd_words)
    total = len(jd_words)
    return round((hit / total) * 80, 1)  # 按PRD公式计算基础分

# 测试
# print(f"匹配度：{calculate_score(my_resume, jd_sample)}%")

#图形界面
class ResumeApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ResumeGPT v1.0")
        
        # 上传简历按钮
        btn_upload = tk.Button(self.window, text="上传简历", command=self.analyze, font=("微软雅黑", 12))
        btn_upload.pack(pady=10)
        
        # 结果显示区域
        self.result_text = tk.Text(self.window, height=15, width=60)
        self.result_text.pack()
    
    def analyze(self):
        """核心分析逻辑"""
        file_path = filedialog.askopenfilename()
        resume_text = parse_resume(file_path)
        jd_keywords = analyze_jd(jd_sample)
        score = calculate_score(resume_text, jd_sample)
        
        # 显示结果
        output = f"""=== 分析结果 ===
匹配度：{score}分
缺失关键词：{list(jd_keywords)[:3]}...
建议添加：Python量化项目经验、TensorFlow实战案例"""
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, output)

if __name__ == "__main__":
    app = ResumeApp()
    app.window.mainloop()


