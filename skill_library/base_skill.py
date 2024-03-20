import random

from sc2 import maps  # maps method for loading maps to play in.
from sc2.bot_ai import BotAI  # parent class we inherit from
from sc2.data import Difficulty, Race  # difficulty for bots, race for the 1 of 3 races
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.main import run_game  # function that facilitates actually running the agents in games
from sc2.player import Bot, Computer


async def build_worker(bot):
    '''
    一直生产农民。
    如果农民数量大于等于基地数量*22，那么停止建造
    '''
    for nexus in bot.townhalls.ready:
        # 检查是否有足够的资源并且探测者的数量少于基地数量*22
        if bot.can_afford(UnitTypeId.PROBE) and bot.supply_workers < bot.townhalls.amount * 22:
            # 也要确保没有达到供应上限
            if bot.supply_left > 0 and nexus.is_idle and bot.units(UnitTypeId.PROBE).amount < 60:
                # 生产探测者
                nexus.train(UnitTypeId.PROBE)


async def build_pylon(bot):
    '''
    建造PYLON，当人口小于5时
    '''
    if bot.supply_left < 5:
        if bot.already_pending(UnitTypeId.PYLON) == 0:
            if bot.can_afford(UnitTypeId.PYLON):
                # 选择一个随机的基地（Nexus）
                nexus = random.choice(bot.townhalls.ready)
                # 计算一个距离该基地5个格子的位置
                target_position = nexus.position.towards(bot.game_info.map_center, 5)
                # 在计算出的位置附近建造PYLON
                await bot.build(UnitTypeId.PYLON, near=target_position)


async def build_nexus(bot):
    '''
    建造基地。
    如果资金大于400块钱，那么建造一个基地
    '''
    if bot.can_afford(UnitTypeId.NEXUS) and bot.already_pending(UnitTypeId.NEXUS) == 0:
        await bot.expand_now()


async def build_assimilators(bot):
    """
    建造气矿
    """
    if bot.structures(UnitTypeId.GATEWAY).amount >= 1:
        for nexus in bot.townhalls:
            for geyser in bot.vespene_geyser.closer_than(10, nexus):
                # build assimilator if there isn't one already:
                if not bot.can_afford(UnitTypeId.ASSIMILATOR):
                    break
                if not bot.structures(UnitTypeId.ASSIMILATOR).closer_than(1.0, geyser).exists:
                    await bot.build(UnitTypeId.ASSIMILATOR, geyser)


async def build_gateway(bot):
    '''
    建造传送门
    '''
    for nexus in bot.townhalls:
        # is there is not a gateway close:
        if not bot.structures(UnitTypeId.GATEWAY).closer_than(10, nexus).exists:
            # if we can afford it:
            if bot.can_afford(UnitTypeId.GATEWAY) and bot.already_pending(UnitTypeId.GATEWAY) == 0:
                # build gateway
                await bot.build(UnitTypeId.GATEWAY, near=nexus)


async def build_cyberneticscore(bot):
    '''
      建造控制芯核
    '''
    for nexus in bot.townhalls:
        if bot.structures(UnitTypeId.GATEWAY).exists:
            if not bot.structures(UnitTypeId.CYBERNETICSCORE).closer_than(10, nexus).exists:
                # if we can afford it:
                if bot.can_afford(UnitTypeId.CYBERNETICSCORE) and bot.already_pending(
                        UnitTypeId.CYBERNETICSCORE) == 0:
                    # build cybernetics core
                    await bot.build(UnitTypeId.CYBERNETICSCORE, near=nexus)


async def update_warp_gate(bot):
    """
    在控制芯核中建造裂隙之门（Warp Gate）。
    """
    # 检查是否已经有控制芯核
    if bot.structures(UnitTypeId.CYBERNETICSCORE).ready:
        # 获取控制芯核
        cyberneticscore = bot.structures(UnitTypeId.CYBERNETICSCORE).ready.first
        # 检查控制芯核是否已经建造完成
        if cyberneticscore:
            # 检查是否已经有裂隙之门，如果没有则开始升级
            if bot.can_afford(AbilityId.RESEARCH_WARPGATE):
                bot.do(cyberneticscore(AbilityId.RESEARCH_WARPGATE))
                print("控制芯核升级为裂隙之门")


