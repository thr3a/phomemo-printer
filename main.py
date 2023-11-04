import asyncio
from typing import Optional

from bleak import BleakScanner, BleakClient, BLEDevice

from bitmap_generator import text_to_bitmap

DEVICE_NAME = 'M02 Pro'
CHARACTERISTIC_UUID_WRITE = '0000ff02-0000-1000-8000-00805f9b34fb'

CONNECTION_RETRY_MAX_COUNT = 5

ESC = b'\x1b'
GS = b'\x1d'
COMMAND_FEED_PAPER = ESC + b'd'  # ESC d
COMMAND_INIT_PRINTER = ESC + b'@' + b'\x1f\x11\x02\x04'  # ESC @ + init params(Probably M02 specifications)
COMMAND_PRINT_RASTER_IMAGE = GS + b'v0'  # GS v0

# 1 line = 72 bytes x 8 bit = 576 dots
DOT_PER_LINE = 576
BYTE_PER_LINE = 72


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
        await init_printer(client=client)
        await print_text(client=client, text='Hello Phomemo M02Pro!', fontsize=24)
        await feed(client=client, line=3)
        # wait a little to avoid disconnect
        await asyncio.sleep(2)

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


async def init_printer(client: BleakClient):
    print(f'init printer: {client.address}')
    await send_command(client=client, command_data=COMMAND_INIT_PRINTER)


async def print_line(client: BleakClient, line_height: int = 1):
    print('print line')

    # send print command (GS v0)
    command = COMMAND_PRINT_RASTER_IMAGE \
              + int(0).to_bytes(1, byteorder="little") \
              + int(BYTE_PER_LINE).to_bytes(2, byteorder="little") \
              + int(line_height).to_bytes(2, byteorder="little")
    await send_command(client=client, command_data=command)

    # send print data
    line_data = bytearray([0xff] * BYTE_PER_LINE * line_height)
    await send_command(client=client, command_data=line_data)


async def print_text(client: BleakClient, text: str, fontsize: int = 24):
    print('print text')

    # generate text bitmap
    bitmap_data = text_to_bitmap(text=text, fontsize=fontsize)

    # send print command (GS v0)
    command = COMMAND_PRINT_RASTER_IMAGE \
              + int(0).to_bytes(1, byteorder="little") \
              + int(BYTE_PER_LINE).to_bytes(2, byteorder="little") \
              + int(bitmap_data.height).to_bytes(2, byteorder="little")
    await send_command(client=client, command_data=command)

    # send print data
    await send_command(client=client, command_data=bitmap_data.bitmap)


async def feed(client: BleakClient, line: int = 1):
    print(f'feed paper: {line} lines')
    command = COMMAND_FEED_PAPER + line.to_bytes(1, 'little')
    await send_command(client=client, command_data=command)


async def send_command(client: BleakClient, command_data):
    await client.write_gatt_char(char_specifier=CHARACTERISTIC_UUID_WRITE, data=command_data, response=True)


if __name__ == "__main__":
    asyncio.run(main())
