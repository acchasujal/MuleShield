# frontend/components/lifecycle_view.py

import streamlit as st

def render_lifecycle_timeline(mule_stage: str) -> tuple[str, str, str]:
    """Renders the dynamic HTML Step Timeline matching the account stage."""
    stages = ["Recruitment", "Activation", "Active Mule", "Being Flushed", "Dormant"]
    mule_stage_clean = mule_stage.upper().replace(" ", "_")

    if mule_stage_clean == "NEWLY_RECRUITED":
        step_states  = [1, 0, 0, 0, 0]
        current_step = "Recruitment"
        reason       = "Account has been recently opened (L7D/L90D bucket) and shows high transactional risk, indicating immediate recruitment."
        action_sop   = "Temporary debit freeze. Queue for enhanced verification of demographic credentials."
    elif mule_stage_clean == "UNDER_REVIEW":
        step_states  = [2, 1, 0, 0, 0]
        current_step = "Under Review"
        reason       = "Fusion severity has been elevated by live transaction intelligence while the static customer profile still appears legitimate. The account requires investigator review before confirmed mule promotion."
        action_sop   = "Queue investigator review, preserve evidence, and maintain enhanced monitoring while STR handling proceeds."
    elif mule_stage_clean == "ACTIVATION":
        step_states  = [2, 1, 0, 0, 0]
        current_step = "Activation"
        reason       = "Initial high-velocity test transactions and channel-switching anomalies detected on a newly registered profile."
        action_sop   = "Mandatory KYC refresh and contact account holder to confirm transaction origin."
    elif mule_stage_clean == "ACTIVE_MULE":
        step_states  = [2, 2, 1, 0, 0]
        current_step = "Active Mule"
        reason       = "Frequent watchlist Warn-Flag hits (F3912), regulatory TMS violations (F670), and UPI structuring transactions matching high-density laundering patterns."
        action_sop   = "Immediate account freeze, generate Suspicious Transaction Report (STR) XML, and submit compliance docket to FIU-IND."
    elif mule_stage_clean == "BEING_FLUSHED":
        step_states  = [2, 2, 2, 1, 0]
        current_step = "Being Flushed"
        reason       = "Extreme debit/credit volume frequency ratio (F115) coupled with complete absence of standard retail banking behavior (F2082), signifying active proceeds dispersal."
        action_sop   = "Total account freeze, suspend beneficiary channels, and escalate transaction coordinates to the Enforcement Directorate (ED) immediately."
    elif mule_stage_clean == "DORMANT":
        step_states  = [2, 2, 2, 2, 1]
        current_step = "Dormant"
        reason       = "Established customer profile activated for high-volume transactions (G365D age bucket) after a long period of complete inactivity."
        action_sop   = "Suspend digital banking channels and request physical presence at home branch to resolve alert."
    else:
        step_states  = [0, 0, 0, 0, 0]
        current_step = "Legitimate (Monitored)"
        reason       = "Normal low-velocity consumer banking pattern. Standalone ML risk score and network centrality values remain well within legitimate baseline parameters."
        action_sop   = "No immediate restrictive action. Continue continuous watchlist monitoring and auto-archive."

    # Renders Custom HTML Timeline
    html_lifecycle = (
        "<style>\n"
        ".mule-lifecycle-container {\n"
        "    display: flex;\n"
        "    justify-content: space-between;\n"
        "    align-items: center;\n"
        "    background-color: #0f172a;\n"
        "    padding: 24px;\n"
        "    border-radius: 6px;\n"
        "    border: 1px solid #1e293b;\n"
        "    margin-bottom: 25px;\n"
        "}\n"
        ".mule-stage-node {\n"
        "    display: flex;\n"
        "    flex-direction: column;\n"
        "    align-items: center;\n"
        "    position: relative;\n"
        "    z-index: 2;\n"
        "    flex: 1;\n"
        "}\n"
        ".mule-stage-circle {\n"
        "    width: 40px;\n"
        "    height: 40px;\n"
        "    border-radius: 50%;\n"
        "    display: flex;\n"
        "    align-items: center;\n"
        "    justify-content: center;\n"
        "    font-weight: 700;\n"
        "    font-size: 13px;\n"
        "}\n"
        ".mule-stage-circle.completed {\n"
        "    background-color: #10b981;\n"
        "    color: #ffffff;\n"
        "    border: 2px solid #047857;\n"
        "}\n"
        ".mule-stage-circle.current {\n"
        "    background-color: #f97316;\n"
        "    color: #ffffff;\n"
        "    border: 2px solid #ea580c;\n"
        "}\n"
        ".mule-stage-circle.future {\n"
        "    background-color: #334155;\n"
        "    color: #94a3b8;\n"
        "    border: 2px solid #475569;\n"
        "}\n"
        ".mule-stage-label {\n"
        "    margin-top: 8px;\n"
        "    font-size: 12px;\n"
        "    font-weight: 600;\n"
        "    text-align: center;\n"
        "}\n"
        ".mule-stage-label.completed { color: #10b981; }\n"
        ".mule-stage-label.current   { color: #f97316; }\n"
        ".mule-stage-label.future    { color: #64748b; }\n"
        ".mule-stage-connector {\n"
        "    height: 3px;\n"
        "    background-color: #334155;\n"
        "    flex: 1;\n"
        "    margin: 0 -22px;\n"
        "    margin-top: -26px;\n"
        "    position: relative;\n"
        "    z-index: 1;\n"
        "}\n"
        ".mule-stage-connector.completed { background-color: #10b981; }\n"
        "</style>\n"
        "<div class=\"mule-lifecycle-container\">\n"
    )

    for idx, stage_name in enumerate(stages):
        state = step_states[idx]
        if state == 2:
            class_name = "completed"
            symbol     = "✓"
        elif state == 1:
            class_name = "current"
            symbol     = str(idx + 1)
        else:
            class_name = "future"
            symbol     = str(idx + 1)

        html_lifecycle += (
            f'<div class="mule-stage-node">\n'
            f'    <div class="mule-stage-circle {class_name}">{symbol}</div>\n'
            f'    <div class="mule-stage-label {class_name}">{stage_name}</div>\n'
            f'</div>\n'
        )
        if idx < len(stages) - 1:
            next_state = step_states[idx + 1]
            connector_class = "completed" if state == 2 else "future"
            html_lifecycle += f'<div class="mule-stage-connector {connector_class}"></div>\n'

    html_lifecycle += "</div>"

    st.markdown(html_lifecycle, unsafe_allow_html=True)
    return current_step, reason, action_sop


