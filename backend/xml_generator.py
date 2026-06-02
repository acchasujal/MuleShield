"""
MuleShield AI — goAML XML Report Generator
Builds FIU-IND compliant Suspicious Transaction Reports (STRs) per regulatory guidelines.
"""

from datetime import datetime, timezone

def generate_goaml_xml(
    case_id: str,
    account_no: str,
    ml_score: float,
    graph_score: float,
    composite_score: float,
    severity: str,
    mule_stage: str,
    explanations: list,
    evidence: list
) -> str:
    """Generates a highly structured goAML compliant XML payload representation for FIU-IND using f-string templates.

    Returns:
        A formatted XML string.
    """
    submission_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    status_code = "FROZEN" if severity == "CRITICAL" else "MONITORED"
    last_4 = account_no[-4:] if len(account_no) >= 4 else "0000"
    
    suspicion_description = (
        f"MuleShield AI flagged account {account_no} with composite risk score of {composite_score} ({severity}). "
        f"Mule Lifecycle Staging: {mule_stage}. "
        f"Tabular ML (XGBoost) features: {', '.join(explanations)}. "
        f"Graph connectivity degree: {graph_score}."
    )

    # Indented transactions block
    txn_blocks = []
    for idx, txn in enumerate(evidence[:5]):
        txn_number = f"TXN-{last_4}-{idx:04d}"
        internal_ref = f"BOI-REF-{datetime.now(timezone.utc).strftime('%y%j')}-{idx}"
        txn_date = txn.get("timestamp", submission_date)
        amount = str(txn.get("amount", 0.0))
        channel = txn.get("channel", "UPI")
        from_acc = txn.get("from_account", account_no)
        to_acc = txn.get("to_account", "ACC05299999999999")
        
        txn_blocks.append(f"    <transaction>\n"
                          f"      <transaction_number>{txn_number}</transaction_number>\n"
                          f"      <internal_ref_number>{internal_ref}</internal_ref_number>\n"
                          f"      <transaction_date>{txn_date}</transaction_date>\n"
                          f"      <amount>{amount}</amount>\n"
                          f"      <currency_code>INR</currency_code>\n"
                          f"      <transmode_code>{channel}</transmode_code>\n"
                          f"      <transaction_direction>\n"
                          f"        <from_account>{from_acc}</from_account>\n"
                          f"        <to_account>{to_acc}</to_account>\n"
                          f"      </transaction_direction>\n"
                          f"    </transaction>")

    txns_xml = "\n".join(txn_blocks)

    xml_content = f"""<?xml version="1.0" ?>
<report>
  <report_header>
    <report_code>STR</report_code>
    <report_ref>{case_id}</report_ref>
    <reporting_entity>Bank of India, AML Compliance Division</reporting_entity>
    <submission_date>{submission_date}</submission_date>
  </report_header>
  <reasons_suspicion>
    <suspicion_description>{suspicion_description}</suspicion_description>
    <laws_violated>PMLA 2002 Section 12, RBI AML Master Circular Clauses</laws_violated>
  </reasons_suspicion>
  <subject_account>
    <account>
      <institution_name>Bank of India</institution_name>
      <branch_code>BOI-HQ-MUM</branch_code>
      <account_number>{account_no}</account_number>
      <currency_code>INR</currency_code>
      <status_code>{status_code}</status_code>
      <account_owner>
        <individual>
          <first_name>Customer</first_name>
          <last_name>#{last_4}</last_name>
          <occupation>Student / Vulnerable Demographic Profile</occupation>
        </individual>
      </account_owner>
    </account>
  </subject_account>
  <transactions>
{txns_xml}
  </transactions>
</report>
"""
    return xml_content
