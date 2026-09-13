import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable,
)

from app.services.reporting.chart_images import (
    feature_importance_chart, confusion_matrix_chart, roc_curve_chart,
)

EMBER = colors.HexColor("#c4501f")
EMBER_STRONG = colors.HexColor("#a63f16")
INK = colors.HexColor("#201d18")
MUTED = colors.HexColor("#63594c")
BORDER = colors.HexColor("#e4e1d8")
WASH = colors.HexColor("#fbf1e8")
HEADER_BG = colors.HexColor("#f2f0ea")


def _styles():
    ss = getSampleStyleSheet()
    ss.add(ParagraphStyle("MFTitle", parent=ss["Heading1"], fontSize=20, textColor=INK, spaceAfter=2))
    ss.add(ParagraphStyle("MFSubtitle", parent=ss["Normal"], fontSize=10, textColor=MUTED, spaceAfter=16))
    ss.add(ParagraphStyle("MFBrand", parent=ss["Normal"], fontSize=11, textColor=INK, spaceAfter=6))
    ss.add(ParagraphStyle("MFH2", parent=ss["Heading2"], fontSize=13, textColor=INK, spaceBefore=18, spaceAfter=8))
    ss.add(ParagraphStyle("MFBody", parent=ss["Normal"], fontSize=9.5, textColor=INK))
    ss.add(ParagraphStyle("MFFooter", parent=ss["Normal"], fontSize=8, textColor=MUTED))
    return ss


def _image_flowable(png_bytes: bytes, max_width_mm=150) -> Image:
    img = Image(io.BytesIO(png_bytes))
    aspect = img.imageHeight / img.imageWidth
    img.drawWidth = max_width_mm * mm
    img.drawHeight = max_width_mm * mm * aspect
    return img


def _leaderboard_table(data: dict, styles) -> Table:
    is_reg = data["is_regression"]
    if is_reg:
        header = ["Rank", "Model", "R\u00b2", "MAE", "RMSE", "Status"]
    else:
        header = ["Rank", "Model", "Accuracy", "Precision", "Recall", "F1", "Status"]

    rows = [header]
    best_row_index = None
    for i, m in enumerate(data["leaderboard"], start=1):
        if m["model_name"] == data["best_model"]:
            best_row_index = i
        if is_reg:
            rows.append([str(m["rank"]), m["model_name"], f"{m['r2_score']:.3f}", f"{m['mae']:.3f}", f"{m['rmse']:.3f}", m["status"]])
        else:
            rows.append([str(m["rank"]), m["model_name"], f"{m['accuracy']:.1f}%", f"{m['precision']:.1f}%", f"{m['recall']:.1f}%", f"{m['f1_score']:.1f}%", m["status"]])

    table = Table(rows, hAlign="LEFT", repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), MUTED),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, BORDER),
        ("LINEBELOW", (0, 1), (-1, -1), 0.5, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]
    if best_row_index is not None:
        style.append(("BACKGROUND", (0, best_row_index), (-1, best_row_index), WASH))
        style.append(("FONTNAME", (0, best_row_index), (-1, best_row_index), "Helvetica-Bold"))
    table.setStyle(TableStyle(style))
    return table


def _metrics_table(data: dict) -> Table:
    m = data["metrics"]
    if data["is_regression"]:
        pairs = [("R\u00b2 Score", f"{m['r2_score'] * 100:.1f}%"), ("MAE", f"{m['mae']:.3f}"),
                 ("RMSE", f"{m['rmse']:.3f}"), ("Status", m["status"])]
    else:
        pairs = [("Accuracy", f"{m['accuracy']:.1f}%"), ("Precision", f"{m['precision']:.1f}%"),
                 ("Recall", f"{m['recall']:.1f}%"), ("F1 Score", f"{m['f1_score']:.1f}%")]

    row = [[Paragraph(f'<font size=14 color="#a63f16"><b>{v}</b></font><br/><font size=8 color="#63594c">{k}</font>', getSampleStyleSheet()["Normal"]) for k, v in pairs]]
    table = Table(row, hAlign="LEFT", colWidths=[35 * mm] * len(pairs))
    table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    return table


def render_pdf_report(data: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=22 * mm, bottomMargin=18 * mm, leftMargin=20 * mm, rightMargin=20 * mm,
    )
    styles = _styles()
    story = []

    story.append(Paragraph('ML<font color="#c4501f">Forge</font>', styles["MFBrand"]))
    story.append(Paragraph(data["display_name"], styles["MFTitle"]))
    story.append(Paragraph(f"{data['problem_type']} &middot; Model report", styles["MFSubtitle"]))
    story.append(HRFlowable(width="100%", thickness=1.2, color=INK, spaceAfter=14))

    meta_rows = [
        ["Target column", data["target_column"], "Best model", data["best_model"]],
        ["Algorithm", str(data["algorithm"]), "Feature count", str(data["feature_count"])],
        ["Models compared", str(len(data["leaderboard"])), "Training date", str(data["training_date"])],
    ]
    meta_table = Table(meta_rows, colWidths=[32 * mm, 50 * mm, 32 * mm, 50 * mm])
    meta_table.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (0, -1), MUTED),
        ("TEXTCOLOR", (2, 0), (2, -1), MUTED),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
        ("FONTNAME", (3, 0), (3, -1), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(meta_table)

    story.append(Paragraph("Best Model Performance", styles["MFH2"]))
    story.append(_metrics_table(data))

    story.append(Paragraph("Model Leaderboard", styles["MFH2"]))
    story.append(_leaderboard_table(data, styles))

    story.append(Paragraph("Feature Importance", styles["MFH2"]))
    fi_bytes = feature_importance_chart(data["feature_importance"])
    if fi_bytes:
        story.append(_image_flowable(fi_bytes))
    else:
        story.append(Paragraph(
            f"{data['best_model']} does not expose a feature-importance score "
            f"(only tree-based and linear models do).",
            styles["MFBody"],
        ))

    if not data["is_regression"] and data["confusion_matrix"]:
        story.append(Paragraph("Confusion Matrix", styles["MFH2"]))
        story.append(_image_flowable(confusion_matrix_chart(data["confusion_matrix"]), max_width_mm=110))

    if not data["is_regression"] and data["roc_curve"]:
        story.append(Paragraph("ROC Curve", styles["MFH2"]))
        story.append(_image_flowable(roc_curve_chart(data["roc_curve"]), max_width_mm=120))

    if data["tuning"] and data["tuning"].get("tuned"):
        story.append(Paragraph("Hyperparameter Tuning", styles["MFH2"]))
        cv_score = data["tuning"].get("best_cv_score")
        score_text = f"{cv_score * 100:.2f}%" if cv_score is not None else "N/A"
        story.append(Paragraph(f"Best cross-validated score: <b>{score_text}</b>", styles["MFBody"]))
        story.append(Spacer(1, 4))
        for k, v in data["tuning"]["best_params"].items():
            story.append(Paragraph(f"&bull; <font face='Courier'>{k}</font>: {v}", styles["MFBody"]))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=8))
    story.append(Paragraph("Generated by MLForge — Forge your data into intelligence. Developed by Pranav Kumar.", styles["MFFooter"]))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()
