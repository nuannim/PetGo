import os
import json
from datetime import datetime
from typing import Any, Dict, List

import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")


def _format_alert(alert: Dict[str, Any]) -> str:
    status = alert.get("status") or alert.get("state", "")
    labels = alert.get("labels", {})
    annotations = alert.get("annotations", {})
    rule_name = labels.get("alertname") or labels.get("rule_name") or "Alert"
    severity = labels.get("severity", "info")
    summary = annotations.get("summary") or annotations.get("description") or ""
    starts_at = alert.get("startsAt") or alert.get("starts_at")
    generator = alert.get("generatorURL") or ""

    ts = None
    if starts_at:
        try:
            ts = datetime.fromisoformat(starts_at.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S UTC")
        except Exception:
            ts = starts_at

    parts = [
        f"[{status.upper()}] {rule_name} (severity: {severity})",
    ]
    if summary:
        parts.append(summary)
    if ts:
        parts.append(f"since: {ts}")
    if generator:
        parts.append(f"source: {generator}")

    label_kv = [f"{k}={v}" for k, v in labels.items() if k not in {"alertname", "severity"}]
    if label_kv:
        parts.append("labels: " + ", ".join(label_kv[:6]))

    msg = "\n".join(parts)
    return msg[:1900]


def _post_to_discord(content: str) -> requests.Response:
    if not DISCORD_WEBHOOK_URL:
        raise RuntimeError("DISCORD_WEBHOOK_URL is not set")
    payload = {"content": content}
    headers = {"Content-Type": "application/json"}
    return requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(payload), headers=headers, timeout=10)


@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        alerts: List[Dict[str, Any]] = data.get("alerts") or data.get("evalMatches") or []
        if not isinstance(alerts, list):
            alerts = [data]

        messages = [_format_alert(a) for a in alerts]
        content = "\n\n".join(messages) if messages else "Received alert"

        resp = _post_to_discord(content)
        if resp.status_code >= 400:
            return JSONResponse(status_code=502, content={"ok": False, "error": resp.text})
        return JSONResponse(status_code=200, content={"ok": True})
    except Exception as e:
        return JSONResponse(status_code=500, content={"ok": False, "error": str(e)})


@app.get("/health")
async def health():
    return JSONResponse(status_code=200, content={"status": "ok"})