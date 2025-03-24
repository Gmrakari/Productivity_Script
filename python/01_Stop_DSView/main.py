
# 根据条件自动停止DSView

# pip3 install pywinauto
# pip3 install pyautogui

import os
import time
from pywinauto import Application
from datetime import datetime
import pyautogui

def capture_screen():
    try:
        time.sleep(2)
        screenshot = pyautogui.screenshot()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        save_folder = os.path.join(script_dir, '01_screenshot')
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        now = datetime.now()
        timestamp= now.strftime("%Y%m%d-%H%M%S%f")[:-3]
        save_path = os.path.join(save_folder, f"{timestamp}.jpg")

        screenshot.save(save_path)
        print(f" save jpg: {save_path}")
    except Exception as e:
        print(f" error: {e}")

def get_current_time():
    """获取当前时间并格式化为字符串，包含毫秒"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # 截取前 3 位毫秒

def check_dsview_path(dsview_path):
    """检查 DSView 路径是否存在"""
    if not os.path.exists(dsview_path):
        print(f"{get_current_time()} - 错误: 路径不存在 - {dsview_path}")
        return False
    else:
        print(f"{get_current_time()} - 路径存在: {dsview_path}")
        return True

def connect_to_dsview(dsview_path):
    """连接到 DSView 应用程序"""
    try:
        # 如果 DSView 未运行，先启动它
        if not Application(backend='uia').connect(path=dsview_path):
            print(f"{get_current_time()} - DSView 未运行，正在启动...")
            app = Application(backend='uia').start(dsview_path)
        else:
            app = Application(backend='uia').connect(path=dsview_path)
        print(f"{get_current_time()} - 连接成功")
        return app
    except Exception as e:
        print(f"{get_current_time()} - 连接失败: {e}")
        return None

def find_and_click_button(window, button_title):
    """查找并点击指定标题的按钮"""
    try:
        button = window.child_window(title_re=f".*{button_title}.*", control_type="Button")
        button.click()
        print(f"{get_current_time()} - {button_title} 按钮点击成功")
        return True
    except Exception as e:
        print(f"{get_current_time()} - 找不到 {button_title} 按钮: {e}")
        return False

def check_button_state(window, button_title):
    """检查按钮的状态"""
    try:
        button = window.child_window(title_re=f".*{button_title}.*", control_type="Button")
        if button.is_enabled():  # 检查按钮是否可用
            print(f"{get_current_time()} - {button_title} 按钮状态: 可用")
            return True
        else:
            print(f"{get_current_time()} - {button_title} 按钮状态: 不可用")
            return False
    except Exception as e:
        # print(f"{get_current_time()} - 检查 {button_title} 按钮状态时出错: {e}")
        return False

def stop_dsview_collect():
    """停止 DSView 数据采集"""
    # DSView 可执行文件路径
    dsview_path = r'C:\Software\DSView\DSView.exe'

    # 检查路径是否存在
    if not check_dsview_path(dsview_path):
        return

    # 连接到 DSView
    app = connect_to_dsview(dsview_path)
    if not app:
        return

    # 获取 DSView 窗口
    dsview_window = app.window(title_re=".*DSView.*")
    dsview_window.set_focus()

    capture_screen()

    time.sleep(15)

    # 查找并点击停止按钮
    find_and_click_button(dsview_window, "停止")

    capture_screen()

def start_dsview_collect():
    """启动 DSView 数据采集"""
    # DSView 可执行文件路径
    dsview_path = r'C:\Software\DSView\DSView.exe'

    # 检查路径是否存在
    if not check_dsview_path(dsview_path):
        return

    # 连接到 DSView
    app = connect_to_dsview(dsview_path)
    if not app:
        return

    # 获取 DSView 窗口
    dsview_window = app.window(title_re=".*DSView.*")
    dsview_window.set_focus()

    time.sleep(2)

    # 检查按钮状态
    if check_button_state(dsview_window, "开始"):
        # 如果“开始”按钮可用，点击“开始”
        find_and_click_button(dsview_window, "开始")
    # else:
        # 如果“开始”按钮不可用，说明已经是“停止”状态，继续执行后续逻辑
        # print(f"{get_current_time()} - DSView 已经是停止状态，继续执行后续逻辑")

def capture_mcu_flash_tool_popup(title_txt):
    """检测 MCU Flash Tool 弹窗"""
    print(f"{get_current_time()} - 进入检测函数")
    try:
        # 连接到 MCU Flash Tool 窗口，使用 uia 后端
        print(f"{get_current_time()} - 开始连接")
        app = Application(backend='uia').connect(title=title_txt)
        print(f"{get_current_time()} - 连接成功")
        popup = app.window(title_re='.*诊断工具.*')
        if popup.exists():
            print(f"{get_current_time()} - 捕获到 MCU Flash Tool 弹窗提醒")
            return True
        else:
            print(f"{get_current_time()} - 未找到 MCU Flash Tool 弹窗提醒")
            return False
    except Exception as e:
        print(f"{get_current_time()} - 捕获 MCU Flash Tool 弹窗提醒时出错: {e}")
        return False

def main():
    """主函数"""
    capture_title_txt = "MCU Flash Tool - ECU Programming_Project.EDS     ( ECU2 )"

    while True:
        # 启动 DSView 数据采集
        start_dsview_collect()

        # 检测 MCU Flash Tool 弹窗
        print(f"{get_current_time()} - 开始检测弹窗")
        flag = capture_mcu_flash_tool_popup(capture_title_txt)
        print(f"{get_current_time()} - 检测弹窗结束")

        if flag:
            # 如果检测到弹窗，停止 DSView 数据采集
            stop_dsview_collect()
            break
        # print(f"next time test")


if __name__ == "__main__":
    main()