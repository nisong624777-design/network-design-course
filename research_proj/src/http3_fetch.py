import argparse
import asyncio
import json
import ssl
import time
from pathlib import Path
from urllib.parse import urlparse

from aioquic.asyncio.client import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.h3.connection import H3_ALPN, H3Connection
from aioquic.h3.events import DataReceived, HeadersReceived
from aioquic.quic.configuration import QuicConfiguration


class HttpClientProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._http = H3Connection(self._quic)
        self._events = {}

    async def get(self, url: str) -> bytes:
        parsed = urlparse(url)
        authority = parsed.netloc
        path = parsed.path or "/"
        if parsed.query:
            path += "?" + parsed.query

        stream_id = self._quic.get_next_available_stream_id()
        self._events[stream_id] = {
            "body": bytearray(),
            "done": asyncio.Event(),
        }

        self._http.send_headers(
            stream_id=stream_id,
            headers=[
                (b":method", b"GET"),
                (b":scheme", parsed.scheme.encode()),
                (b":authority", authority.encode()),
                (b":path", path.encode()),
                (b"user-agent", b"aioquic-client"),
            ],
            end_stream=True,
        )
        self.transmit()

        await self._events[stream_id]["done"].wait()
        return bytes(self._events[stream_id]["body"])

    def http_event_received(self, event) -> None:
        if isinstance(event, DataReceived):
            self._events[event.stream_id]["body"] += event.data
            if event.stream_ended:
                self._events[event.stream_id]["done"].set()

    def quic_event_received(self, event) -> None:
        super().quic_event_received(event)
        for http_event in self._http.handle_event(event):
            self.http_event_received(http_event)


async def fetch_all(base_url: str, paths_file: str, output_dir: str):
    paths = [line.strip() for line in Path(paths_file).read_text().splitlines() if line.strip()]
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    parsed = urlparse(base_url)

    configuration = QuicConfiguration(
        is_client=True,
        alpn_protocols=H3_ALPN,
        verify_mode=ssl.CERT_NONE,
    )
    configuration.server_name = parsed.hostname

    start = time.perf_counter()

    async with connect(
        host=parsed.hostname,
        port=parsed.port or 443,
        configuration=configuration,
        create_protocol=HttpClientProtocol,
        wait_connected=True,
    ) as client:

        async def fetch_one(path: str):
            url = f"{base_url}{path}"
            body = await client.get(url)
            outfile = out_dir / Path(path).name
            outfile.write_bytes(body)
            return {
                "path": path,
                "bytes": len(body),
                "protocol": "h3",
            }

        results = await asyncio.gather(*(fetch_one(p) for p in paths))

    end = time.perf_counter()

    total_bytes = sum(r["bytes"] for r in results)

    print(json.dumps({
        "success": True,
        "elapsed_ms": (end - start) * 1000.0,
        "bytes_total": total_bytes,
        "protocol": "h3",
        "object_count": len(results),
    }))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--paths-file", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    asyncio.run(fetch_all(args.base_url, args.paths_file, args.output_dir))


if __name__ == "__main__":
    main()