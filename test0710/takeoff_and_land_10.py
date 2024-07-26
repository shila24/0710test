import asyncio
from mavsdk import System
from logger_drone import logger_info, logger_debug

async def run():    
    drone = System()
    await drone.connect(system_address="serial:///dev/ttyACM0:115200")
    logger_info.info("Start takeoff_and_land.")
    logger_info.info("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            logger_info.info(f"-- Connected to drone!")
            break

    logger_info.info("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            logger_info.info("-- Global position estimate OK")
            break

    logger_info.info("-- Arming")
    await drone.action.arm()

    logger_info.info("-- Taking off")
    await drone.action.takeoff()

    await asyncio.sleep(10)

    logger_info.info("-- Landing")
    await drone.action.land()
    logger_info.info("-- Landed")

if __name__ == "__main__":
    # Run the asyncio loop
    try:
      asyncio.run(run())

    except KeyboardInterrupt:
      await drone.action.kill()
      logger_info.info("Program interrupted by user (Ctrl+C)")
