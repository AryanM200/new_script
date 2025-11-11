#!/usr/bin/env python3
import asyncio
import aioari
import logging
import concurrent.futures
import requests
from lxml import etree
from html import escape
from gi.repository import GLib, Gst

logging.basicConfig(level=logging.INFO)

ARI_URL = "http://127.0.0.1:8088/ari"
ARI_USER = "asterisk"
ARI_PASS = "asterisk"
ARI_APP = "app1"

# Cisco phone settings
CISCO_PHONE = "172.16.160.55"
CISCO_USER = "test"
CISCO_PASS = "test"

WAV_FILE = "/home/moon/BRC-Paging-Test-1.wav"
PORT = 20480
TIMEOUT = 3


class CiscoController:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def send_xml(self, hostname, xml):
        try:
            resp = requests.post(
                f"http://{hostname}/CGI/Execute",
                auth=requests.auth.HTTPBasicAuth(self.username, self.password),
                data={"XML": xml},
                timeout=TIMEOUT
            )
            if resp.status_code != 200:
                logging.error(f"CGI error {hostname}: {resp.status_code}")
            return resp.content
        except Exception as e:
            logging.error(f"Error sending XML to {hostname}: {e}")
            return None

    def start_rtp(self, hostname, port):
        url = f"RTPRx:{hostname}:{port}"
        xml = f"""<?xml version="1.0"?>
        <CiscoIPPhoneExecute>
            <ExecuteItem URL="{escape(url)}" Priority="0"/>
        </CiscoIPPhoneExecute>"""
        self.send_xml(hostname, xml)

    def stop_rtp(self, hostname):
        xml = """<?xml version="1.0"?>
        <CiscoIPPhoneExecute>
            <ExecuteItem URL="RTPRx:Stop" Priority="0"/>
        </CiscoIPPhoneExecute>"""
        self.send_xml(hostname, xml)


def stream_rtp(hostname, port, wav_file):
    Gst.init(None)
    pipeline_str = (
        f"filesrc location={wav_file} ! wavparse ! audioconvert ! audioresample "
        f"! audio/x-raw,channels=1,rate=8000 ! mulawenc ! rtppcmupay pt=0 "
        f"! udpsink host={hostname} port={port} sync=true"
    )
    pipeline = Gst.parse_launch(pipeline_str)
    pipeline.set_state(Gst.State.PLAYING)
    logging.info(f"Streaming {wav_file} to {hostname}:{port}")
    bus = pipeline.get_bus()
    msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.EOS)
    pipeline.set_state(Gst.State.NULL)


async def on_stasis_start(channel, event, ari_client):
    logging.info(f"Incoming call: {channel.json.get('name')}")
    cisco = CiscoController(CISCO_USER, CISCO_PASS)
    cisco.start_rtp(CISCO_PHONE, PORT)
    await asyncio.sleep(1)
    await asyncio.to_thread(stream_rtp, CISCO_PHONE, PORT, WAV_FILE)
    cisco.stop_rtp(CISCO_PHONE)
    await channel.hangup()


async def main():
    client = await aioari.connect(ARI_URL, ARI_USER, ARI_PASS)

    async for event in client.on_event("StasisStart"):
        channel = event.get("channel")
        await on_stasis_start(await client.channels.get(channel["id"]), event, client)


if __name__ == "__main__":
    asyncio.run(main())