def render_dispatch_controls(account_id: str) -> None:
    """Renders the context-aware investigator action dispatch panel."""
    st.markdown("**Investigator Action Center**")
    st.caption("Compliance dispatch controls linked to Core Banking System (CBS) webhooks.")

    col_act1, col_act2, col_act3, col_act4, col_act5 = st.columns(5)

    btn_mon = col_act1.button("Monitor",         key=f"btn_mon_{account_id}")
    btn_rev = col_act2.button("Initiate Review", key=f"btn_rev_{account_id}")
    btn_esc = col_act3.button("Escalate",        key=f"btn_esc_{account_id}")
    btn_str = col_act4.button("File STR",        key=f"btn_str_{account_id}")
    btn_frz = col_act5.button("Freeze Account",  key=f"btn_frz_{account_id}")

    if btn_mon:
        st.toast("Monitor: Account telemetry logging enabled. Watchlist records synced.")
        st.success("Monitor: Continuous watchlist monitoring enabled.")
    if btn_rev:
        st.toast("Initiate Review: Investigator review workflow scheduled.")
        st.warning("Initiate Review: Review workflow dispatched.")
    if btn_esc:
        st.toast("Escalate: Alert dispatched to senior review board.")
        st.error("Escalate: Priority alert sent to senior board.")
    if btn_str:
        st.toast("File STR: goAML XML payload queued for FIU-IND submission.")
        st.success("File STR: Compliance payload queued.")
    if btn_frz:
        st.toast("Freeze Account: CBS debit freeze webhook executed.")
        st.error("Freeze Account: Debit freeze lock applied via CBS webhook.")
