from typing import Dict, Tuple

import requests

from .config import API_URL


def response_preview(text: str, max_len: int = 180) -> str:
    return text.replace("\n", " ").replace("\r", " ")[:max_len]


def fetch_page(
    keyword: str,
    page: int,
    headers: Dict[str, str],
    timeout: int = 15,
) -> Tuple[Dict, Dict]:
    params = {
        "containerid": f"100103type=1&q={keyword}",
        "page_type": "searchall",
        "page": page,
    }
    response = requests.get(API_URL, headers=headers, params=params, timeout=timeout)
    response.raise_for_status()

    meta = {
        "status": response.status_code,
        "content_type": response.headers.get("content-type", ""),
        "final_url": response.url,
        "preview": response_preview(response.text),
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
