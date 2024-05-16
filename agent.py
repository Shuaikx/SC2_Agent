import cv2
import math
import numpy as np
import pickle
import sys
from skill_library.base_skill import *
from skill_library.tactics_library import *

sys.path.append(r'/tools')

sys.path.append(r'/')

from tools.game_control import *
from tools.prompt import *

SAVE_REPLAY = True

total_steps = 10000
steps_for_pun = np.linspace(0, 1, total_steps)
step_punishment = ((np.exp(steps_for_pun ** 3) / 10) - 0.1) * 10

state = {'action': None, }


class MyBot(BotAI):
    def __init__(self):
        super().__init__()

    async def on_step(self, iteration: int):  # on_step is a method that is called every step of the game.
        no_action = True
        global state, action
        while no_action:
            try:
                with open('state_rwd.pkl', 'rb') as f:
                    state_rwd_action = pickle.load(f)

                    if state_rwd_action['action'] is None:
                        # print("No action yet")
                        no_action = True
                    else:
                        # print("Action found")
                        no_action = False
            except:
                pass
        game_loop = self.state.game_loop
        print(state_rwd_action)
        # 转换游戏时间为秒数
        game_time_second = game_loop / 22.4
        game_time_seconds = int(game_time_second)
        times = game_time_seconds // 60
        print(state)
        try:
            with open('state.pkl', 'rb') as f:
                state = pickle.load(f)
                print(state)
        except:
            pass
        await self.distribute_workers()
        if game_time_seconds == 10:
            fullscreen()
        remainder = game_time_seconds % 20
        if game_time_seconds % 20 == 0 and game_time_seconds > 11 and action != 18:
            moveto_menu()
            pause_game()
            action = max_action()
            game_recovery()
            pause_game()
        else:
            if state['action'] is None:
                action = state_rwd_action['action']
            else:
                action = state['action']
        print(action)
        if action == 0:
            # 造农民
            try:
                await build_worker(self)
            except Exception as e:
                print(e)
        if action == 1:
            try:
                await build_pylon(self)
            except Exception as e:
                print(e)
        if action == 2:
            try:
                await build_nexus(self)
            except Exception as e:
                print(e)
        if action == 3:
            try:
                await build_assimilators(self)
            except Exception as e:
                print(e)
        if action == 4:
            try:
                await build_gateway(self)
            except Exception as e:
                print(e)
        if action == 5:
            try:
                await build_cyberneticscore(self)
            except Exception as e:
                print(e)
        if action == 6:
            try:
                await build_twilight_council(self)
            except Exception as e:
                print(e)
        if action == 7:
            try:
                await build_shield_battery(self)
            except Exception as e:
                print(e)
        if action == 8:
            try:
                await build_dark_shrine(self)
            except Exception as e:
                print(e)
        if action == 9:
            try:
                await update_warp_gate(self)
            except Exception as e:
                print(e)
        if action == 10:
            try:
                await update_charge(self)
            except Exception as e:
                print(e)
        if action == 11:
            try:
                await build_stargate(self)
            except Exception as e:
                print(e)
        if action == 12:
            try:
                await warp_stalker(self)
            except Exception as e:
                print(e)
        if action == 13:
            try:
                await warp_darktemplar(self)
            except Exception as e:
                print(e)
        if action == 14:
            try:
                await warp_zealots(self)
            except Exception as e:
                print(e)
        if action == 15:
            try:
                await build_twilight_council(self)
            except Exception as e:
                print(e)
        if action == 16:
            try:
                await train_voidray(self)
            except Exception as e:
                print(e)
        if action == 17:
            try:
                await attack(self)
            except Exception as e:
                print(e)

        # 战术
        if action == 18:
            try:
                result = await warp_zealots_allin(self)
                with open('state.pkl', 'wb') as f:
                    data = {"action": action, }
                    pickle.dump(data, f)
                print(result)
                if result:
                    with open('state.pkl', 'wb') as f:
                        data = {"action": None, }
                        pickle.dump(data, f)
            except Exception as e:
                print(e)
        if action == 19:
            try:
                result = await warp_darktemplar_suppress(self)
                with open('state.pkl', 'wb') as f:
                    data = {"action": action, }
                    pickle.dump(data, f)
                print(result)
                if result:
                    with open('state.pkl', 'wb') as f:
                        data = {"action": None, }
                        pickle.dump(data, f)


            except Exception as e:
                print(e)
        if action == 20:
            try:
                result = await defend(self)
                with open('state.pkl', 'wb') as f:
                    data = {"action": action, }
                    pickle.dump(data, f)
                print(result)
                if result:
                    with open('state.pkl', 'wb') as f:
                        data = {"action": None, }
                        pickle.dump(data, f)
            except Exception as e:
                print(e)
        if action == 21:
            try:
                result = await rapid_economic_development(self)
                with open('state.pkl', 'wb') as f:
                    data = {"action": action, }
                    pickle.dump(data, f)
                print(result)
                if result:
                    with open('state.pkl', 'wb') as f:
                        data = {"action": None, }
                        pickle.dump(data, f)
            except Exception as e:
                print(e)
        game_loop = self.state.game_loop

        # Convert the game time to seconds
        game_time_seconds = game_loop / 22.4
        nexus_count = self.structures(UnitTypeId.NEXUS).amount
        
        # Number of farmers (detectors)
        probe_count = self.units(UnitTypeId.PROBE).amount
        
        # Combat population (military units)
        army_count = self.supply_army
        
        # Example number of buildings: Barracks and control core
        gateway_count = self.structures(UnitTypeId.GATEWAY).amount
        cybernetics_core_count = self.structures(UnitTypeId.CYBERNETICSCORE).amount
        

        supply_cap = self.supply_cap

        supply_used = self.supply_used

        minerals = self.minerals

        vespene = self.vespene

        enemy_structures = self.enemy_structures
        enemy_units = self.enemy_units
        game_time = f"{game_time_seconds}s"

        # read json
        game_data = {
            "game_time": game_time,
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
        with open('sc2_agent/input/game_info.json', 'w') as file:
            json.dump(game_data, file, indent=4)

        # 打印信息
        print(f"基地数量: {nexus_count}, 农民数量: {probe_count}, 战斗人口: {army_count}")
        print(f"兵营数量: {gateway_count}, 控制核心数量: {cybernetics_core_count}")
        print(f"人口上限: {supply_cap}, 人口使用: {supply_used}")
        print(f"矿脉余额: {minerals}, 瓦斯余额: {vespene}")
        print(f"已探测到的敌方建筑: {enemy_structures}, 已探测到的敌方单位: {enemy_units}")
        # 侦察
        if game_time_seconds % 60 == 0 and game_time_seconds > 5:
            try:
                if self.units(UnitTypeId.PROBE).idle.exists:
                    # pick one of these randomly:
                    probe = random.choice(self.units(UnitTypeId.PROBE).idle)
                else:
                    probe = random.choice(self.units(UnitTypeId.PROBE))
                # send probe towards enemy base:
                probe.attack(self.enemy_start_locations[0])
            except Exception as e:
                pass

        map = np.zeros((self.game_info.map_size[0], self.game_info.map_size[1], 3), dtype=np.uint8)

        # draw the minerals:
        for mineral in self.mineral_field:
            pos = mineral.position
            c = [175, 255, 255]
            fraction = mineral.mineral_contents / 1800
            if mineral.is_visible:
                # print(mineral.mineral_contents)
                map[math.ceil(pos.y)][math.ceil(pos.x)] = [int(fraction * i) for i in c]
            else:
                map[math.ceil(pos.y)][math.ceil(pos.x)] = [20, 75, 50]

                # draw the enemy start location:
        for enemy_start_location in self.enemy_start_locations:
            pos = enemy_start_location
            c = [0, 0, 255]
            map[math.ceil(pos.y)][math.ceil(pos.x)] = c

        # draw the enemy units:
        for enemy_unit in self.enemy_units:
            pos = enemy_unit.position
            c = [100, 0, 255]
            # get unit health fraction:
            fraction = enemy_unit.health / enemy_unit.health_max if enemy_unit.health_max > 0 else 0.0001
            map[math.ceil(pos.y)][math.ceil(pos.x)] = [int(fraction * i) for i in c]

        # draw the enemy structures:
        for enemy_structure in self.enemy_structures:
            pos = enemy_structure.position
            c = [0, 100, 255]
            # get structure health fraction:
            fraction = enemy_structure.health / enemy_structure.health_max if enemy_structure.health_max > 0 else 0.0001
            map[math.ceil(pos.y)][math.ceil(pos.x)] = [int(fraction * i) for i in c]

        # draw our structures:
        for our_structure in self.structures:
            # if it's a nexus:
            if our_structure.type_id == UnitTypeId.NEXUS:
                pos = our_structure.position
                c = [255, 255, 175]
                # get structure health fraction:
                fraction = our_structure.health / our_structure.health_max if our_structure.health_max > 0 else 0.0001
                map[math.ceil(pos.y)][math.ceil(pos.x)] = [int(fraction * i) for i in c]

            else:
                pos = our_structure.position
                c = [0, 255, 175]
                # get structure health fraction:
                fraction = our_structure.health / our_structure.health_max if our_structure.health_max > 0 else 0.0001
                map[math.ceil(pos.y)][math.ceil(pos.x)] = [int(fraction * i) for i in c]

        # draw the vespene geysers:
        for vespene in self.vespene_geyser:
            # draw these after buildings, since assimilators go over them.
            # tried to denote some way that assimilator was on top, couldnt
            # come up with anything. Tried by positions, but the positions arent identical. ie:
            # vesp position: (50.5, 63.5)
            # bldg positions: [(64.369873046875, 58.982421875), (52.85693359375, 51.593505859375),...]
            pos = vespene.position
            c = [255, 175, 255]
            fraction = vespene.vespene_contents / 2250

            if vespene.is_visible:
                map[math.ceil(pos.y)][math.ceil(pos.x)] = [int(fraction * i) for i in c]
            else:
                map[math.ceil(pos.y)][math.ceil(pos.x)] = [50, 20, 75]

        # draw our units:
        for our_unit in self.units:
            # if it is a voidray:
            if our_unit.type_id == UnitTypeId.VOIDRAY:
                pos = our_unit.position
                c = [255, 75, 75]
                # get health:
                fraction = our_unit.health / our_unit.health_max if our_unit.health_max > 0 else 0.0001
                map[math.ceil(pos.y)][math.ceil(pos.x)] = [int(fraction * i) for i in c]


            else:
                pos = our_unit.position
                c = [175, 255, 0]
                # get health:
                fraction = our_unit.health / our_unit.health_max if our_unit.health_max > 0 else 0.0001
                map[math.ceil(pos.y)][math.ceil(pos.x)] = [int(fraction * i) for i in c]

        # show map with opencv, resized to be larger:
        # horizontal flip:

        cv2.imshow('map', cv2.flip(cv2.resize(map, None, fx=4, fy=4, interpolation=cv2.INTER_NEAREST), 0))
        cv2.waitKey(1)

        if SAVE_REPLAY:
            # save map image into "replays dir"
            cv2.imwrite(f"replays/{int(time.time())}-{iteration}.png", map)

        reward = 0

        try:
            attack_count = 0
            # iterate through our void rays:
            for voidray in self.units(UnitTypeId.VOIDRAY):
                # if voidray is attacking and is in range of enemy unit:
                if voidray.is_attacking and voidray.target_in_range:
                    if self.enemy_units.closer_than(8, voidray) or self.enemy_structures.closer_than(8, voidray):
                        # reward += 0.005 # original was 0.005, decent results, but let's 3x it.
                        reward += 0.015
                        attack_count += 1

        except Exception as e:
            print("reward", e)
            reward = 0

        print(f"Iter: {iteration}. RWD: {reward}. VR: {self.units(UnitTypeId.VOIDRAY).amount},action: {action}")

        data = {"state": map, "reward": reward, "action": None, "done": False}  # empty action waiting for the next one!

        with open('state_rwd.pkl', 'wb') as f:
            pickle.dump(data, f)


bot = Bot(Race.Protoss, MyBot())

# 运行游戏
run_game(maps.get("2000AtmospheresAIE"), [
    bot,
    Computer(Race.Terran, Difficulty.Hard),
], realtime=True)
