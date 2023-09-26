import asyncio

from bleak import BleakScanner, BleakClient

DEVICE_NAME = 'M02 Pro'
CHARACTERISTIC_UUID_WRITE = '0000ff02-0000-1000-8000-00805f9b34fb'


async def main():
    # scan and connect
    print('scanning for 5 seconds, please wait...')
    device = await BleakScanner.find_device_by_name(
        name=DEVICE_NAME
    )
    if device:
        print('connected.')
    else:
        print('device not found.')
        return

    # print
    async with BleakClient(device) as client:
        await feed(client, 1)

    print('disconnect.')


async def feed(client: BleakClient, line: int = 1):
    await client.write_gatt_char(
        char_specifier=CHARACTERISTIC_UUID_WRITE,
        data=b'\x1b\x64' + line.to_bytes(1, 'little')
    )


if __name__ == "__main__":
    asyncio.run(main())