async def warp_zealots(bot):
    # print("kaishi")
    # for warpgate in bot.structures(UnitTypeId.WARPGATE).ready:
    #     print("11111111111")
    #     # Check if we can warp in a Zealot
    #     if bot.can_afford(UnitTypeId.ZEALOT) and bot.supply_left > 0:
    #         print("22222222222222222222222")
    #         target_position = warpgate.position.towards(bot.game_info.map_center, 1)
    #         warpgate.warp_in(UnitTypeId.ZEALOT, position=target_position)
    # for warpgate in bot.units(UnitTypeId.WARPGATE).ready:
    #     abilities = await bot.get_available_abilities(warpgate)
    #     # all the units have the same cooldown anyway so let's just look at ZEALOT
    #     if AbilityId.WARPGATETRAIN_ZEALOT in abilities:
    #         pos = proxy.position.to2.random_on_distance(4)
    #         placement = await bot.find_placement(AbilityId.WARPGATETRAIN_STALKER, pos, placement_step=1)
    #         if placement is None:
    #             # return ActionResult.CantFindPlacementLocation
    #             print("can't place")
    #             return
    #         await bot.do(warpgate.warp_in(UnitTypeId.ZEALOT, placement))

    # 选择一个Pylon作为折跃位置的参考点
    if bot.structures(UnitTypeId.PYLON).ready.exists:
        proxy_pylon = bot.structures(UnitTypeId.PYLON).ready.closest_to(bot.start_location)

        # 遍历所有就绪的Warp Gate
        for warpgate in bot.structures(UnitTypeId.WARPGATE).ready:
            abilities = await bot.get_available_abilities(warpgate)
            # 检查是否可以折跃狂热者
            if AbilityId.WARPGATETRAIN_ZEALOT in abilities:
                # 计算折跃位置，靠近选中的Pylon
                position = proxy_pylon.position.to2.random_on_distance(3)
                # 执行折跃操作
                bot.do(warpgate.warp_in(UnitTypeId.ZEALOT, position))


async def warp_stalker(bot):
    # 选择一个Pylon作为折跃位置的参考点
    if bot.structures(UnitTypeId.PYLON).ready.exists:
        proxy_pylon = bot.structures(UnitTypeId.PYLON).ready.closest_to(bot.start_location)

        # 遍历所有就绪的Warp Gate
        for warpgate in bot.structures(UnitTypeId.WARPGATE).ready:
            abilities = await bot.get_available_abilities(warpgate)
            # 检查是否可以折跃狂热者
            if AbilityId.WARPGATETRAIN_ZEALOT in abilities:
                # 计算折跃位置，靠近选中的Pylon
                position = proxy_pylon.position.to2.random_on_distance(3)
                # 执行折跃操作
                bot.do(warpgate.warp_in(UnitTypeId.STALKER, position))


async def build_stargate(bot):
    for nexus in bot.townhalls:
        if not bot.structures(UnitTypeId.STARGATE).closer_than(10, nexus).exists:
            # if we can afford it:
            if bot.can_afford(UnitTypeId.STARGATE) and bot.already_pending(UnitTypeId.STARGATE) == 0:
                # build stargate
                await bot.build(UnitTypeId.STARGATE, near=nexus)


async def build_robotics_facility(bot):
    for nexus in bot.townhalls:
        if not bot.structures(UnitTypeId.ROBOTICSFACILITY).closer_than(10, nexus).exists:
            # if we can afford it:
            if bot.can_afford(UnitTypeId.ROBOTICSFACILITY) and bot.already_pending(UnitTypeId.ROBOTICSFACILITY) == 0:
                # build stargate
                await bot.build(UnitTypeId.ROBOTICSFACILITY, near=nexus)


async def build_robotics_bay(bot):
    for nexus in bot.townhalls:
        if not bot.structures(UnitTypeId.ROBOTICSBAY).closer_than(10, nexus).exists:
            # if we can afford it:
            if bot.can_afford(UnitTypeId.ROBOTICSBAY) and bot.already_pending(UnitTypeId.ROBOTICSBAY) == 0:
                # build stargate
                await bot.build(UnitTypeId.ROBOTICSBAY, near=nexus)


# vc
async def build_twilight_council(bot):
    for nexus in bot.townhalls:
        if not bot.structures(UnitTypeId.TWILIGHTCOUNCIL).closer_than(10, nexus).exists:
            # if we can afford it:
            if bot.can_afford(UnitTypeId.TWILIGHTCOUNCIL) and bot.already_pending(UnitTypeId.TWILIGHTCOUNCIL) == 0:
                # build stargate
                await bot.build(UnitTypeId.TWILIGHTCOUNCIL, near=nexus)


# 电池
async def build_shield_battery(bot):
    for nexus in bot.townhalls:
        if not bot.structures(UnitTypeId.SHIELDBATTERY).closer_than(10, nexus).exists:
            # if we can afford it:
            if bot.can_afford(UnitTypeId.SHIELDBATTERY) and bot.already_pending(UnitTypeId.SHIELDBATTERY) == 0:
                # build stargate
                await bot.build(UnitTypeId.SHIELDBATTERY, near=nexus)


# 隐刀塔
async def build_dark_shrine(bot):
    for nexus in bot.townhalls:
        if not bot.structures(UnitTypeId.DARKSHRINE).closer_than(10, nexus).exists:
            # if we can afford it:
            if bot.can_afford(UnitTypeId.DARKSHRINE) and bot.already_pending(UnitTypeId.DARKSHRINE) == 0:
                # build stargate
                await bot.build(UnitTypeId.DARKSHRINE, near=nexus)


