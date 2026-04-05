from typing import Dict, List


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
