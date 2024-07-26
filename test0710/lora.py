import RPi.GPIO as GPIO
import serial
import asyncio
import struct


class Lora:
    def __init__(self):
        # pin number
        # reset,pinofraspi
        self.rst = 17
        # Vin
        self.power = 4

        # 改行文字
        self.CRLF = "\r\n"
        # massage received from PC on ground
        self.msg_received = "hello, world"
        # serial,uartのttyのやつかく
        self.serial = serial.Serial("/dev/ttyS0", 9600, timeout=None)
                # power
        self.is_on = False
        # is out of carrier?
        self.is_out = False
        #self.is_sending = False
        
        self.counter = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.rst, GPIO.OUT)
        GPIO.setup(self.power, GPIO.OUT)


    async def change_status(self):
        """start lora"""
        GPIO.output(self.power, GPIO.HIGH)

        GPIO.output(self.rst, GPIO.LOW)
        await asyncio.sleep(2)
                print("lora power on")
        #await self.write("processor")
        await self.write("start")

        self.is_on = True

    async def write(self, message: str) -> None:
        #         self.is_sending = True
        msg_send = str(message) + self.CRLF
        self.serial.write(msg_send.encode("ascii"))
        await asyncio.sleep(4)

    #         self.is_sending = False
#以下よくわかってない
    async def read(self) -> None:
        """clear header and read lora"""
        data = self.serial.readline()
        fmt = "4s4s4s" + str(len(data) - 14) + "sxx"  # rssi, rcvidが両方onの時>

        try:
            line = struct.unpack(fmt, data)
            self.msg_received = line[3].decode("ascii")
            await asyncio.sleep(1)
        except struct.error:
            await asyncio.sleep(1)