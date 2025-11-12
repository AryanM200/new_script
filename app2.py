#!/usr/bin/env python3
import asyncio
import aioari
import subprocess
import logging

logging.basicConfig(level=logging.INFO)

ARI_URL = "http://127.0.0.1:8088/ari"
ARI_USER = "asterisk"
ARI_PASS = "asterisk"
APP_NAME = "app2"

async def on_stasis_start(channel, event):
    logging.info(f"Channel {channel.id} entered Stasis")

    # Run your RTP transmit command
    cmd = [
        "/usr/bin/python3",
        "/var/lib/asterisk/agi-bin/rtptransmit",
        "-f", "/home/moon/BRC-Paging-Test-1.wav",
        "-u", "test",
        "-p", "test",
        "172.16.160.55"
    ]

    logging.info(f"Running RTP script: {' '.join(cmd)}")
    subprocess.Popen(cmd)

    # Optionally play audio, log, or hang up
    await asyncio.sleep(10)
    await channel.hangup()

async def main():
    client = await aioari.connect(ARI_URL, username=ARI_USER, password=ARI_PASS)
    client.on_channel_event('StasisStart', on_stasis_start)
    await client.run(APP_NAME)

if __name__ == "__main__":
    asyncio.run(main())
