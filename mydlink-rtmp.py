import aiohttp
import asyncio
import logging
import re
import sys
import websockets

access_token = sys.argv[1]
camera_id = sys.argv[2]

logger = logging.getLogger('websockets')
# logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

stream_url = f"https://mp-eu-openapi.auto.mydlink.com/v2/device/live/stream?access_token={access_token}"

headers = {
    "Origin": "https://se.mydlink.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
}


async def socketRead(reader, writer, websocket, url):
    while True:
        data = await reader.readuntil(b'\r\n\r\n')
        print('----------  socket -> websocket')
        try:
            text = data.decode('utf8')
            if "CSeq: 1" in text:
                text = re.sub(r'rtsp://([^\s]+)', url, text)
            if "CSeq: 2" in text:
                text = re.sub(r'rtsp://([^\s]+)', url, text)
            data = text.encode("utf8")
        except BaseException:
            pass

        try:
            print(data.decode('utf8'))
        except e as err:
            print(data)

        try:
            await websocket.send(data)
        except BaseException:
            writer.close()
            websocket.close()


async def onConnect(reader, writer):
    url = ""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            stream_url,
            headers={"content-type": "application/json"},
            json={"data": {"mydlink_id": camera_id, "uid": 0, "idx": 0}}
        ) as res:
            jsonres = await res.json()
            url = jsonres["data"]["rtsp_url"]
            print('url', url)

    async with websockets.connect(url.replace('rtsp://', 'wss://'), subprotocols=["rtsp"], extra_headers=headers) as websocket:
        asyncio.create_task(socketRead(reader, writer, websocket, url))
        while True:
            data = await websocket.recv()
            print('---------- websocket -> socket')
            try:
                print(data.decode('utf8'))
            except BaseException:
                print(len(data))

            try:
                writer.write(data)
            except BaseException:
                websocket.close()
                write.close()


async def main():
    server = await asyncio.start_server(host="0.0.0.0", port=4444, client_connected_cb=onConnect)
    await server.serve_forever()

asyncio.run(main())
