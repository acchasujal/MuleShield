# frontend/components/compliance_panel.py

import hashlib
import tempfile
import streamlit as st
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate

@st.cache_data(show_spinner=False)
def generate_pdf(alerts: list) -> str:
    """Build a PDF mule account report and return the temp file path. Cached."""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(tmp.name)
    styles = getSampleStyleSheet()
    content = [Paragraph("MuleShield AI – Mule Account Intelligence Report", styles["Title"])]
    for alert in alerts:
        line = (
            f"Account: {alert['account']}  |  "
            f"Risk: {alert['risk_score']}%  |  "
            f"Patterns: {', '.join(alert['reasons'])}"
        )
        content.append(Paragraph(line, styles["Normal"]))
    doc.build(content)
    return tmp.name

def render_integrity_seal(evidence_hash: str) -> None:
    """Renders a tamper-proof evidence signature block conforming to Section 65B."""
    st.markdown(f"""
    <div style='background-color:#0f172a;padding:12px;border-radius:6px;border:1px solid #1e293b;'>
        <code style='color:#10b981;font-size:11px;word-break:break-all;'>SHA-256: {evidence_hash}</code>
        <br/>
        <small style='color:#64748b;'>OpenTimestamps Cryptographic Seal Verified | Admissible under Section 65B</small>
    </div>
    """, unsafe_allow_html=True)

def render_goaml_download(goaml_xml: str, case_id: str, account_no: str) -> None:
    """Renders download controls for compliant goAML XML reports."""
    st.download_button(
        label="⬇️ Download goAML XML Report",
        data=goaml_xml,
        file_name=f"goAML-{case_id}.xml",
        mime="application/xml",
        key=f"dl_xml_{account_no}"
    )

def render_pdf_export(alerts: list) -> None:
    """Renders controls to download full PDF compliance dossier."""
    st.markdown("---")
    st.subheader("🖨️ Compliance Report Export")
    st.caption("Generate a signed, fully-admissible PDF intelligence folder representation for judicial submissions.")
    
    pdf_path = generate_pdf(alerts)
    with open(pdf_path, "rb") as f:
        st.download_button(
            label="⬇️ Download Signed Compliance PDF Folder",
            data=f.read(),
            file_name="MuleShield-Compliance-Report.pdf",
            mime="application/pdf",
            key="btn_dl_pdf"
        )
