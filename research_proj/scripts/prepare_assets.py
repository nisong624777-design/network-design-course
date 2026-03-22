# scripts/prepare_assets.py
from pathlib import Path
import os


def make_file(path: Path, size_bytes: int):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        f.write(os.urandom(size_bytes))


def main():
    base = Path("./static")
    many_small = []
    few_large = []

    for i in range(300):
        p = base / "many_small" / f"obj_{i:03d}.bin"
        make_file(p, 10 * 1024)   # 10 KB
        many_small.append("/many_small/" + p.name)

    for i in range(10):
        p = base / "few_large" / f"obj_{i:03d}.bin"
        make_file(p, 1024 * 1024)  # 1 MB
        few_large.append("/few_large/" + p.name)

    Path("./configs").mkdir(exist_ok=True)
    Path("./configs/many_small.txt").write_text("\n".join(many_small), encoding="utf-8")
    Path("./configs/few_large.txt").write_text("\n".join(few_large), encoding="utf-8")


if __name__ == "__main__":
    main()