from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Header
from pydantic import BaseModel

from database import get_connection
from routes.study_leads import _check_admin_key

router = APIRouter()

PAGES = {"inicio", "privacidad"}
SOURCES = {"facebook", "instagram", "google", "whatsapp", "tiktok", "directo", "otros"}
BOT_WORDS = ("bot", "crawl", "spider", "preview", "headless", "facebookexternalhit")


def _today() -> str:
    try:
        from zoneinfo import ZoneInfo

        now = datetime.now(ZoneInfo("Europe/Madrid"))
    except Exception:
        now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d")


class VisitRequest(BaseModel):
    page: str = "inicio"
    source: str = "directo"


@router.post("/visit")
def register_visit(request: VisitRequest, user_agent: str | None = Header(default=None)):
    # Sin cookies, sin IP: se suma 1 a un contador por día, página y origen.
    if user_agent and any(word in user_agent.lower() for word in BOT_WORDS):
        return {"status": "ignored"}

    page = request.page if request.page in PAGES else "inicio"
    source = request.source.lower() if request.source.lower() in SOURCES else "otros"

    connection = get_connection()
    connection.execute(
        """
        INSERT INTO visits (day, page, source, count) VALUES (?, ?, ?, 1)
        ON CONFLICT(day, page, source) DO UPDATE SET count = count + 1
        """,
        (_today(), page, source),
    )
    connection.commit()
    connection.close()

    return {"status": "ok"}


@router.get("/visits")
def visits_summary(key: str | None = None, days: int = 30):
    _check_admin_key(key)
    days = max(1, min(days, 365))

    today = datetime.strptime(_today(), "%Y-%m-%d")
    first = (today - timedelta(days=days - 1)).strftime("%Y-%m-%d")

    connection = get_connection()
    rows = connection.execute(
        "SELECT day, page, source, count FROM visits WHERE day >= ?", (first,)
    ).fetchall()
    connection.close()

    by_day = {}
    by_source = {}
    by_page = {}
    for row in rows:
        by_day[row["day"]] = by_day.get(row["day"], 0) + row["count"]
        by_source[row["source"]] = by_source.get(row["source"], 0) + row["count"]
        by_page[row["page"]] = by_page.get(row["page"], 0) + row["count"]

    daily = []
    for i in range(days):
        day = (today - timedelta(days=days - 1 - i)).strftime("%Y-%m-%d")
        daily.append({"day": day, "count": by_day.get(day, 0)})

    def last(n: int) -> int:
        return sum(d["count"] for d in daily[-n:])

    return {
        "today": last(1),
        "last_7": last(7),
        "total": sum(by_day.values()),
        "days": days,
        "daily": daily,
        "sources": sorted(
            ({"source": k, "count": v} for k, v in by_source.items()),
            key=lambda x: -x["count"],
        ),
        "pages": sorted(
            ({"page": k, "count": v} for k, v in by_page.items()),
            key=lambda x: -x["count"],
        ),
    }
