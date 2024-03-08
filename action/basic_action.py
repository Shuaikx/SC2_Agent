
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, GATEWAY, \
    CYBERNETICSCORE, STALKER, STARGATE, VOIDRAY
import random


async def build_worker(bot):
    '''
    一直生产农民。
    如果农民数量大于等于基地数量*22，那么停止建造
    '''
    nexuses = bot.units(NEXUS).ready
    if nexuses.exists:
        if len(bot.units(PROBE)) < len(nexuses) * 22:
            for nexus in nexuses:
                if nexus.is_idle and bot.can_afford(PROBE):
                    await bot.do(nexus.train(PROBE))


async def build_pylon(bot):
    """
    建造水晶。
    如果人口上限-当前人口<=4，那么建造一个水晶塔。
    """
    # 检查人口上限-当前人口是否小于等于4
    if bot.supply_left <= 4:
        # 检查是否有足够的资源来建造水晶塔，并且当前没有正在建造的水晶塔
        if bot.can_afford(PYLON) and bot.already_pending(PYLON) == 0:
            # 获取所有就绪的基地
            nexuses = bot.units(NEXUS).ready
            if nexuses.exists:
                # 随机选择一个基地
                chosen_nexus = random.choice(nexuses)
                # 找到离该基地10格外的位置来建造水晶塔
                build_position = chosen_nexus.position.towards_with_random_angle(bot.game_info.map_center, distance=15)
                # 开始建造水晶塔
                await bot.build(PYLON, build_position)
                print("建造水晶塔")



async def build_nexus(bot):
    '''
    建造基地。
    如果资金大于400块钱，那么建造一个基地
    '''
    if bot.can_afford(NEXUS) and bot.already_pending(NEXUS) == 0:
        await bot.expand_now()


async def build_assimilators(bot):
    """
    建造气矿
    """
    for nexus in bot.units(NEXUS).ready:
        vespenes = bot.state.vespene_geyser.closer_than(25.0, nexus)
        for vespene in vespenes:
            if not bot.can_afford(ASSIMILATOR):
                break
            worker = bot.select_build_worker(vespene.position)
            if worker is None:
                break
            if not bot.units(ASSIMILATOR).closer_than(1.0, vespene).exists:
                await bot.do(worker.build(ASSIMILATOR, vespene))



