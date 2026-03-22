import argparse
import asyncio
import json
import time
from pathlib import Path

import httpx


async def fetch_all(base_url: str, paths_file: str, output_dir: str):
    paths = [line.strip() for line in Path(paths_file).read_text().splitlines() if line.strip()]
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    start = time.perf_counter()

    async with httpx.AsyncClient(http2=True, verify=False, timeout=30.0) as client:
        async def fetch_one(path: str):
            url = f"{base_url}{path}"
            response = await client.get(url)
            response.raise_for_status()
            data = response.content
            outfile = out_dir / Path(path).name
            outfile.write_bytes(data)
            return {
                "path": path,
                "bytes": len(data),
                "protocol": response.http_version,
            }

        results = await asyncio.gather(*(fetch_one(p) for p in paths))

    end = time.perf_counter()

    total_bytes = sum(r["bytes"] for r in results)
    protocol = results[0]["protocol"] if results else "HTTP/2"

    print(json.dumps({
        "success": True,
        "elapsed_ms": (end - start) * 1000.0,
        "bytes_total": total_bytes,
        "protocol": protocol,
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