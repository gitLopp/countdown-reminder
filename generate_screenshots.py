from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import os
import json
import hashlib

def generate_temp_extension_id():
    # 读取 manifest.json
    with open('manifest.json', 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    
    # 使用 manifest 的关键信息生成一个稳定的 ID
    key_info = f"{manifest['name']}_{manifest['version']}_{manifest['description']}"
    return hashlib.md5(key_info.encode()).hexdigest()[:32]

def setup_driver():
    edge_options = Options()
    edge_options.add_argument('--headless')
    edge_options.add_argument('--window-size=1280,800')
    edge_options.add_argument('--hide-scrollbars')
    edge_options.add_argument('--force-device-scale-factor=1')
    
    # 获取当前目录
    current_dir = os.path.abspath(os.path.dirname(__file__))
    edge_options.add_argument(f'--load-extension={current_dir}')
    
    service = Service(EdgeChromiumDriverManager().install())
    return webdriver.Edge(service=service, options=edge_options)

def take_screenshot(driver, filename, width=1280, height=800):
    driver.set_window_size(width, height)
    time.sleep(2)  # 增加等待时间确保页面完全加载
    
    # 确保 store-assets 目录存在
    os.makedirs('store-assets', exist_ok=True)
    
    # 保存截图
    driver.save_screenshot(f'store-assets/{filename}')
    print(f'已保存截图：{filename}')

def capture_extension_screenshots():
    print("开始生成扩展商店截图...")
    
    # 生成临时扩展 ID
    extension_id = generate_temp_extension_id()
    print(f"使用临时扩展 ID: {extension_id}")
    
    driver = setup_driver()
    
    try:
        # 生成空白事件列表的截图
        print("正在生成主界面截图...")
        driver.get(f'ms-browser-extension://{extension_id}/popup.html')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "eventList"))
        )
        take_screenshot(driver, 'screenshot1_empty.png')
        
        # 添加示例事件
        print("正在添加示例事件...")
        add_button = driver.find_element(By.ID, "addEventButton")
        add_button.click()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "eventForm"))
        )
        
        # 填写并提交表单
        name_input = driver.find_element(By.ID, "eventName")
        date_input = driver.find_element(By.ID, "eventDate")
        
        name_input.send_keys("春节")
        date_input.send_keys("2025-02-10")
        
        # 保存添加事件界面的截图
        take_screenshot(driver, 'screenshot2_add_event.png')
        
        # 提交表单
        submit_button = driver.find_element(By.ID, "submitButton")
        submit_button.click()
        
        # 等待事件显示
        time.sleep(2)
        
        # 保存包含事件的主界面截图
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
    capture_extension_screenshots() 