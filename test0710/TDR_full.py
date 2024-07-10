import asyncio
from mavsdk import System
from logger_drone import logger_info, logger_debug
import RPi.GPIO as GPIO

# GPIO ピンの設定
PIN_LIST = [11, 13]  # 使用するGPIOピンのリスト
RUN_TIME = 4
SLEEP_TIME = 20
LOOP_COUNT = 1  # ループ回数を設定

async def control_mosfets(loop_count):
    GPIO.setmode(GPIO.BOARD)
    for pin in PIN_LIST:
        GPIO.setup(pin, GPIO.OUT)
    
    try:
        for _ in range(loop_count):
            for pin in PIN_LIST:
                GPIO.output(pin, GPIO.HIGH)  # MOSFETをONにする
                logger_info.info(f"Turned ON MOSFET on pin {pin}")
                await asyncio.sleep(RUN_TIME)  # RUN_TIME秒
                GPIO.output(pin, GPIO.LOW)  # MOSFETをOFFにする
                logger_info.info(f"Turned OFF MOSFET on pin {pin}")
                await asyncio.sleep(SLEEP_TIME)  # SLEEP_TIME秒
    finally:
        GPIO.cleanup()

async def run():
    await control_mosfets(lLOOP_COUNT)
    logger_info.info(f"Palacute has been released!!")

    drone = System()
    await drone.connect(system_address="serial:///dev/ttyACM0:115200")

    status_text_task = asyncio.ensure_future(print_status_text(drone))

    logger_info.info("Start takeoff_and_land_altitude.")
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

    status_text_task.cancel()

if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())
