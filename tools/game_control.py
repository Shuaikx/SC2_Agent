import time
import pyautogui
from datetime import datetime
import sys

sys.path.append('SCII-agent-main/sc2_agent')

import os

current_folder = os.getcwd()
parent_folder = os.path.dirname(current_folder)
sys.path.append(parent_folder)


def fullscreen():
    '''
    将游戏设置为全屏
    '''
    time.sleep(1)
    pyautogui.keyDown('alt')
    pyautogui.press('enter')
    pyautogui.keyUp('alt')


def screenshot():
    '''
    对图像进行截图
    '''
    seconds_since_midnight = datetime.now().hour * 3600 + datetime.now().minute * 60 + datetime.now().second
    filename = f'{parent_folder}/sc2_agent/screen_image/game_{seconds_since_midnight}.png'

    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    return filename


def moveto_menu():
    pyautogui.moveTo(1886, 803)
    time.sleep(1)


def game_recovery():
    pyautogui.moveTo(966, 623)
    time.sleep(1)


def pause_game():
    pyautogui.click()


