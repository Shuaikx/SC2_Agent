import pickle
import threading
from sc2.constants import UnitTypeId
from sc2.bot_ai import BotAI
from sc2.main import run_game
from sc2.data import Difficulty, Race
import sc2
from sc2 import maps
from sc2.player import Bot, Computer
import pyautogui

from base_skill import *
from tactics_library import *


def fullscreen():
    pyautogui.keyDown('alt')
    pyautogui.press('enter')
    pyautogui.keyUp('alt')
    print("1")


class MyBot(BotAI):
    def __init__(self):
        super().__init__()
        self.game_lock = threading.Lock()
        self.proxy_built = False
        self.warpgate_started = False

    async def on_step(self, iteration):
        # 在每个游戏步骤中调用 build_worker 方法

        try:
            with open('state_rwd_action.pkl', 'rb') as f:
                state_rwd_action = pickle.load(f)
                # if state_rwd_action['action'] is None:
                #     # print("No action yet")
                #     no_action = True
                # else:
                #     # print("Action found")
                #     no_action = False
        except:
            pass
        await self.distribute_workers()

        # await warp_zealots_allin(self)
        action = state_rwd_action

        if action == 0:
            tactics = await warp_darktemplar_suppress(self)
            print(tactics)
            print(self.units(UnitTypeId.STALKER).amount)
            if tactics:
                action = 1
                with open('state_rwd_action.pkl', 'wb') as f:
                    pickle.dump(action, f)
            else:
                action = 0
                with open('state_rwd_action.pkl', 'wb') as f:
                    pickle.dump(action, f)
        if action == 1:
            await warp_zealots_allin(self)
        if action == 2:
            aaa=await rapid_economic_development(self)
            print(aaa)
            if aaa:
                action=3
        print(action)
        # await warp_zealots_allin(self)
        # await build_assimilators(self)
        # # # await self.distribute_workers()
        # # #
        # await build_gateway(self)
        # await build_worker(self)
        # await build_cyberneticscore(self)
        # await update_warp_gate(self)
        # # await build_stargate(self)
        # # await warp_stalker(self)
        # # await build_robotics_facility(self)
        # # await build_robotics_bay(self)
        # await build_twilight_council(self)
        # await build_dark_shrine(self)
        # await build_shield_battery(self)
        # await warp_darktemplar(self)
        # await attack(self)
        # # await update_charge(self)
        # await update_blink(self)
        # await chronoboostenergycost(self)
        # await train_voidray(self)
        # await warp_in_units(self)
        game_loop = self.state.game_loop

        # 转换游戏时间为秒数
        game_time_seconds = game_loop / 22.4
        nexus_count = self.structures(UnitTypeId.NEXUS).amount
        # 农民（探测器）数量
        probe_count = self.units(UnitTypeId.PROBE).amount
        # 战斗人口数量（军事单位）
        army_count = self.supply_army
        # 建筑数量示例：兵营和控制核心
        gateway_count = self.structures(UnitTypeId.GATEWAY).amount
        cybernetics_core_count = self.structures(UnitTypeId.CYBERNETICSCORE).amount
        # 人口上限
        supply_cap = self.supply_cap
        # 人口使用
        supply_used = self.supply_used
        # 矿脉余额
        minerals = self.minerals
        # 瓦斯余额
        vespene = self.vespene
        # 所能看到的敌方建筑和单位
        enemy_structures = self.enemy_structures
        enemy_units = self.enemy_units

        # for enemy_unit in enemy_units:
        #     print(enemy_unit.type_id, enemy_unit.hit_points)
        import json

        # 收集你想要写入JSON的数据
        game_data = {
            "nexus_count": nexus_count,
            "probe_count": probe_count,
            "army_count": army_count,
            "gateway_count": gateway_count,
            "cybernetics_core_count": cybernetics_core_count,
            "supply_cap": supply_cap,
            "supply_used": supply_used,
            "minerals": minerals,
            "vespene": vespene,
            # 收集敌方建筑详细信息
            "enemy_structures": [
                {
                    "type_id": str(structure.type_id),
                    "position": [structure.position.x, structure.position.y],
                } for structure in self.enemy_structures
            ],
            # 原有的敌方单位信息保持不变
            "enemy_units": [
                {"type_id": str(unit.type_id)} for unit in enemy_units
            ],
        }
        structure_counts = {}
        for structure in game_data["enemy_structures"]:
            type_id = structure["type_id"]
            if type_id in structure_counts:
                structure_counts[type_id]["count"] += 1
            else:
                structure_counts[type_id] = {"type_id": type_id, "count": 1, "position": structure["position"]}

        # 生成新的列表，每种类型的建筑只占用一个条目，并包含count字段
        new_enemy_structures = list(structure_counts.values())

        # 更新原始数据
        game_data["enemy_structures"] = new_enemy_structures
        # 将数据写入JSON文件
        with open('game_info.json', 'w') as file:
            json.dump(game_data, file, indent=4)

        # 打印信息
        print(f"基地数量: {nexus_count}, 农民数量: {probe_count}, 战斗人口: {army_count}")
        print(f"兵营数量: {gateway_count}, 控制核心数量: {cybernetics_core_count}")
        print(f"人口上限: {supply_cap}, 人口使用: {supply_used}")
        print(f"矿脉余额: {minerals}, 瓦斯余额: {vespene}")
        print(f"已探测到的敌方建筑: {enemy_structures}, 已探测到的敌方单位: {enemy_units}")

        # 更新上次侦察的时间
        if game_time_seconds % 60 == 0 and game_time_seconds > 5:
            # 创建一个包含所有可能的战斗单位类型的列表
            possible_combat_units = [UnitTypeId.ZEALOT, UnitTypeId.STALKER]
            print("aaaaaaaaaa")
            # 尝试找到一个可用的战斗单位
            scout = None
            for unit_type in possible_combat_units:
                if self.units(unit_type).idle.exists:
                    scout = self.units(unit_type).idle.random
                    break

            # 如果没有找到战斗单位，使用一个农民进行侦察
            if not scout and self.workers.exists:
                scout = self.units(UnitTypeId.PROBE).random

            if scout:
                print("55555555555")
                # 敌方的初始出生点
                target = self.enemy_start_locations[0]
                # 派遣侦察单位
                self.do(scout.move(target))
            else:
                print("No available unit for scouting")
        # 如果游戏时间达到 60 秒，则暂停游戏
        # if game_time_seconds >= 5:
        #     acquired = self.game_lock.acquire(blocking=False)
        #     if acquired:
        #         print("游戏已暂停")
        #         time.sleep(10)
        #     self.game_lock.release()
        #     print("游戏已恢复")

        # print("当前游戏时间（秒）：", game_time_seconds)


# 创建 Bot 实例
bot = Bot(Race.Protoss, MyBot())

# 运行游戏
run_game(maps.get("AcropolisLE"), [
    bot,
    Computer(Race.Random, Difficulty.Hard),
], realtime=False)
