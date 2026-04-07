time="2026-04-01"
author="Chen Mingze"

from .config import CrawlSettings, DEFAULT_HEADERS, OUTPUT_DIR
from .crawler import crawl_weibo
from .storage import save_csv, save_json
from .validators import validate_cookie


def run(settings: CrawlSettings) -> None:
    headers = dict(DEFAULT_HEADERS)

    try:
        headers["Cookie"] = validate_cookie(headers.get("Cookie", ""))
    except ValueError as exc:
        print(f"Cookie 配置错误: {exc}")
        return

    print(f"开始抓取关键词: {settings.keyword}")
    rows = crawl_weibo(
        keyword=settings.keyword,
        headers=headers,
        max_pages=settings.max_pages,
        sleep_sec=settings.sleep_sec,
        max_retries=settings.max_retries,
        timeout=settings.timeout,
    )

    save_csv(rows, output_dir=OUTPUT_DIR)
    save_json(rows, output_dir=OUTPUT_DIR)


def main() -> None:
    settings = CrawlSettings(
        keyword="",  # 输入你想搜索的关键词
        max_pages=10,
        sleep_sec=2.0,
        max_retries=2,
        timeout=15,
    )
    run(settings)


if __name__ == "__main__":
    main()
