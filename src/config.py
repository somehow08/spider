import os
from dataclasses import dataclass


API_URL = "https://m.weibo.cn/api/container/getIndex"
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer": "https://m.weibo.cn/",
    "Cookie": "",
}

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")


@dataclass
class CrawlSettings:
    keyword: str = ""
    max_pages: int = 10
    sleep_sec: float = 2.0
    max_retries: int = 2
    timeout: int = 15
