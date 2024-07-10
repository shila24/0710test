import asyncio
from mavsdk import System

async def run():
  drone = System()
  await drone.connect(system_address="serial:///dev/ttyACM0:115200")
  status_text_task = asyncio.ensure_future(print_status_text(drone))
  print("Waiting for drone to connect...")
  async for state in drone.core.connection_state():
    if state.is_connected:
      print(f"-- Connected to drone!")
      break
async def print_status_text(drone):
  try:
      async for status_text in drone.telemetry.status_text():
        print(f"Status: {status_text.type}: {status_text.text}")
  except asyncio.CancelledError:
      return

if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  loop.run_until_complete(run())