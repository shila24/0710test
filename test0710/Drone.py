import asyncio
from mavsdk import System
from  logger_drone import logger_info, log_file_

async def run():
    # Connect to the drone
    drone = System()
    await drone.connect(system_address="serial:///dev/ttyACM0:115200")
    status_text_task = asyncio.ensure_future(print_status_text(drone))
    logger_info.info("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
      if state.is_connected:
        logger_info.info(f"-- Connected to drone!")
        break
    #ttyACM0が rasberrypi to pixhawk、 ボーレート115200
      logger_info.info("conected")

    # Get the list of parameters
    all_params = await drone.param.get_all_params()

    # Iterate through all int parameters
    for param in all_params.int_params:
        logger_info.info(f"{param.name}: {param.value}")

    for param in all_params.float_params:
        logger_info.info(f"{param.name}: {param.value}")

if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  loop.run_until_complete(run())	