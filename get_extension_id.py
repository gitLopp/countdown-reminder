from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import json
import os
import sys

def get_extension_id():
    # 获取当前目录的绝对路径
    current_dir = os.path.abspath(os.path.dirname(__file__))
    
    # 设置 Edge 选项
    edge_options = Options()
    edge_options.add_argument('--headless')
    edge_options.add_argument(f'--load-extension={current_dir}')
    
    try:
        # 启动 Edge
        service = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=edge_options)
        
        # 等待扩展加载
        driver.implicitly_wait(2)
        
        # 获取扩展 ID
        extension_id = None
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if driver.current_url.startswith("ms-browser-extension://"):
                extension_id = driver.current_url.split('/')[2]
                break
        
        if extension_id:
            print(f"\n扩展 ID: {extension_id}")
            
            # 更新 generate_screenshots.py
            with open('generate_screenshots.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            updated_content = content.replace('[YOUR_EXTENSION_ID]', extension_id)
            updated_content = updated_content.replace('chrome-extension://', 'ms-browser-extension://')
            
            with open('generate_screenshots.py', 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print("已更新 generate_screenshots.py 中的扩展 ID")
        else:
            print("未能找到扩展 ID")
        
    except Exception as e:
        print(f"获取扩展 ID 时出错：{str(e)}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    get_extension_id() 