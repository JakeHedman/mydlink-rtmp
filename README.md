# mydlink rtmp

Connect to video stream from dlink cloud using rtmp.

## Usage

Get access token from https://eu.mydlink.com/ (view source).

Get access token from https://eu.mydlink.com/ (in URL when viewing camera).

Install dependencies

```sh
pip install aiohttp websockets
```

Start server

```sh
python dlinkrtmp.py your-access-token camera-id
```

View stream
```sh
mpv rtsp://localhost:4444
```
