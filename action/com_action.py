from sc2 import UnitTypeId
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, GATEWAY, \
    CYBERNETICSCORE, STALKER, STARGATE, VOIDRAY, AbilityId
import random


async def build_gateway(bot):
    """
    建造传送门。
    选择最初的那个基地，找到离它10格外但是20格内的水晶（pylon），然后建造传送门。
    """
    # 获取最初的基地
    nexus = bot.units(NEXUS).first

    # 找到离该基地10格外但是20格内的水晶
    pylons = bot.units(PYLON).closer_than(20, nexus)
    pylons = pylons.filter(lambda pylon: pylon.distance_to(nexus) > 10)
    gateways = bot.units(GATEWAY)
    print(gateways.amount)
    wrapgates = bot.units(UnitTypeId.WARPGATE)
    print(wrapgates.amount)
    # 如果有符合条件的水晶
    if pylons:
        pylon = pylons.random
        build_position = pylon.position.towards(nexus.position)

        # 检查是否有足够的资源来建造传送门
        if bot.can_afford(GATEWAY) and gateways.amount < 3 and wrapgates.amount < 3:
            # 使用建造命令开始建造传送门
            await bot.build(GATEWAY, build_position)
            print("建造传送门")


async def build_cyberneticscore(bot):
    """
    建造控制芯核。
    如果没有控制芯核，就建造一个，否则不用建造。
    """
    nexus = bot.units(NEXUS).first

    # 找到离该基地10格外但是20格内的水晶
    pylons = bot.units(PYLON).closer_than(20, nexus)
    pylons = pylons.filter(lambda pylon: pylon.distance_to(nexus) > 10)
    cyberneticscores = bot.units(CYBERNETICSCORE)
    # 如果有符合条件的水晶
    if pylons:
        pylon = pylons.random
        build_position = pylon.position.towards(nexus.position)
        # 检查是否有足够的资源来建造控制芯核
        if bot.can_afford(CYBERNETICSCORE) and cyberneticscores.amount < 1 and bot.already_pending(
                CYBERNETICSCORE) == 0:
            # 开始建造控制芯核
            await bot.build(CYBERNETICSCORE, build_position)
            print("建造控制芯核")


async def build_stargate(bot):
    """
    建造星门。
    """
    # 检查资源是否足够
    nexus = bot.units(NEXUS).first

    # 找到离该基地10格外但是20格内的水晶
    pylons = bot.units(PYLON).closer_than(20, nexus)
    pylons = pylons.filter(lambda pylon: pylon.distance_to(nexus) > 10)
    stargates = bot.units(STARGATE).amount
    # 如果有符合条件的水晶
    if pylons:
        pylon = pylons.random
        build_position = pylon.position.towards(nexus.position)
        if bot.can_afford(UnitTypeId.STARGATE) and stargates < 3:
            # 使用命令开始建造星门
            await bot.build(UnitTypeId.STARGATE, build_position)


async def update_warp_gate(bot):
    """
    在控制芯核中建造裂隙之门（Warp Gate）。
    """
    # 检查是否已经有控制芯核
    if bot.units(CYBERNETICSCORE).ready:
        # 获取控制芯核
        cyberneticscore = bot.units(CYBERNETICSCORE).ready.first
        # 检查控制芯核是否已经建造完成
        if cyberneticscore:
            # 检查是否已经有裂隙之门，如果没有则开始升级
            if bot.can_afford(AbilityId.RESEARCH_WARPGATE):
                await bot.do(cyberneticscore(AbilityId.RESEARCH_WARPGATE))
                print("控制芯核升级为裂隙之门")


async def train_voidray(bot):
    '''
    建造虚空辉光舰
    '''
    if bot.can_afford(UnitTypeId.VOIDRAY):
        # 获取就绪的星门
        stargates = bot.units(UnitTypeId.STARGATE).ready
        if stargates.exists:
            # 选择一个星门训练虚空辉光舰
            target_stargate = stargates.random
            if target_stargate.noqueue:
                await bot.do(target_stargate.train(UnitTypeId.VOIDRAY))

# async def train_stalker(bot):
#     """
#     使用 Warp Gate 生产追猎者。
#     """
#     # 检查资源是否足够
#     if bot.can_afford(UnitTypeId.STALKER):
#         # 获取就绪的 Warp Gate
#         warp_gates = bot.units(UnitTypeId.WARPGATE).ready
#         if warp_gates.exists:
#             # 选择一个 Warp Gate 生产追猎者
#             target_warp_gate = warp_gates.random
#             abilities = await bot.get_available_abilities(target_warp_gate)
#             # 检查是否有生产追猎者的能力
#             if AbilityId.WARPGATETRAIN_STALKER in abilities:
#                 await bot.do(target_warp_gate(AbilityId.WARPGATETRAIN_STALKER))
#                 print("Warp Gate 生产追猎者")
