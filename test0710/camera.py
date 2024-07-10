import asyncio
from mavsdk import System
from logger_drone import logger_info, logger_debug
import asyncio
from picamera import PiCamera
from datetime import datetime

async def capture_image(camera, count):
    for i in range(count):
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'/home/pi/Pictures/image_{timestamp}.jpg'
        camera.capture(filename)
        logger_info.info(f'Captured {filename}')
        await asyncio.sleep(30)
    camera.close()
    logger_info.info('Camera closed')

async def main():
    camera = PiCamera()
    capture_task = asyncio.create_task(capture_image(camera, 5))
    # メイン関数が終了しないように無限ループを追加
    while not capture_task.done():
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())


