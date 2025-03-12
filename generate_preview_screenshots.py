from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import os

def setup_driver():
    edge_options = Options()
    edge_options.add_argument('--headless')
    edge_options.add_argument('--window-size=1280,800')
    edge_options.add_argument('--hide-scrollbars')
    edge_options.add_argument('--force-device-scale-factor=1')
    
    service = Service(EdgeChromiumDriverManager().install())
    return webdriver.Edge(service=service, options=edge_options)

def take_screenshot(driver, filename, width=1280, height=800):
    driver.set_window_size(width, height)
    time.sleep(1)
    
    # 确保 store-assets 目录存在
    os.makedirs('store-assets', exist_ok=True)
    
    # 保存截图
    driver.save_screenshot(f'store-assets/{filename}')
    print(f'已保存截图：{filename}')

def capture_preview_screenshots():
    print("开始生成预览截图...")
    driver = setup_driver()
    
    try:
        # 获取当前目录的绝对路径
        current_dir = os.path.abspath(os.path.dirname(__file__))
        preview_url = f'file://{current_dir}/store-assets/preview.html'
        
        # 生成空白状态截图
        print("正在生成空白状态截图...")
        driver.get(preview_url)
        driver.execute_script("document.getElementById('empty-state').style.display = 'block';")
        driver.execute_script("document.getElementById('add-form').style.display = 'none';")
        driver.execute_script("document.getElementById('with-events').style.display = 'none';")
        take_screenshot(driver, 'screenshot1_empty.png')
        
        # 生成添加事件表单截图
        print("正在生成添加事件表单截图...")
        driver.execute_script("document.getElementById('empty-state').style.display = 'none';")
        driver.execute_script("document.getElementById('add-form').style.display = 'block';")
        driver.execute_script("document.getElementById('with-events').style.display = 'none';")
        take_screenshot(driver, 'screenshot2_add_event.png')
        
        # 生成包含事件的状态截图
        print("正在生成包含事件的状态截图...")
        driver.execute_script("document.getElementById('empty-state').style.display = 'none';")
        driver.execute_script("document.getElementById('add-form').style.display = 'none';")
        driver.execute_script("document.getElementById('with-events').style.display = 'block';")
        take_screenshot(driver, 'screenshot3_with_event.png')
        
        print("截图生成完成！")
        print("截图文件保存在 store-assets 目录中：")
        print("1. screenshot1_empty.png - 空白主界面")
        print("2. screenshot2_add_event.png - 添加事件界面")
        print("3. screenshot3_with_event.png - 包含事件的主界面")
        
    except Exception as e:
        print(f"生成截图时出错：{str(e)}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    capture_preview_screenshots() 