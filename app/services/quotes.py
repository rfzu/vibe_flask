"""Котировки с Московской биржи (MOEX ISS API)."""
import urllib.request
import json
import ssl

MOEX_URL = "https://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}.json"
PARAMS = "?iss.only=marketdata&marketdata.columns=SECID,LAST,OPEN,LOW,HIGH,BOARDID"

# Тикеры: Сбербанк, Совкомбанк
TICKERS = {"SBER": "Сбербанк", "SVCB": "Совкомбанк"}


def fetch_quote(ticker: str) -> dict | None:
    """Получить котировку по тикеру с MOEX."""
    url = (MOEX_URL + PARAMS).format(ticker=ticker)
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(url, headers={"User-Agent": "VibeFlask/1.0"})
        with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
            data = json.load(resp)
    except Exception:
        return None

    md = data.get("marketdata", {})
    columns = md.get("columns", [])
    rows = md.get("data", [])
    if not rows:
        return None

    # Берём первую строку (основная площадка)
    row = rows[0]
    out = {"ticker": ticker, "name": TICKERS.get(ticker, ticker)}
    for i, col in enumerate(columns):
        if i < len(row) and row[i] is not None:
            out[col.lower()] = row[i]
    return out


def get_all_quotes() -> list[dict]:
    """Котировки Сбера и Совкомбанка."""
    result = []
    for ticker in TICKERS:
        q = fetch_quote(ticker)
        if q:
            result.append(q)
        else:
            result.append({
                "ticker": ticker,
                "name": TICKERS[ticker],
                "last": None,
                "open": None,
                "error": "Не удалось загрузить",
            })
    return result
