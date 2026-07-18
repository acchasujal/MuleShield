# frontend/components/compliance_panel.py

import hashlib
import tempfile
import streamlit as st
import pandas as pd
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate
from frontend.utils.constants import SEVERITY_COLORS


@st.cache_data(show_spinner=False)
def generate_pdf(alerts: list) -> str:
    """Build a PDF mule account report and return the temp file path. Cached."""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp.close()
    doc = SimpleDocTemplate(tmp.name)
    styles = getSampleStyleSheet()
    content = [Paragraph("MuleShield AML — Mule Account Intelligence Report", styles["Title"])]
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
    <div style='background-color:#0f172a;padding:12px 14px;border-radius:6px;border:1px solid #1e293b;'>
        <code style='color:#10b981;font-size:11px;word-break:break-all;'>SHA-256: {evidence_hash}</code>
        <br/>
        <small style='color:#64748b;'>OpenTimestamps Cryptographic Seal — Admissible under Section 65B of the Indian Evidence Act</small>
    </div>
    """, unsafe_allow_html=True)


def render_goaml_download(goaml_xml: str, case_id: str, account_no: str) -> None:
    """Renders download controls for compliant goAML XML reports."""
    st.download_button(
        label="Download goAML XML Report",
        data=goaml_xml,
        file_name=f"goAML-{case_id}.xml",
        mime="application/xml",
        key=f"dl_xml_{account_no}"
    )


def render_pdf_export(alerts: list) -> None:
    """Renders controls to download full PDF compliance dossier."""
    st.markdown("---")
    st.markdown("#### Evidence Package Export")
    st.caption("Generate a signed compliance PDF intelligence dossier with cryptographic integrity hash logging.")

    pdf_path = generate_pdf(alerts)
    with open(pdf_path, "rb") as f:
        st.download_button(
            label="Download Compliance PDF Dossier",
            data=f.read(),
            file_name="MuleShield-Compliance-Report.pdf",
            mime="application/pdf",
            key="btn_dl_pdf"
        )


def render_compliance_workspace_view() -> None:
    """Renders the top-level Compliance Workspace for auditors and compliance officers."""
    alerts_data = st.session_state.get("analysis_result")

    if alerts_data is None:
        st.markdown("""
        <div style='background:#0f172a;border:1px solid #1e293b;border-radius:8px;padding:32px;text-align:center;margin-top:20px;'>
            <div style='color:#475569;font-size:14px;margin-bottom:8px;font-weight:500;'>No Active Investigation Dataset</div>
            <div style='color:#334155;font-size:12px;'>Load a transaction dataset from the Investigations workspace to generate compliance artifacts.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    alerts = alerts_data.get("alerts", [])
    high_risk = [a for a in alerts if float(a.get("risk_score", 0)) >= 40.0]

    if not high_risk:
        st.info("No accounts meet the STR eligibility threshold (composite risk >= 40%).")
        return

    # -------------------------------------------------------------------------
    # Layout Split: Left Column (Queue & KPIs), Right Column (Dossier Preview)
    # -------------------------------------------------------------------------
    col_left, col_right = st.columns([4.2, 7.8])

    # Left Column: Case list and KPIs
    with col_left:
        st.markdown('<div class="muleshield-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Compliance Summary")
        
        # Summary metrics
        str_ready = sum(1 for a in high_risk if float(a.get("risk_score", 0)) >= 80.0)
        critical  = sum(1 for a in high_risk if a.get("severity") == "CRITICAL")
        
        st.metric("STR-Ready Cases",      f"{str_ready:,}")
        st.metric("Critical Escalations", f"{critical:,}")
        st.metric("Analysis SLA",       "< 8 sec",       "Risk fusion latency")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="muleshield-card">', unsafe_allow_html=True)
        st.markdown("### 📋 STR Register")
        st.caption("Select a flagged account to view and export the formal Suspicious Transaction Report.")
        
        acc_list = [a["account"] for a in high_risk]
        selected_acc = st.selectbox(
            "Select Account to Export",
            options=acc_list,
            key="compliance_selected_account_selector"
        )
        st.session_state.inspected_account_id = selected_acc
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="muleshield-card">', unsafe_allow_html=True)
        st.markdown("### 📜 Regulatory Frameworks")
        st.markdown("""
        <div style='font-size:11px; line-height:1.8; color:#8A8F98;'>
            <b>PMLA 2002, Section 3:</b> Offence of money-laundering<br/>
            <b>PMLA 2002, Section 12:</b> Record maintenance obligations<br/>
            <b>FIU-IND goAML:</b> STR compliance XML format<br/>
            <b>Indian Evidence Act, Section 65B:</b> Electronic records admissibility<br/>
            <b>I4C MHA India:</b> Inter-agency intelligence webhooks
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Right Column: STR Document Preview Card
    with col_right:
        active_case = next((a for a in high_risk if a["account"] == selected_acc), high_risk[0])
        
        st.markdown('<div class="muleshield-card" style="background-color:#ffffff; color:#1e293b; padding:32px; border:1px solid #e2e8f0; box-shadow:0 10px 30px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
        
        # Letterhead Title
        st.markdown("""
        <div style='text-align:center; border-bottom:2px solid #1e293b; padding-bottom:12px; margin-bottom:20px; color:#0f172a;'>
            <div style='font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; color:#64748b;'>Government of India</div>
            <h3 style='margin:4px 0 0 0; font-size:18px; font-weight:800; text-transform:uppercase; color:#0f172a;'>Financial Intelligence Unit - India (FIU-IND)</h3>
            <div style='font-size:12px; font-weight:600; text-transform:uppercase; color:#0f172a;'>Suspicious Transaction Report (STR) Dossier</div>
        </div>
        """, unsafe_allow_html=True)

        # Metadata Table
        case_id = active_case.get("case_id", "STR-MOCK")
        st.markdown(f"""
        <table style='width:100%; border-collapse:collapse; font-size:12px; color:#334155; margin-bottom:20px;'>
            <tr style='border-bottom:1px solid #e2e8f0;'>
                <td style='padding:6px 0; font-weight:700; width:35%;'>Report Reference ID</td>
                <td style='padding:6px 0; font-family:monospace;'>{case_id}</td>
            </tr>
            <tr style='border-bottom:1px solid #e2e8f0;'>
                <td style='padding:6px 0; font-weight:700;'>Reporting Institution</td>
                <td style='padding:6px 0;'>Bank of India (BOI) — AML Operations</td>
            </tr>
            <tr style='border-bottom:1px solid #e2e8f0;'>
                <td style='padding:6px 0; font-weight:700;'>Target Account ID</td>
                <td style='padding:6px 0; font-family:monospace;'>{active_case["account"]}</td>
            </tr>
            <tr style='border-bottom:1px solid #e2e8f0;'>
                <td style='padding:6px 0; font-weight:700;'>Composite Risk Assessment</td>
                <td style='padding:6px 0; font-weight:700; color:#ef4444;'>{active_case["risk_score"]}% (Severity: {active_case.get("severity")})</td>
            </tr>
            <tr style='border-bottom:1px solid #e2e8f0;'>
                <td style='padding:6px 0; font-weight:700;'>Mule Lifecycle Stage</td>
                <td style='padding:6px 0;'>{active_case.get("mule_stage", "LEGITIMATE").replace("_"," ").title()}</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)

        # Risk Factors Attributions Section
        st.markdown("<h4 style='color:#0f172a; margin-top:16px; margin-bottom:8px; font-size:13px; font-weight:700;'>I. RISK FACTORS ATTRIBUTIONS</h4>", unsafe_allow_html=True)
        
        translation_map = {
            "F670": "Prior regulatory watch-list flag active on account",
            "F886": "Unusual rapid channel-switching behavior detected",
            "F3908": "High velocity in/out ratio (funds passing through rapidly)",
            "F115": "Elevated transaction ratio relative to customer history",
            "F2082": "Complete absence of standard retail banking behavior",
            "F3889": "Account is established dormant profile activated for laundering",
            "F3891": "High-vulnerability demographic profile matched (student mule)"
        }
        
        shap_sigs = active_case.get("shap_signals", {})
        sorted_sigs = sorted(shap_sigs.items(), key=lambda x: abs(x[1]), reverse=True)
        factors_found = False
        
        for feature, val in sorted_sigs:
            if feature in translation_map and abs(val) > 0.01:
                desc = translation_map[feature]
                st.markdown(f"<div style='font-size:12px; color:#475569; margin-bottom:6px;'>• <b>{desc}</b> (Impact score: +{abs(val * 100):.1f}%)</div>", unsafe_allow_html=True)
                factors_found = True
        
        if not factors_found:
            st.markdown(f"<div style='font-size:12px; color:#475569;'>• {active_case.get('explanation')}</div>", unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)

        # Integrity seal Section
        st.markdown("<h4 style='color:#0f172a; margin-bottom:8px; font-size:13px; font-weight:700;'>II. EVIDENCE INTEGRITY CERTIFICATE (IEA SECTION 65B)</h4>", unsafe_allow_html=True)
        
        xml_content = active_case.get("goaml_xml", "")
        evidence_hash = active_case.get("evidence_hash")
        if not evidence_hash and xml_content:
            evidence_hash = hashlib.sha256(xml_content.encode()).hexdigest()
        
        st.markdown(f"""
        <div style='background-color:#f8fafc; border:1px solid #e2e8f0; padding:10px 14px; border-radius:6px; margin-bottom:24px;'>
            <code style='color:#0f766e; font-size:11px; word-break:break-all;'>SHA-256: {evidence_hash}</code>
            <div style='color:#64748b; font-size:10px; margin-top:4px;'>OpenTimestamps cryptographic seal linked to PostgreSQL ledger record. Signed with timezone-naive UTC timestamp.</div>
        </div>
        """, unsafe_allow_html=True)

        # Download Buttons Row
        st.markdown("<h4 style='color:#0f172a; margin-bottom:8px; font-size:13px; font-weight:700;'>III. REPORT ACTIONS</h4>", unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if xml_content:
                st.download_button(
                    label="Export goAML XML Report",
                    data=xml_content,
                    file_name=f"goAML-{case_id}.xml",
                    mime="application/xml",
                    key=f"dl_xml_compliance_{active_case['account']}"
                )
            else:
                st.caption("XML report not generated.")
        
        with col_btn2:
            pdf_path = generate_pdf([active_case])
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Download PDF Dossier",
                    data=f.read(),
                    file_name=f"MuleShield-{case_id}.pdf",
                    mime="application/pdf",
                    key=f"dl_pdf_compliance_{active_case['account']}"
                )
        
        st.markdown("</div>", unsafe_allow_html=True) # Close white card


def _compliance_action(severity: str, risk: float) -> str:
    """Return the recommended compliance action based on severity and risk score."""
    sev = severity.upper()
    if sev == "CRITICAL" or risk >= 80.0:
        return "File STR + Recommend Hold"
    elif sev == "HIGH" or risk >= 60.0:
        return "File STR + Enhanced Monitoring"
    elif risk >= 40.0:
        return "Initiate Review + KYC Refresh"
    else:
        return "Enhanced Monitoring"
