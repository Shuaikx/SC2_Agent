import time
import pyautogui
from datetime import datetime


def fullscreen():
    '''
    将游戏设置为全屏
    '''
    pyautogui.keyDown('alt')
    pyautogui.press('enter')
    pyautogui.keyUp('alt')


def screenshot():
    '''
    对图像进行截图
    '''
    seconds_since_midnight = datetime.now().hour * 3600 + datetime.now().minute * 60 + datetime.now().second
    filename = f'game_{seconds_since_midnight}.png'

    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    return filename


def moveto_menu():
    pyautogui.moveTo(1886, 803)
    time.sleep(1)


def pause_game():
    pyautogui.click()

# time.sleep(30)
# fullscreen()
# time.sleep(10)
# pyautogui.moveTo(1886, 803)
# time.sleep(1)
# pyautogui.click()
# # 获取当前鼠标位置
# x, y = pyautogui.position()
# print(x,y)
