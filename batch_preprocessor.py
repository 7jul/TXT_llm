import jieba
import re
from text_preprocessor import TextPreprocessor
import os
from concurrent.futures import ThreadPoolExecutor

def batch_process(input_dir="txt", output_dir="LLM"):
    """批量处理文档的核心函数"""
    preprocessor = TextPreprocessor()
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    
    with ThreadPoolExecutor() as executor:
        for filename in files:
            try:
                input_path = os.path.join(input_dir, filename)
                new_name = f"{os.path.splitext(filename)[0]}_LLM.txt"
                output_path = os.path.join(output_dir, new_name)
                
                with open(input_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                processed = preprocessor.process_text(content)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(processed)
                
                print(f"成功处理：{filename} -> {new_name}")
            except Exception as e:
                print(f"处理失败[{filename}]: {str(e)}")

if __name__ == "__main__":
    os.makedirs("txt", exist_ok=True)
    os.makedirs("LLM", exist_ok=True)
    batch_process()
    print("批量处理完成！检查LLM文件夹获取结果")