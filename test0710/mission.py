import asyncio
from logger import logger_info, logger_debug
import csv
import datetime
from mavsdk import System
from mavsdk.mission import (MissionItem, MissionPlan)

center = [35.797379299999996, 139.8922272]
north_m = 5
south_m = -5
lat_deg_per_m = 0.000008983148616
lng_deg_per_m = 0.000008983668124


async def run():
    drone = System()
    await drone.connect(system_address="serial:///dev/ttyACM0:115200")

    logger_info.info("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            logger_info.info(f"-- Connected to drone!")
            break
    print_mission_progress_task = asyncio.ensure_future(
        print_mission_progress(drone))
    
    logger_info.info(f"-- starting mission upload...")
    
    running_tasks = [print_mission_progress_task]
    termination_task = asyncio.ensure_future(observe_is_in_air(drone, running_tasks))
    waypoint1 = [center[0] + lat_deg_per_m * north_m, center[1]]
    waypoint2 = [center[0] + lat_deg_per_m * south_m, center[1]]

    mission_items = []
    mission_items.append(MissionItem(waypoint1[0],
                                     waypoint1[1],
                                     3,
                                     5,
                                     True,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.NONE,
                                     float('nan'),
                                     float('nan'),
                                     float('nan'),
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.VehicleAction.NONE))
    mission_items.append(MissionItem(waypoint2[0],
                                     waypoint2[1],
                                     3,
                                     5,
                                     True,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.NONE,
                                     float('nan'),
                                     float('nan'),
                                     float('nan'),
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.VehicleAction.NONE))

    mission_plan = MissionPlan(mission_items)

    await drone.mission.set_return_to_launch_after_mission(True)

    logger_info.info("-- Uploading mission")
    await drone.mission.upload_mission(mission_plan)

    logger_info.info("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            logger_info.info("-- Global position estimate OK")
            break

    logger_info.info("-- Arming")
    await drone.action.arm()

    logger_info.info("-- Starting mission")
    await drone.mission.start_mission()

    await termination_task


async def print_mission_progress(drone):
    async for mission_progress in drone.mission.mission_progress():
        print(f"Mission progress: "
              f"{mission_progress.current}/"
              f"{mission_progress.total}")
        logger_info.info(f"Mission progress: "
              f"{mission_progress.current}/"
              f"{mission_progress.total}")


async def observe_is_in_air(drone, running_tasks):
    """ Monitors whether the drone is flying or not and
    returns after landing """

    was_in_air = False

    async for is_in_air in drone.telemetry.in_air():
        if is_in_air:
            was_in_air = is_in_air

        if was_in_air and not is_in_air:
            for task in running_tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            await asyncio.get_event_loop().shutdown_asyncgens()

            return


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())
