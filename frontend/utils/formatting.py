# frontend/utils/formatting.py

def _fmt_amount(total: float) -> str:
    """Format INR amount as Lakhs or Crores."""
    if total >= 1e7:
        return f"₹{total / 1e7:.2f} Cr"
    return f"₹{total / 1e5:.2f} L"
