import csv
import json
import os
from typing import Dict, List


def save_csv(rows: List[Dict], output_dir: str, file_name: str = "weibo.csv") -> None:
    if not rows:
        print("没有可保存的数据。")
        return

    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, file_name)
    fieldnames = list(rows[0].keys())
    with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"已保存到 {file_path}，共 {len(rows)} 条。")


def save_json(rows: List[Dict], output_dir: str, file_name: str = "weibo.json") -> None:
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(rows, file, ensure_ascii=False, indent=2)
    print(f"已保存到 {file_path}。")
