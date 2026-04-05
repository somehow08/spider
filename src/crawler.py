import time
from typing import Dict, List

from .client import fetch_page
from .parser import parse_cards


def crawl_weibo(
    keyword: str,
    headers: Dict[str, str],
    max_pages: int = 5,
    sleep_sec: float = 2.0,
    max_retries: int = 2,
    timeout: int = 15,
) -> List[Dict]:
    all_rows: List[Dict] = []
    empty_page_streak = 0

    for page in range(1, max_pages + 1):
        success = False
        for attempt in range(1, max_retries + 2):
            try:
                data, meta = fetch_page(
                    keyword=keyword,
                    page=page,
                    headers=headers,
                    timeout=timeout,
                )
                rows = parse_cards(data)
                cards_count = len(data.get("data", {}).get("cards", []))
                ok = data.get("ok")
                msg = data.get("msg", "")

                if not rows:
                    empty_page_streak += 1
                    print(
                        f"第 {page} 页无数据，连续空页 {empty_page_streak}/3。"
                        f" ok={ok}, msg={msg}, cards={cards_count},"
                        f" content_type={meta['content_type']}, url={meta['final_url']}"
                    )
                    if empty_page_streak >= 3:
                        print("连续 3 页无数据，结束抓取。")
                        return all_rows
                    success = True
                    break

                empty_page_streak = 0
                all_rows.extend(rows)
                print(f"第 {page} 页抓取成功，新增 {len(rows)} 条。")
                success = True
                break
            except Exception as exc:
                print(f"第 {page} 页第 {attempt} 次失败: {exc}")
                time.sleep(sleep_sec * attempt)

        if not success:
            print(f"第 {page} 页重试后仍失败，跳过。")

        time.sleep(sleep_sec)

    return all_rows
