time="2026-04-01"
author="Chen Mingze"

import csv
import json
import os
import time
from typing import Dict, List, Tuple

import requests


HEADERS = {
	"User-Agent": (
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
		"AppleWebKit/537.36 (KHTML, like Gecko) "
		"Chrome/124.0.0.0 Safari/537.36"
	),
	"Referer": "https://m.weibo.cn/",
	"Cookie": "",
}#Cookie 需要替换成登录 Cookie，保持登录状态才能抓取到数据。

API_URL = "https://m.weibo.cn/api/container/getIndex"
OUTPUT_DIR = ""#输出目录，请根据需要修改。


def validate_cookie(cookie: str) -> str:
	if not cookie or not cookie.strip():
		raise ValueError("Cookie 为空，请填入浏览器复制的完整 Cookie 值。")

	cookie = cookie.strip()
	if cookie.lower().startswith("cookie:"):
		raise ValueError("不要包含前缀 'Cookie:'，只保留分号连接的键值对。")

	if "\r" in cookie or "\n" in cookie:
		raise ValueError("Cookie 中包含换行符，请删除换行后重试。")

	try:
		cookie.encode("latin-1")
	except UnicodeEncodeError:
		illegal_chars = [
			f"{char}(U+{ord(char):04X})"
			for char in cookie
			if ord(char) > 255 or ord(char) < 32 or ord(char) == 127
		]
		preview = ", ".join(illegal_chars[:5]) if illegal_chars else "未知字符"
		raise ValueError(
			"Cookie 含非法字符，通常是中文符号或不可见控制字符。"
			f" 示例: {preview}"
		) from None

	return cookie


def _response_preview(text: str, max_len: int = 180) -> str:
	return text.replace("\n", " ").replace("\r", " ")[:max_len]


def fetch_page(keyword: str, page: int, timeout: int = 15) -> Tuple[Dict, Dict]:
	params = {
		"containerid": f"100103type=1&q={keyword}",
		"page_type": "searchall",
		"page": page,
	}
	response = requests.get(API_URL, headers=HEADERS, params=params, timeout=timeout)
	response.raise_for_status()

	meta = {
		"status": response.status_code,
		"content_type": response.headers.get("content-type", ""),
		"final_url": response.url,
		"preview": _response_preview(response.text),
	}

	if "json" not in meta["content_type"].lower():
		raise ValueError(
			"接口返回非 JSON，可能是登录失效或风控拦截。"
			f" status={meta['status']}, content_type={meta['content_type']},"
			f" url={meta['final_url']}, preview={meta['preview']}"
		)

	try:
		data = response.json()
	except ValueError as exc:
		raise ValueError(
			"JSON 解析失败，返回内容可能异常。"
			f" status={meta['status']}, content_type={meta['content_type']},"
			f" url={meta['final_url']}, preview={meta['preview']}"
		) from exc

	return data, meta


def parse_cards(data: Dict) -> List[Dict]:
	rows: List[Dict] = []
	cards = data.get("data", {}).get("cards", [])

	stack: List[Dict] = list(cards)
	while stack:
		card = stack.pop(0)

		if not isinstance(card, dict):
			continue

		card_group = card.get("card_group", [])
		if isinstance(card_group, list) and card_group:
			stack.extend(card_group)

		mblog = card.get("mblog")
		if not mblog:
			continue

		user = mblog.get("user", {})
		rows.append(
			{
				"id": mblog.get("id"),
				"text_raw": mblog.get("text_raw") or "",
				"created_at": mblog.get("created_at"),
				"reposts_count": mblog.get("reposts_count"),
				"comments_count": mblog.get("comments_count"),
				"attitudes_count": mblog.get("attitudes_count"),
				"user_id": user.get("id"),
				"screen_name": user.get("screen_name"),
				"source": mblog.get("source"),
			}
		)

	return rows


def crawl_weibo(
	keyword: str,
	max_pages: int = 5,
	sleep_sec: float = 2.0,
	max_retries: int = 2,
) -> List[Dict]:
	all_rows: List[Dict] = []
	empty_page_streak = 0

	for page in range(1, max_pages + 1):
		success = False
		for attempt in range(1, max_retries + 2):
			try:
				data, meta = fetch_page(keyword=keyword, page=page)
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


def save_csv(rows: List[Dict], file_name: str = "weibo.csv") -> None:
	if not rows:
		print("没有可保存的数据。")
		return

	os.makedirs(OUTPUT_DIR, exist_ok=True)
	file_path = os.path.join(OUTPUT_DIR, file_name)
	fieldnames = list(rows[0].keys())
	with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(rows)

	print(f"已保存到 {file_path}，共 {len(rows)} 条。")


def save_json(rows: List[Dict], file_name: str = "weibo.json") -> None:
	os.makedirs(OUTPUT_DIR, exist_ok=True)
	file_path = os.path.join(OUTPUT_DIR, file_name)
	with open(file_path, "w", encoding="utf-8") as file:
		json.dump(rows, file, ensure_ascii=False, indent=2)
	print(f"已保存到 {file_path}。")


def main() -> None:
	keyword = ""#输入你想搜索的关键词
	max_pages = 10

	try:
		HEADERS["Cookie"] = validate_cookie(HEADERS.get("Cookie", ""))
	except ValueError as exc:
		print(f"Cookie 配置错误: {exc}")
		return

	print(f"开始抓取关键词: {keyword}")
	rows = crawl_weibo(keyword=keyword, max_pages=max_pages, sleep_sec=2)

	save_csv(rows)
	save_json(rows)


if __name__ == "__main__":
	main()
