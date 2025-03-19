import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import jieba
import re
import os
from threading import Thread

# 在原文件顶部添加导出声明
__all__ = ['TextPreprocessor']  # 新增此行

class TextPreprocessor:
    def __init__(self):
        self.stopwords = set()
        self.load_stopwords('cn_stopwords.txt')
        
    def load_stopwords(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.stopwords = set(line.strip() for line in f)
        except FileNotFoundError:
            self.stopwords = set()

    def process_text(self, text):
        # 文本清洗
        text = re.sub(r'\s+', ' ', text)  # 合并连续空格
        text = re.sub(r'[^\w\u4e00-\u9fa5 ]', '', text)  # 去除非中文字符
        
        # 中文分词
        words = jieba.lcut(text)
        
        # 停用词过滤
        words = [w for w in words if w not in self.stopwords and len(w) > 1]
        
        # 段落重组（每5个词换行）
        processed = '\n'.join(' '.join(words[i:i+5]) for i in range(0, len(words), 5))
        
        return processed

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.preprocessor = TextPreprocessor()
        self.title("AI文本预处理工具")
        self.geometry("600x400")
        self.create_widgets()
        
    def create_widgets(self):
        # 文件选择区域
        self.file_frame = ttk.LabelFrame(self, text="源文件")
        self.file_entry = ttk.Entry(self.file_frame, width=50)
        self.browse_btn = ttk.Button(self.file_frame, text="浏览...", command=self.browse_file)
        
        # 处理进度条
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=500, mode='determinate')
        
        # 控制按钮
        self.start_btn = ttk.Button(self, text="开始处理", command=self.start_processing)
        self.save_btn = ttk.Button(self, text="保存结果", state=tk.DISABLED, command=self.save_result)
        
        # 布局
        self.file_frame.pack(pady=10)
        self.file_entry.pack(side=tk.LEFT, padx=5)
        self.browse_btn.pack(side=tk.RIGHT, padx=5)
        self.progress.pack(pady=10)
        self.start_btn.pack(pady=5)
        self.save_btn.pack(pady=5)
        
    def browse_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")])
        if filepath:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filepath)
            
    def start_processing(self):
        filepath = self.file_entry.get()
        if not os.path.exists(filepath):
            messagebox.showerror("错误", "文件不存在！")
            return
            
        self.progress['value'] = 0
        self.start_btn['state'] = tk.DISABLED
        Thread(target=self.run_processing, args=(filepath,)).start()
        
    def run_processing(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            processed = self.preprocessor.process_text(content)
            self.processed_content = processed
            self.progress['value'] = 100
            self.save_btn['state'] = tk.NORMAL
            messagebox.showinfo("完成", "文本处理完成！")
            
        except Exception as e:
            messagebox.showerror("处理错误", str(e))
        finally:
            self.start_btn['state'] = tk.NORMAL
            
    def save_result(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(self.processed_content)
            messagebox.showinfo("保存成功", "文件已保存！")

if __name__ == "__main__":
    app = Application()
    app.mainloop()