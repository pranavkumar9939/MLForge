from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.deps import require_admin
from app.database.database import get_db
from app.database.models import PageView, User

router = APIRouter(prefix="/analytics", tags=["Analytics"])


class PageViewRequest(BaseModel):
    path: str
    visitor_id: str
    referrer: str | None = None


@router.post("/pageview")
def record_pageview(request: PageViewRequest, db: Session = Depends(get_db)):
    """
    Records one page load. Deliberately has no auth requirement - visitors
    browsing the landing page or login screen haven't logged in yet, and
    tracking only logged-in traffic would make the numbers meaningless.
    Never raises on bad input; a broken tracking call should never break
    the page it's tracking.
    """
    try:
        db.add(PageView(
            path=request.path[:255],
            visitor_id=request.visitor_id[:64],
            referrer=(request.referrer or "")[:255] or None,
        ))
        db.commit()
    except Exception:
        db.rollback()
    return {"ok": True}


@router.get("/summary")
def get_summary(days: int = 30, db: Session = Depends(get_db), _admin: User = Depends(require_admin)):
    """
    Admin-only. Total views, unique visitors, a daily time series for the
    requested window, and the most-visited pages.
    """
    since = datetime.utcnow() - timedelta(days=days)

    total_views = db.query(func.count(PageView.id)).filter(PageView.created_at >= since).scalar() or 0

    unique_visitors = (
        db.query(func.count(func.distinct(PageView.visitor_id)))
        .filter(PageView.created_at >= since)
        .scalar() or 0
    )

    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    views_today = db.query(func.count(PageView.id)).filter(PageView.created_at >= today_start).scalar() or 0

    daily_rows = (
        db.query(
            func.date(PageView.created_at).label("day"),
            func.count(PageView.id).label("views"),
            func.count(func.distinct(PageView.visitor_id)).label("visitors"),
        )
        .filter(PageView.created_at >= since)
        .group_by(func.date(PageView.created_at))
        .order_by(func.date(PageView.created_at))
        .all()
    )

    top_pages_rows = (
        db.query(PageView.path, func.count(PageView.id).label("views"))
        .filter(PageView.created_at >= since)
        .group_by(PageView.path)
        .order_by(func.count(PageView.id).desc())
        .limit(10)
        .all()
    )

    return {
        "window_days": days,
        "total_views": total_views,
        "unique_visitors": unique_visitors,
        "views_today": views_today,
        "daily": [{"date": str(row.day), "views": row.views, "visitors": row.visitors} for row in daily_rows],
        "top_pages": [{"path": row.path, "views": row.views} for row in top_pages_rows],
    }