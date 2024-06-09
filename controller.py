import asyncio
import keyboard
from bleak import BleakClient


raspberry_pi_address = "DC:A6:32:B0:B1:CD"


async def send_command(command):
    async with BleakClient(raspberry_pi_address) as client:
        try:
            await client.connect()
            await client.write_gatt_char("0000ffe1-0000-1000-8000-00805f9b34fb", bytes(command, 'utf-8'))
            print(f"Sent command: {command}")
        except Exception as e:
            print(f"Error occurred: {e}")


async def main():
    is_w_pressed = False
    is_s_pressed = False
    is_a_pressed = False
    is_d_pressed = False

    while True:
        if keyboard.is_pressed("w"):
            if not is_w_pressed:
                is_w_pressed = True
                await send_command("w")
        else:
            if is_w_pressed:
                is_w_pressed = False
                await send_command("stop")

        if keyboard.is_pressed("s"):
            if not is_s_pressed:
                is_s_pressed = True
                await send_command("s")
        else:
            if is_s_pressed:
                is_s_pressed = False
                await send_command("stop")

        if keyboard.is_pressed("a"):
            if not is_a_pressed:
                is_a_pressed = True
                await send_command("a")
        else:
            if is_a_pressed:
                is_a_pressed = False
                await send_command("stop")

        if keyboard.is_pressed("d"):
            if not is_d_pressed:
                is_d_pressed = True
                await send_command("d")
        else:
            if is_d_pressed:
                is_d_pressed = False
                await send_command("stop")

        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())
