
from pathlib import Path
from client_runner import fetch_workload

def main():
    # 先只测 3 个小文件，方便快速验证
    paths = [
        "/many_small/obj_000.bin",
        "/many_small/obj_001.bin",
        "/many_small/obj_002.bin",
    ]

    output_dir = "./results/test_download"
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    result = fetch_workload(
        base_url="https://127.0.0.1:8443",
        paths=paths,
        protocol="h2",
        output_dir=output_dir,
    )

    print("Test result:")
    for k, v in result.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()