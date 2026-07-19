# MuleShield AI — Connected Demo Dataset Specification

This document details the single connected financial crime universe utilized by the MuleShield AI demonstration. Every account, transaction, and narrative belongs to the same underlying money-laundering network.

---

## 1. Connected Laundering Network

The demo maps out a coordinated money-laundering syndicate operating through **Bank of India** and linked merchant hubs. The entities are:

### The Victims
- **Mrs. Ananya Sharma**: Retired school teacher who fell victim to a fake investment scam.
- **Rohan Mehta**: Student mule recruited via campus social circles.

### The Recruiter Nodes
- **Priya Nair (`ACC-00310`)**: Recruits students and dormant account holder details, routing funds to shell companies.
- **Arjun Menon (`ACC-00311`)**: Coordinated mule recruiter working in tandem with Priya.

### The Layering Shell Merchants
- **Vikram Shah (`ACC-00199` - V-9 Trading)**: Shell merchant receiving transactions, routing them in 3-hop layering loops.
- **Neha Iyer (`ACC-00208` - Northstar Retail)**: Shell merchant receiving large fake payroll transactions.
- **Sanjay Kapoor (`ACC-00217` - Kaveri Goods)**: Shell merchant receiving fake loan disbursements.

### The Cash-out Destinations
- **OrbitX Exchange (`ACC-00619`)**: Cryptocurrency exchange where layered funds are converted to crypto wallets.
- **FestivalPay (`ACC-00881`)**: Cashback settlement engine used to disguise card refunds.

---

## 2. Connected Investigations (The Trail of ₹2,80,000)

```
[Mrs. Sharma (Victim)] ➔ Inbound UPI ➔ [Ananya Rao (ACC-00028 - Dormant)]
                                                │
                                                ▼ (UPI: ₹75,000)
                                        [Priya Nair (ACC-00310 - Recruiter)]
                                                │
                                                ▼ (IMPS: ₹69,000)
                                        [V-9 Trading (ACC-00199 - Shell Merchant)]
                                                │
                                                ▼ (NEFT: ₹62,000)
                                        [OrbitX Exchange (ACC-00619 - Crypto Sink)]
```

Every sample case in the priority queue represents a different facet of this same ecosystem:
- **Case 0028 (Critical)**: Dormant salary account reactivated by Priya Nair.
- **Case 0142 (High)**: Student Rohan Mehta receiving recruitment payouts.
- **Case 0199 (High)**: Shell merchant V-9 Trading conducting 3-hop loop layering.
- **Case 0619 (High)**: OrbitX Exchange cash-out pipeline during overnight hours.
