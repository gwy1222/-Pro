# -*- coding: utf-8 -*-
import jieba.analyse
from transformers import pipeline
import logging

class ResumeOptimizer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.rewriter = pipeline(
            "text2text-generation",
            model="Linly-AI/Chinese-LLaMA-2-7B-hf"
        )

    def generate_suggestions(self, resume_text, jd_text):
        try:
            # 提取JD关键词
            keywords = jieba.analyse.extract_tags(
                jd_text,
                topK=10,
                withWeight=False,
                allowPOS=('n', 'vn', 'eng'))
            # 生成优化建议
            prompt = f"优化以下简历以匹配职位要求:\n职位描述:{jd_text}\n当前简历:{resume_text[:1000]}"
            optimized = self.rewriter(
                prompt,
                max_length=512,
                do_sample=True,
                temperature=0.7
            )[0]['generated_text']
            
            return {
                "missing_keywords": keywords,
                "optimized_content": optimized
            }
        except Exception as e:
            self.logger.error(f"优化失败: {str(e)}")
            return {"missing_keywords": [], "optimized_content": ""}