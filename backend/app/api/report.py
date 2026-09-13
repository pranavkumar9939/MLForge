from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
import io

from app.core.deps import get_current_user
from app.core.ownership import require_owner
from app.database.models import User
from app.services.reporting.report_data import build_report_data
from app.services.reporting.html_report import render_html_report
from app.services.reporting.pdf_report import render_pdf_report

router = APIRouter(prefix="/report", tags=["Reports"])


@router.get("/{dataset_name}/html", response_class=HTMLResponse)
def get_html_report(dataset_name: str, model_name: str | None = None, current_user: User = Depends(get_current_user)):
    """
    Render a styled, self-contained HTML report for the dataset's best
    model (or a specific model, if `model_name` is given). Viewable
    directly in the browser.
    """
    require_owner(dataset_name, current_user.id)

    data = build_report_data(dataset_name, model_name)
    if data is None:
        raise HTTPException(status_code=404, detail="No trained models found for this dataset.")

    return HTMLResponse(content=render_html_report(data))


@router.get("/{dataset_name}/pdf")
def get_pdf_report(dataset_name: str, model_name: str | None = None, current_user: User = Depends(get_current_user)):
    """
    Download a PDF version of the same report - same underlying data and
    charts as the HTML version, laid out for printing/sharing.
    """
    require_owner(dataset_name, current_user.id)

    data = build_report_data(dataset_name, model_name)
    if data is None:
        raise HTTPException(status_code=404, detail="No trained models found for this dataset.")

    pdf_bytes = render_pdf_report(data)

    filename = f"{data['display_name']}_report.pdf"

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
