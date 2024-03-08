
import threading

import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from action.basic_action import build_worker, build_pylon, build_nexus, build_assimilators
from action.com_action import build_gateway, build_cyberneticscore, update_warp_gate, build_stargate, train_voidray
import pyautogui


def fullscreen():
    pyautogui.keyDown('alt')
    pyautogui.press('enter')
    pyautogui.keyUp('alt')
    print("1")

class MyBot(sc2.BotAI):
    def __init__(self):
        super().__init__()
        self.game_lock = threading.Lock()

    async def on_step(self, iteration):
        # 在每个游戏步骤中调用 build_worker 方法
        await build_worker(self)
        await build_pylon(self)
        await build_nexus(self)
        await build_assimilators(self)
        await self.distribute_workers()

        await build_gateway(self)
        await build_cyberneticscore(self)
        await update_warp_gate(self)
        await build_stargate(self)
        await train_voidray(self)
        game_loop = self.state.game_loop

        # 转换游戏时间为秒数
        game_time_seconds = game_loop / 22.4

        # 如果游戏时间达到 60 秒，则暂停游戏
        # if game_time_seconds >= 5:
        #     acquired = self.game_lock.acquire(blocking=False)
        #     if acquired:
        #         print("游戏已暂停")
        #         time.sleep(10)
        #     self.game_lock.release()
        #     print("游戏已恢复")

        print("当前游戏时间（秒）：", game_time_seconds)


# 创建 Bot 实例
bot = Bot(Race.Protoss, MyBot())

# 运行游戏
run_game(maps.get("AcropolisLE"), [
    bot,
    Computer(Race.Terran, Difficulty.Easy),
], realtime=False)

