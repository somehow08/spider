time="2026-04-01"
author="Chen Mingze"

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
