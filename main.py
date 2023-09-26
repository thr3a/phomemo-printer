import asyncio
from typing import Optional

from bleak import BleakScanner, BleakClient, BLEDevice

DEVICE_NAME = 'M02 Pro'
CHARACTERISTIC_UUID_WRITE = '0000ff02-0000-1000-8000-00805f9b34fb'

CONNECTION_RETRY_MAX_COUNT = 5

ESC = b'\x1B'
COMMAND_FEED_PAPER = ESC + b'd'  # ESC d


async def main():
    # scan and connect
    device = await connect()
    if device:
        print('connected.')
    else:
        print('device not found.')
        return

    # print
    async with BleakClient(device) as client:
        await feed(client, 1)

    print('disconnect.')


async def connect() -> Optional[BLEDevice]:
    retry_count = 0
    device = None
    while not device and retry_count < CONNECTION_RETRY_MAX_COUNT:
        print(f'scanning device, please wait... ({retry_count + 1}/{CONNECTION_RETRY_MAX_COUNT})')
        device = await BleakScanner.find_device_by_name(
            name=DEVICE_NAME
        )
        retry_count += 1

    return device


async def feed(client: BleakClient, line: int = 1):
    print(f'feed paper: {line} lines')
    await client.write_gatt_char(
        char_specifier=CHARACTERISTIC_UUID_WRITE,
        data=COMMAND_FEED_PAPER + line.to_bytes(1, 'little')
    )


if __name__ == "__main__":
    asyncio.run(main())