# 隐刀
async def warp_darktemplar(bot):
    # 选择一个Pylon作为折跃位置的参考点
    if bot.structures(UnitTypeId.PYLON).ready.exists:
        proxy_pylon = bot.structures(UnitTypeId.PYLON).ready.closest_to(bot.start_location)

        # 遍历所有就绪的Warp Gate
        for warpgate in bot.structures(UnitTypeId.WARPGATE).ready:
            abilities = await bot.get_available_abilities(warpgate)
            # 检查是否可以折跃狂热者
            if AbilityId.WARPGATETRAIN_ZEALOT in abilities:
                # 计算折跃位置，靠近选中的Pylon
                position = proxy_pylon.position.to2.random_on_distance(3)
                # 执行折跃操作
                bot.do(warpgate.warp_in(UnitTypeId.DARKTEMPLAR, position))


async def attack_enemies_within_sight(bot):
    non_combat_units = [UnitTypeId.PROBE, UnitTypeId.OVERLORD]
    if bot.units.ready.idle:
        # 寻找视野中的敌人单位

        for enemy in bot.enemy_units:
            # 检查是否有可以指挥的军队
            for unit in bot.units.ready.idle:
                # 过滤出战斗单位，排除非战斗单位
                if unit.type_id not in non_combat_units:
                    # 向敌人单位发起攻击
                    bot.do(unit.attack(enemy))


async def update_charge(bot):
    # 检查是否已经有控制芯核
    if bot.structures(UnitTypeId.TWILIGHTCOUNCIL).ready:
        # 获取控制芯核
        TWILIGHTCOUNCIL = bot.structures(UnitTypeId.TWILIGHTCOUNCIL).ready.first
        # 检查控制芯核是否已经建造完成
        if TWILIGHTCOUNCIL:
            # 检查是否已经有裂隙之门，如果没有则开始升级
            if bot.can_afford(AbilityId.RESEARCH_CHARGE):
                bot.do(TWILIGHTCOUNCIL(AbilityId.RESEARCH_CHARGE))


async def attack(self):  # 遍历所有单位，而不仅仅是虚空之舰
    non_combat_units = [UnitTypeId.PROBE, UnitTypeId.OVERLORD]
    if self.units.ready.idle:
        for unit in self.units.ready.idle:

            # 检查是否为能够攻击的单位
            # 这里的unit.can_attack是假设的属性，你需要根据实际情况调整
            if unit.type_id not in non_combat_units:
                # 如果我们可以攻击附近的敌方单位：
                if self.enemy_units.closer_than(10, unit):
                    # 攻击!
                    unit.attack(random.choice(self.enemy_units.closer_than(20, unit)))
                # 如果我们可以攻击附近的敌方建筑：
                elif self.enemy_structures.closer_than(10, unit):
                    # 攻击!
                    unit.attack(random.choice(self.enemy_structures.closer_than(20, unit)))
                # 任何敌方单位：
                elif self.enemy_units:
                    # 攻击!
                    unit.attack(random.choice(self.enemy_units))
                # 任何敌方建筑：
                elif self.enemy_structures:
                    # 攻击!
                    unit.attack(random.choice(self.enemy_structures))
                # 敌方出生地：
                elif self.enemy_start_locations:
                    # 攻击!
                    unit.attack(self.enemy_start_locations[0])

async def train_voidray(bot):
    if bot.can_afford(UnitTypeId.VOIDRAY):
        for sg in bot.structures(UnitTypeId.STARGATE).ready.idle:
            if bot.can_afford(UnitTypeId.VOIDRAY):
                sg.train(UnitTypeId.VOIDRAY)

async def update_blink(bot):
    # 检查是否已经有控制芯核
    if bot.structures(UnitTypeId.TWILIGHTCOUNCIL).ready:
        # 获取控制芯核
        TWILIGHTCOUNCIL = bot.structures(UnitTypeId.TWILIGHTCOUNCIL).ready.first
        # 检查控制芯核是否已经建造完成
        if TWILIGHTCOUNCIL:
            # 检查是否已经有裂隙之门，如果没有则开始升级
            if bot.can_afford(AbilityId.RESEARCH_BLINK):
                bot.do(TWILIGHTCOUNCIL(AbilityId.RESEARCH_BLINK))


async def chronoboostenergycost(bot,structures):
    if bot.structures(UnitTypeId.NEXUS).ready and bot.structures(UnitTypeId.TWILIGHTCOUNCIL).ready:
        nexus = bot.structures(UnitTypeId.NEXUS).first  # 选择第一个母舰核心
        cybernetics_core = bot.structures(UnitTypeId.TWILIGHTCOUNCIL).first  # 选择第一个控制核心

        # 检查母舰核心的能量是否足够使用星空加速
        if nexus.energy >= 50:
            # 对控制核心使用星空加速技能
            bot.do(nexus(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, structures))

async def attack_worker(self):
    non_combat_units = [UnitTypeId.PROBE, UnitTypeId.OVERLORD]
    attack_workers = [UnitTypeId.PROBE,UnitTypeId.SCV,UnitTypeId.DRONE]
    if self.units.ready.idle:
        for unit in self.units.ready.idle:

            # 检查是否为能够攻击的单位
            # 这里的unit.can_attack是假设的属性，你需要根据实际情况调整
            if unit.type_id not in non_combat_units:
                if self.enemy_units:
                    # 攻击!
                    unit.attack(random.choice(attack_workers))