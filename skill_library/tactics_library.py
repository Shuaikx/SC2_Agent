from skill_library.base_skill import *
from sc2.ids.unit_typeid import UnitTypeId



async def warp_zealots_allin(self):
    """
    warp_zealots_allin: Refers to filling up eight warp gates and then warping in a large number of zealots to attack the enemy.

    Tactic Overview:A strategy for the 5-6 minute mark, featuring two nexuses, one assimilator, and having 35 probes. The attack is launched when the count of zealots reaches 15. This tactic cannot be used after 3 minutes.

    Tactic Characteristics: All-in, suitable for playing against Zerg and Terran.

    Tactic Advantages: Aggressive and fast.

    Tactic Disadvantages: Unable to defend against air units, and has relatively weak defense capabilities before the 3-minute mark. Additionally, as an all-in strategy, it must defeat the enemy in a single attempt.

    """
    await build_pylon(self)

    if self.structures(UnitTypeId.PROBE).amount < 35:
        await build_worker(self)
    if self.structures(UnitTypeId.NEXUS).amount < 2:
        await build_nexus(self)
    if self.structures(UnitTypeId.ASSIMILATOR).amount < 1:
        await build_assimilators(self)
    if self.structures(UnitTypeId.GATEWAY).amount < 1 and self.structures(UnitTypeId.WARPGATE).amount < 1:
        await build_gateway(self)
    if self.structures(UnitTypeId.CYBERNETICSCORE).amount < 1:
        await build_cyberneticscore(self)
    if self.structures(UnitTypeId.CYBERNETICSCORE).exists and self.structures(
            UnitTypeId.GATEWAY).amount < 8 and self.structures(UnitTypeId.WARPGATE).amount < 8:
        await build_gateway(self)
    await update_warp_gate(self)
    await warp_zealots(self)
    await attack_enemies_within_sight(self)
    if self.structures(UnitTypeId.TWILIGHTCOUNCIL).amount < 1:
        await build_twilight_council(self)
    await update_charge(self)
    if self.units(UnitTypeId.ZEALOT).amount > 15:
        await attack(self)


async def warp_darktemplar_suppress(self):
    """
    warp_darktemplar_suppress: Produces the darktemplar at the first time and then attacks the opponent's worker.
    Tactic Overview: Attack at around six minutes, need 2 Nexus, need 2 Assimilators, need 38 probe, attack the local worker when there are two darktemplars.
    Tactic Characteristics: Suppress the opponent's economy, suitable for use against Protoss, Zerg and Terran.
    Tactic Advantages: If the enemy does not have reconnaissance, it will be difficult to defend, and it can destroy a large number of workers in a short time
    Tactic Disadvantages: There is no defensive ability 5 minutes before, if the other side reconnaissance in advance, the difficulty of defense will be greatly reduced.
    """
    await build_pylon(self)

    if self.structures(UnitTypeId.PROBE).amount < 38:
        await build_worker(self)
    if self.structures(UnitTypeId.NEXUS).amount < 2:
        await build_nexus(self)
    if self.structures(UnitTypeId.ASSIMILATOR).amount < 2:
        await build_assimilators(self)
    if self.structures(UnitTypeId.GATEWAY).amount < 1 and self.structures(UnitTypeId.WARPGATE).amount < 1:
        await build_gateway(self)
    if self.structures(UnitTypeId.CYBERNETICSCORE).amount < 1:
        await build_cyberneticscore(self)
    if self.structures(UnitTypeId.CYBERNETICSCORE).exists and self.structures(
            UnitTypeId.GATEWAY).amount < 4 and self.structures(UnitTypeId.WARPGATE).amount < 4:
        await build_gateway(self)
    await update_warp_gate(self)
    # await attack_enemies_within_sight(self)
    if self.structures(UnitTypeId.TWILIGHTCOUNCIL).amount < 1:
        await build_twilight_council(self)
    if self.units(UnitTypeId.STALKER).amount < 4:
        await warp_stalker(self)
    if self.structures(UnitTypeId.DARKSHRINE).amount < 1:
        await build_dark_shrine(self)
    if self.units(UnitTypeId.DARKTEMPLAR).amount < 2:
        await warp_darktemplar(self)
    if self.units(UnitTypeId.DARKTEMPLAR).amount == 2:
        await attack(self)
        return True
    return False


async def defend(self):
    """
    defend: This tactic is primarily used to defend, using stalker and shield battery
    Tactic Overview：nothing
    Tactic Characteristics: Used to defend against an opponent's allin, or to suppress
    Tactic Advantages: It can be used to defend any situation
    Tactic Disadvantages： may affect economic development due to excessive defense
    """
    game_loop = self.state.game_loop
    # 转换游戏时间为秒数
    game_time_seconds = game_loop / 22.4
    await build_pylon(self)
    if self.structures(UnitTypeId.CYBERNETICSCORE).amount < 1:
        await build_cyberneticscore(self)
    await update_warp_gate(self)
    if self.structures(UnitTypeId.ASSIMILATOR).amount < 2:
        await build_assimilators(self)
    if self.units(UnitTypeId.STALKER).amount < (game_time_seconds / 30):
        await warp_stalker(self)
    if self.structures(UnitTypeId.GATEWAY).amount < 4 and self.structures(UnitTypeId.WARPGATE).amount < 4:
        await build_gateway(self)
    if self.structures(UnitTypeId.SHIELDBATTERY).amount < self.structures(UnitTypeId.NEXUS).amount:
        await build_shield_battery(self)
    if self.structures(UnitTypeId.SHIELDBATTERY).amount == self.structures(UnitTypeId.NEXUS).amount and self.units(
            UnitTypeId.STALKER).amount >= (game_time_seconds / 30):
        return True
    return False


async def rapid_economic_development(self):
    """
    rapid_economic_development: This tactic is suitable for rapid economic development.
    Tactic Overview: Building a new NEXUS marks the end of this tactic.
    Tactic Characteristics: Rapid economic development, building Probes.
    Tactic Advantages: Allows for rapid economic development, thus having more resources to build a powerful army after the tactic ends.
    Tactic Disadvantages: Cannot withstand harassment and pressure from the enemy. If the opponent uses an ALL-in tactic, then we might fail.
    """
    await build_pylon(self)
    if self.structures(UnitTypeId.GATEWAY).amount < 2 and self.structures(UnitTypeId.WARPGATE).amount < 2:
        await build_gateway(self)
    if self.structures(UnitTypeId.CYBERNETICSCORE).amount < 1:
        await build_cyberneticscore(self)
    if self.units(UnitTypeId.PROBE).amount < 60:
        await build_worker(self)
    await build_assimilators(self)
    if  self.units(UnitTypeId.PROBE).amount >self.structures(UnitTypeId.NEXUS).amount * 22:
        await build_nexus(self)
        return True
    if self.structures(UnitTypeId.TWILIGHTCOUNCIL).amount < 1:
        await build_twilight_council(self)
    await update_warp_gate(self)
    cybernetics_core = self.structures(UnitTypeId.NEXUS).random  # 选择第一个控制核心
    await chronoboostenergycost(self, cybernetics_core)
    return False
