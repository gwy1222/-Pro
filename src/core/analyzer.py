# -*- coding: utf-8 -*-
from transformers import BertTokenizer, BertModel
import torch
import numpy as np
import logging

class ResumeAnalyzer:
    def __init__(self, model_path="bert-base-chinese"):
        self.logger = logging.getLogger(__name__)
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertModel.from_pretrained(model_path)
        self.model.eval()  # 设置为评估模式

    def get_embeddings(self, text):
        try:
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            )
            with torch.no_grad():
                outputs = self.model(**inputs)
            return torch.mean(outputs.last_hidden_state, dim=1).numpy()
        except Exception as e:
            self.logger.error(f"Embedding生成失败: {str(e)}")
            return np.zeros((1, 768))

    def calculate_similarity(self, resume_text, jd_text):
        try:
            resume_vec = self.get_embeddings(resume_text)
            jd_vec = self.get_embeddings(jd_text)
            similarity = np.dot(resume_vec, jd_vec.T)[0][0] * 100
            return round(similarity, 2)
        except Exception as e:
            self.logger.error(f"相似度计算失败: {str(e)}")
            return 0.0