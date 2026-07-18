import { useMemo, useState, useEffect } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { NavLink, useLocation, useNavigate } from "react-router-dom";
import {
  Activity, ArrowLeft, ArrowRight, BarChart3, Check, ChevronDown, CircleHelp,
  ClipboardCheck, FileCheck2, FileText, GitBranch, Home, Info, Network,
  Search, ShieldCheck, Sparkles, Upload, Waypoints, X, Play, RefreshCw, Terminal
} from "lucide-react";

type Severity = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
type CaseItem = {
  account: string; risk_score: number; severity: Severity; mule_stage: string;
  profile_risk: number; transaction_risk: number; graph_risk: number;
  explanation: string; shap_signals: Record<string, number>; evidence_hash: string;
  case_id: string; goaml_xml: string; evidence: Evidence[]; reasons: string[];
};
type Evidence = { from_account: string; to_account: string; amount: number; timestamp: string; from_name?: string; to_name?: string; channel?: string };

const signalNames: Record<string, string> = {
  F670: "Prior regulatory watch-list signal",
  F886: "Unusual payment-channel switching",
  F3908: "High-velocity pass-through behavior",
  F115: "Elevated transaction frequency",
  F2082: "Normal retail activity is absent",
  F3889: "Dormant profile reactivated",
  F3891: "High-vulnerability profile signal",
};

const fallbackCases: CaseItem[] = [
  { account:"ACC05200000000028", risk_score:86, severity:"CRITICAL", mule_stage:"BEING_FLUSHED", profile_risk:78, transaction_risk:92, graph_risk:65, case_id:"STR-20260719-0028", evidence_hash:"9e31f17b5d8ac4ab41c3a0e9d3f8c21a7a7d59efc26e4ddf0d11f4f2a6b7c2a1", reasons:["Dormant reactivation","Velocity spike","Linked accounts"], explanation:"A dormant account reactivated and moved funds at high velocity through linked accounts. The pattern is consistent with an account being used as a pass-through node.", shap_signals:{F3889:0.82,F3908:0.74,F886:0.51,F670:0.28}, evidence:[{from_account:"ACC05200000000028",to_account:"ACC05299999999999",amount:75000,timestamp:"2026-07-19 10:42:00",from_name:"Subject account",to_name:"Consolidation node",channel:"UPI"}], goaml_xml:"<goAMLReport><caseId>STR-20260719-0028</caseId><account>ACC05200000000028</account><risk>86</risk><severity>CRITICAL</severity></goAMLReport>" },
  { account:"ACC05200000000142", risk_score:74, severity:"HIGH", mule_stage:"ACTIVE_MULE", profile_risk:71, transaction_risk:79, graph_risk:54, case_id:"STR-20260719-0142", evidence_hash:"5a7c8e9b1d4f6a2b8c0e7f3d9a1b5c6d", reasons:["Circular routing","High velocity"], explanation:"The account shows repeated high-velocity transfers and a circular routing pattern across related beneficiaries.", shap_signals:{F3908:0.7,F115:0.49,F886:0.35}, evidence:[{from_account:"ACC05200000000142",to_account:"ACC05299999999980",amount:42000,timestamp:"2026-07-19 09:18:00",channel:"IMPS"}], goaml_xml:"<goAMLReport><caseId>STR-20260719-0142</caseId><account>ACC05200000000142</account><risk>74</risk><severity>HIGH</severity></goAMLReport>" },
  { account:"ACC05200000000199", risk_score:52, severity:"MEDIUM", mule_stage:"NEWLY_RECRUITED", profile_risk:54, transaction_risk:58, graph_risk:32, case_id:"STR-20260719-0199", evidence_hash:"7d2a9f4b6c1e8a3d", reasons:["New account activity","Unusual amount ratio"], explanation:"The account is newly active with transaction behavior that needs enrichment before escalation.", shap_signals:{F115:0.41,F2082:0.25}, evidence:[{from_account:"ACC05200000000199",to_account:"ACC05200000000011",amount:18500,timestamp:"2026-07-19 08:03:00",channel:"NEFT"}], goaml_xml:"<goAMLReport><caseId>STR-20260719-0199</caseId><account>ACC05200000000199</account><risk>52</risk><severity>MEDIUM</severity></goAMLReport>" },
  { account:"ACC05200000000013", risk_score:16, severity:"LOW", mule_stage:"LEGITIMATE", profile_risk:12, transaction_risk:24, graph_risk:8, case_id:"CASE-20260719-0013", evidence_hash:"8b7053c65586b6f8", reasons:["Isolated anomaly"], explanation:"An isolated anomaly was detected, but current evidence does not support escalation.", shap_signals:{F3908:-0.19}, evidence:[], goaml_xml:"" },
];

const navItems = [
  { label:"Cases", path:"/cases", icon:Home }, { label:"Investigate", path:"/investigate", icon:Sparkles },
  { label:"Evidence", path:"/evidence", icon:FileCheck2 }, { label:"Methodology", path:"/methodology", icon:BarChart3 },
];

function severityClass(severity: Severity) { return severity.toLowerCase(); }
function labelStage(stage: string) { return stage.replace(/_/g, " ").replace(/\b\w/g, (m: string) => m.toUpperCase()); }
function briefFor(item: CaseItem) { return Object.entries(item.shap_signals).sort((a,b) => Math.abs(b[1])-Math.abs(a[1])).slice(0,3).map(([key]) => signalNames[key] || `Elevated factor ${key}`); }

function App() {
  const location = useLocation(); const navigate = useNavigate();
  const [cases, setCases] = useState<CaseItem[]>(fallbackCases);
  const [selectedId, setSelectedId] = useState(fallbackCases[0].account);
  const [query, setQuery] = useState(""); const [toast, setToast] = useState(""); const [packageReady, setPackageReady] = useState(false);
  const [isCmdOpen, setIsCmdOpen] = useState(false);
  const [offlineMode, setOfflineMode] = useState(true);
  const [unfoldProgress, setUnfoldProgress] = useState<Record<string, number>>({});

  const selected = cases.find((item) => item.account === selectedId) || cases[0];
  const filtered = useMemo(() => cases.filter((item) => `${item.account} ${item.severity} ${item.mule_stage} ${item.reasons.join(" ")}`.toLowerCase().includes(query.toLowerCase())), [cases, query]);
  const notify = (message: string) => { setToast(message); window.setTimeout(() => setToast(""), 2600); };

  const chooseCase = (item: CaseItem) => { setSelectedId(item.account); setPackageReady(false); navigate("/investigate"); };
  const runGuided = () => {
    setCases(fallbackCases);
    setSelectedId(fallbackCases[0].account);
    setPackageReady(false);
    // Reset unfolding sequence for this case
    setUnfoldProgress(prev => ({ ...prev, [fallbackCases[0].account]: 0 }));
    notify("Guided investigation loaded from mock provider.");
    navigate("/investigate");
  };

  const resetDemo = () => {
    setCases(fallbackCases);
    setSelectedId(fallbackCases[0].account);
    setPackageReady(false);
    setUnfoldProgress({});
    notify("Demo states successfully reset.");
    setIsCmdOpen(false);
  };

  const upload = async (file: File) => {
    const form = new FormData(); form.append("file", file);
    try {
      const response = await fetch(`${(import.meta as any).env.VITE_API_URL || "http://127.0.0.1:8000"}/analyze`, { method:"POST", body:form });
      if (!response.ok) throw new Error("API unavailable");
      const data = await response.json();
      const incoming = (data.alerts || []).map(normalizeCase) as CaseItem[];
      if (incoming.length) { setCases(incoming); setSelectedId(incoming[0].account); notify("Transaction batch analyzed."); navigate("/investigate"); }
    } catch { notify("Backend unavailable — showing offline guided case instead."); runGuided(); }
  };

  const page = location.pathname;

  // Listen for Ctrl+K / Cmd+K
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setIsCmdOpen(prev => !prev);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  return <div className="app">
    <Sidebar offlineMode={offlineMode} onReset={resetDemo} />
    <main className="main">
      <header className="topbar">
        <div className="topbar-title">AML Investigation Workspace <span className="muted">/ {page.slice(1) || "cases"}</span></div>
        <div className="topbar-actions">
          <button className="reset-badge" onClick={() => setIsCmdOpen(true)} title="Press Ctrl+K">
            <Terminal size={12} style={{marginRight:5}}/> Cmd Menu
          </button>
          <label className="search"><Search size={14}/><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search cases..."/></label>
          <div className="avatar" title="Analyst workspace">AR</div>
        </div>
      </header>
      <div className="content">
        {page === "/investigate" ? (
          <Investigation
            item={selected}
            cases={filtered}
            onSelect={chooseCase}
            onBack={() => navigate("/cases")}
            packageReady={packageReady}
            setPackageReady={setPackageReady}
            unfoldProgress={unfoldProgress[selected.account] ?? 0}
            setUnfoldProgress={(v) => setUnfoldProgress(prev => ({ ...prev, [selected.account]: v }))}
            notify={notify}
          />
        ) : page === "/evidence" ? (
          <Evidence item={selected} cases={cases} packageReady={packageReady} onPrepare={setPackageReady} notify={notify} />
        ) : page === "/methodology" ? (
          <Methodology />
        ) : (
          <Cases cases={filtered} onSelect={chooseCase} onGuided={runGuided} onUpload={upload} />
        )}
      </div>
    </main>

    {/* Command Bar Modal */}
    <AnimatePresence>
      {isCmdOpen && (
        <div className="modal-overlay" onClick={() => setIsCmdOpen(false)}>
          <motion.div
            className="modal-content"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.15, ease: "easeOut" }}
            onClick={(e) => e.stopPropagation()}
          >
            <div className="modal-header">
              <h3>MuleShield Command Bar</h3>
              <button className="close-btn" onClick={() => setIsCmdOpen(false)}><X size={16}/></button>
            </div>
            <div className="modal-body">
              <div className="command-section">
                <div className="section-label">Demo Commands</div>
                <button className="cmd-item" onClick={runGuided}>
                  <Sparkles size={14}/> <span>Run Guided Investigation Scenario</span> <kbd>G</kbd>
                </button>
                <button className="cmd-item" onClick={resetDemo}>
                  <RefreshCw size={14}/> <span>Reset Presentation State</span> <kbd>R</kbd>
                </button>
                <button className="cmd-item" onClick={() => { setOfflineMode(!offlineMode); setIsCmdOpen(false); notify(`Connection State Toggled to ${!offlineMode ? "Online" : "Simulated Offline"}`); }}>
                  <Activity size={14}/> <span>Toggle Connection Mock Mode ({offlineMode ? "Simulated Offline" : "Live Web"})</span> <kbd>O</kbd>
                </button>
              </div>
              <div className="command-section">
                <div className="section-label">Navigation Shortcuts</div>
                <button className="cmd-item" onClick={() => { navigate("/cases"); setIsCmdOpen(false); }}>
                  <Home size={14}/> <span>Navigate to Cases Queue</span> <kbd>1</kbd>
                </button>
                <button className="cmd-item" onClick={() => { navigate("/investigate"); setIsCmdOpen(false); }}>
                  <Sparkles size={14}/> <span>Navigate to Investigation Workspace</span> <kbd>2</kbd>
                </button>
                <button className="cmd-item" onClick={() => { navigate("/evidence"); setIsCmdOpen(false); }}>
                  <FileCheck2 size={14}/> <span>Navigate to Sealed Evidence Packages</span> <kbd>3</kbd>
                </button>
                <button className="cmd-item" onClick={() => { navigate("/methodology"); setIsCmdOpen(false); }}>
                  <BarChart3 size={14}/> <span>Navigate to Technical Methodology</span> <kbd>4</kbd>
                </button>
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>

    <AnimatePresence>{toast && <motion.div className="toast" initial={{opacity:0,y:12}} animate={{opacity:1,y:0}} exit={{opacity:0,y:12}}>{toast}</motion.div>}</AnimatePresence>
  </div>;
}

function Sidebar({ offlineMode, onReset }: { offlineMode: boolean, onReset: () => void }) {
  return <aside className="sidebar">
    <div className="brand">
      <div className="brand-mark">M</div>
      <div>
        <div className="brand-name">MuleShield AI</div>
        <div className="brand-sub">Trust infrastructure</div>
      </div>
    </div>
    <nav className="nav">
      <div className="nav-label">Workspace</div>
      {navItems.map(({label,path,icon:Icon}) => <NavLink key={path} to={path} className={({isActive}) => `nav-link ${isActive ? "active" : ""}`}><Icon size={16}/><span>{label}</span></NavLink>)}
    </nav>
    <div className="sidebar-bottom">
      <div className="sidebar-note">
        <ShieldCheck size={15} color="#89e4bd"/>
        <div style={{marginTop: 5}}><b>{offlineMode ? "Demo Mode Active" : "Operational Mode"}</b></div>
        <div className="small muted" style={{marginTop: 3}}>{offlineMode ? "Resilient fallback fixture loaded without external APIs." : "Connected to MuleShield active server API."}</div>
      </div>
      <button className="reset-button" onClick={onReset}>
        <RefreshCw size={12}/> Reset Presentation
      </button>
    </div>
  </aside>;
}

function Cases({ cases, onSelect, onGuided, onUpload }: { cases: CaseItem[]; onSelect:(item:CaseItem)=>void; onGuided:()=>void; onUpload:(file:File)=>void }) {
  const critical=cases.filter(c=>c.severity==="CRITICAL").length;
  const high=cases.filter(c=>c.severity==="HIGH").length;
  const review=cases.filter(c=>c.severity!=="LOW").length;
  return <>
    <div className="page-heading">
      <div>
        <div className="eyebrow">Cases / Priority queue</div>
        <h1>Good morning, Analyst.</h1>
        <p className="muted" style={{marginTop:8}}>Four signals need a defensible next move.</p>
      </div>
      <div style={{display:"flex",gap:9}}>
        <label className="button"><Upload size={15}/> Upload batch<input hidden type="file" accept=".csv" onChange={(e)=>e.target.files?.[0] && onUpload(e.target.files[0])}/></label>
        <button className="button primary" onClick={onGuided}><Sparkles size={15}/> Run guided investigation</button>
      </div>
    </div>
    <div className="grid summary-grid">
      <Stat label="Critical cases" value={critical.toString()} detail="Immediate review" color="critical"/>
      <Stat label="High priority" value={high.toString()} detail="Priority queue" color="high"/>
      <Stat label="Awaiting decision" value={review.toString()} detail="Across current batch" color="medium"/>
      <Stat label="Evidence sealed" value="12" detail="Review-ready packages" color="low"/>
    </div>
    <div className="grid two-col">
      <section className="card">
        <div className="section-head">
          <div>
            <h2>Priority queue</h2>
            <div className="muted" style={{marginTop:4}}>Ranked by composite risk and lifecycle urgency</div>
          </div>
          <span className="eyebrow">{cases.length} cases</span>
        </div>
        <div className="case-list">
          {cases.map((item,index)=><CaseRow key={item.account} item={item} selected={index===0} onClick={()=>onSelect(item)}/>)}
        </div>
      </section>
      <section className="card focal">
        <div className="eyebrow">Guided investigation</div>
        <h2 style={{marginTop:10}}>Make the next decision visible.</h2>
        <p className="muted" style={{lineHeight:1.6,marginTop:10}}>Open a prepared scenario to see how MuleShield turns profile, transaction, and network signals into an explainable handoff.</p>
        <div className="callout">
          <div className="status critical"><span className="status-dot"/> Critical case ready</div>
          <p className="small muted" style={{marginTop:9}}>Dormant reactivation · velocity · linked accounts</p>
        </div>
        <motion.button
          whileTap={{ scale: 0.98 }}
          className="button primary"
          style={{marginTop:22}}
          onClick={onGuided}
        >
          Open case workspace <ArrowRight size={15}/>
        </motion.button>
      </section>
    </div>
  </>;
}

function Stat({label,value,detail,color}:{label:string;value:string;detail:string;color:string}) {
  return <div className="card stat">
    <div className={`status ${color}`}><span className="status-dot"/>{label}</div>
    <div className="stat-value">{value}</div>
    <div className="stat-label">{detail}</div>
  </div>;
}

function CaseRow({item,selected,onClick}:{item:CaseItem;selected:boolean;onClick:()=>void}) {
  return <button className={`case-row ${selected?"selected":""}`} onClick={onClick}>
    <div>
      <div className={`status ${severityClass(item.severity)}`}><span className="status-dot"/>{item.severity}</div>
      <div className="small muted" style={{marginTop:5}}>{labelStage(item.mule_stage)}</div>
    </div>
    <div>
      <div className="case-account mono">{item.account}</div>
      <div className="case-signal" style={{marginTop: 4}}>{item.reasons.join(" · ")}</div>
    </div>
    <div className="case-score">{Math.round(item.risk_score)}<span className="muted small"> /100</span></div>
  </button>;
}

function Investigation({
  item, cases, onSelect, onBack, packageReady, setPackageReady, unfoldProgress, setUnfoldProgress, notify
}:{
  item:CaseItem; cases:CaseItem[]; onSelect:(item:CaseItem)=>void; onBack:()=>void;
  packageReady:boolean; setPackageReady:(v:boolean)=>void; unfoldProgress: number; setUnfoldProgress:(v:number)=>void;
  notify:(m:string)=>void;
}) {
  const brief = briefFor(item);
  const stages = ["DORMANT", "ACTIVATION", "NEWLY_RECRUITED", "ACTIVE_MULE", "BEING_FLUSHED"];
  const current = Math.max(0, stages.indexOf(item.mule_stage));

  // Auto-play unfolding effect with intervals
  useEffect(() => {
    if (unfoldProgress >= 3) return;
    const interval = setTimeout(() => {
      setUnfoldProgress(unfoldProgress + 1);
    }, 1200);
    return () => clearTimeout(interval);
  }, [unfoldProgress]);

  // Smooth Count-Up effect aligned with the weights
  const targetScore = useMemo(() => {
    if (unfoldProgress === 0) return Math.round(item.profile_risk * 0.40);
    if (unfoldProgress === 1) return Math.round(item.profile_risk * 0.40 + item.transaction_risk * 0.40);
    return Math.round(item.risk_score);
  }, [unfoldProgress, item]);

  const [counterVal, setCounterVal] = useState(0);
  useEffect(() => {
    let start = counterVal;
    if (start === targetScore) return;
    const duration = 500;
    const startTime = performance.now();
    let frame: number;
    const tick = (now: number) => {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const ease = progress * (2 - progress); // easeOut
      setCounterVal(Math.round(start + (targetScore - start) * ease));
      if (progress < 1) {
        frame = requestAnimationFrame(tick);
      }
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [targetScore]);

  // Handle prepare evidence sequence
  const [prepareState, setPrepareState] = useState<'idle' | 'preparing' | 'sealing' | 'verified' | 'ready'>(packageReady ? 'ready' : 'idle');
  const handlePrepare = () => {
    if (prepareState === 'ready') return;
    setPrepareState('preparing');
    setTimeout(() => {
      setPrepareState('sealing');
      setTimeout(() => {
        setPrepareState('verified');
        setTimeout(() => {
          setPrepareState('ready');
          setPackageReady(true);
          notify("Evidence hash sealed and locked in Case Ledger.");
        }, 400);
      }, 400);
    }, 400);
  };

  return <>
    <div className="case-header">
      <div className="case-header-left">
        <button className="button" onClick={onBack}><ArrowLeft size={15}/> Cases</button>
        <span className="mono small muted">{item.account}</span>
        <span className={`status ${severityClass(item.severity)}`}><span className="status-dot"/>{item.severity}</span>
      </div>
      <button className="button primary" onClick={handlePrepare} disabled={prepareState !== 'idle' && prepareState !== 'ready'}>
        <FileCheck2 size={15}/>
        {prepareState === 'idle' ? "Prepare Evidence" :
         prepareState === 'preparing' ? "Reading Metadata..." :
         prepareState === 'sealing' ? "Computing Cryptographic Seal..." :
         prepareState === 'verified' ? "Verifying SHA-256 integrity..." : "Evidence Package Ready"}
      </button>
    </div>
    <div className="grid three-col">
      <section className="card">
        <div className="section-head">
          <h3>Case queue</h3>
          <span className="eyebrow">{cases.length}</span>
        </div>
        <div className="case-list">
          {cases.map((candidate) => (
            <button key={candidate.account} className={`case-row ${candidate.account===item.account?"selected":""}`} style={{gridTemplateColumns:"1fr"}} onClick={()=>onSelect(candidate)}>
              <div style={{display:"flex",justifyContent:"space-between",gap:8}}>
                <span className={`status ${severityClass(candidate.severity)}`}><span className="status-dot"/>{candidate.severity}</span>
                <b className="mono small">{Math.round(candidate.risk_score)}</b>
              </div>
              <div className="case-account mono" style={{marginTop:7}}>{candidate.account}</div>
              <div className="case-signal" style={{marginTop: 4}}>{candidate.reasons.join(" · ")}</div>
            </button>
          ))}
        </div>
      </section>

      {/* Decision surface (staged layout) */}
      <section className="card focal">
        <div className="section-head">
          <div className="eyebrow">Decision surface</div>
          {unfoldProgress < 3 && (
            <button className="skip-btn" onClick={() => setUnfoldProgress(3)}>Skip Unfolding</button>
          )}
        </div>
        <div className="score-wrap">
          <div className="score">{counterVal}<span> / 100</span></div>
          <div>
            <div className={`status ${severityClass(item.severity)}`}><span className="status-dot"/>{item.severity} risk</div>
            <div className="score-copy" style={{marginTop:8}}>
              {unfoldProgress === 0 ? "Assembling composite risk profile... [ML model active]" :
               unfoldProgress === 1 ? "Correlating profile with transaction telemetry... [Dual engines active]" :
               "Risk fusion complete. Network evidence correlated."}
            </div>
          </div>
        </div>

        {/* Contributor Bars reveal based on progress */}
        <div className="bars">
          {unfoldProgress >= 0 && (
            <motion.div initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }}>
              <div className="bar-head"><span>Profile behavior <span className="muted">· 40% weight</span></span><span className="mono">{item.profile_risk.toFixed(0)}</span></div>
              <div className="bar-track"><div className="bar-fill" style={{ width: `${item.profile_risk}%` }} /></div>
            </motion.div>
          )}
          {unfoldProgress >= 1 && (
            <motion.div initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} style={{marginTop: 12}}>
              <div className="bar-head"><span>Transaction behavior <span className="muted">· 40% weight</span></span><span className="mono">{item.transaction_risk.toFixed(0)}</span></div>
              <div className="bar-track"><div className="bar-fill" style={{ width: `${item.transaction_risk}%` }} /></div>
            </motion.div>
          )}
          {unfoldProgress >= 2 && (
            <motion.div initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} style={{marginTop: 12}}>
              <div className="bar-head"><span>Network context <span className="muted">· 20% weight</span></span><span className="mono">{item.graph_risk.toFixed(0)}</span></div>
              <div className="bar-track"><div className="bar-fill" style={{ width: `${item.graph_risk}%` }} /></div>
            </motion.div>
          )}
        </div>

        {/* Recommendation Card reveals at Stage 3 */}
        <AnimatePresence>
          {unfoldProgress >= 3 && (
            <motion.div
              className="recommendation"
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2 }}
            >
              <div className="eyebrow">Recommended next step</div>
              <strong>{item.severity === "LOW" ? "No escalation recommended from current evidence." : item.severity === "MEDIUM" ? "Monitor and enrich profile before escalation." : "Immediate review and escalation under bank policy."}</strong>
              <p className="small muted" style={{marginTop: 6}}>Final action must be confirmed by investigator. No auto-actions taken.</p>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Timeline reveals at Stage 3 */}
        {unfoldProgress >= 3 && (
          <motion.div style={{marginTop:26}} initial={{opacity:0}} animate={{opacity:1}}>
            <div className="section-head"><h3>Investigation timeline</h3><span className="small muted">Lifecycle context</span></div>
            <div className="timeline">
              {stages.map((stage,index)=><div key={stage} className={`timeline-item ${index<current?"done":""} ${index===current?"current":""}`}><div className="timeline-dot"/><div className="timeline-label">{labelStage(stage)}</div></div>)}
            </div>
          </motion.div>
        )}
      </section>

      {/* Case brief / details */}
      <section className="card">
        <div className="eyebrow">Case brief</div>
        <h2 style={{marginTop:9}}>Why this case was flagged</h2>
        <p className="muted small" style={{lineHeight:1.55,marginTop:10}}>{item.explanation}</p>
        <div className="brief-list">
          {brief.map((text, idx)=>(
            unfoldProgress >= idx && (
              <motion.div className="brief-item" key={text} initial={{opacity:0, x:-4}} animate={{opacity:1, x:0}}>
                <Check size={15} color="#89e4bd"/>
                <span>{text}</span>
              </motion.div>
            )
          ))}
        </div>

        {/* Network diagram panel */}
        {unfoldProgress >= 2 && (
          <motion.div initial={{opacity:0}} animate={{opacity:1}} style={{marginTop: 20}}>
            <div className="eyebrow">Network evidence</div>
            <div className="network">
              <div className="node small n1">ACC...999</div>
              <div className="node small n2">ACC...980</div>
              <div className="node">{item.account.slice(-4)}</div>
            </div>
            <p className="small muted" style={{lineHeight:1.5,marginTop:10}}>
              <Network size={13} style={{verticalAlign:"-2px",marginRight:5}}/>
              Simulated offline network enrichment. Fallback targets configured successfully.
            </p>
          </motion.div>
        )}

        <details className="drawer" style={{marginTop: 20}}>
          <summary>View technical factors</summary>
          {Object.entries(item.shap_signals).map(([key,value])=>(
            <div className="factor" key={key}>
              <span>{signalNames[key] || key}</span>
              <span className="mono">{Number(value).toFixed(2)}</span>
            </div>
          ))}
        </details>
      </section>
    </div>

    {/* Decision Ledger at the bottom */}
    {unfoldProgress >= 3 && (
      <motion.div className="card" style={{marginTop:14}} initial={{opacity: 0, y: 10}} animate={{opacity:1, y:0}}>
        <div className="section-head">
          <div>
            <div className="eyebrow">Evidence timeline</div>
            <h2 style={{marginTop:8}}>From signal to accountable handoff</h2>
          </div>
          <span className="small muted">{item.evidence.length} transaction record{item.evidence.length===1?"":"s"}</span>
        </div>
        <div className="grid" style={{gridTemplateColumns:"repeat(3,1fr)"}}>
          {["Signal detected","Evidence reviewed","Recommendation recorded"].map((label,index)=>(
            <div className="callout" key={label} style={{marginTop:0}}>
              <div className="status low"><span className="status-dot"/>{index < 2 || prepareState === 'ready' ? "Complete" : "Ready"}</div>
              <div style={{fontWeight:600,fontSize:13,marginTop:9}}>{label}</div>
              <div className="small muted" style={{marginTop:5}}>
                {index===0 ? item.reasons[0] || "Risk signal" :
                 index===1 ? "Profile and transaction context correlated" :
                 prepareState === 'ready' ? "Decision finalized & sealed" : "Awaiting investigator review"}
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    )}
  </>;
}

function Evidence({item,cases,packageReady,onPrepare,notify}:{item:CaseItem;cases:CaseItem[];packageReady:boolean;onPrepare:(v:boolean)=>void;notify:(m:string)=>void}) {
  const [stampStage, setStampStage] = useState(0);
  useEffect(() => {
    const timer = setTimeout(() => {
      setStampStage(1);
      setTimeout(() => {
        setStampStage(2);
      }, 250);
    }, 250);
    return () => clearTimeout(timer);
  }, []);

  return <>
    <div className="page-heading">
      <div>
        <div className="eyebrow">Evidence / Handoff</div>
        <h1>Evidence packages.</h1>
        <p className="muted" style={{marginTop:8}}>Make every recommendation reviewable and exportable.</p>
      </div>
      <button className="button primary" onClick={() => { onPrepare(true); notify("Evidence package successfully sealed."); }}>
        <FileCheck2 size={15}/>{packageReady ? "Package Sealed" : "Seal selected package"}
      </button>
    </div>
    <div className="grid two-col">
      <section className="card">
        <div className="section-head">
          <h2>Packages</h2>
          <span className="eyebrow">{cases.length} records</span>
        </div>
        <div className="case-list">
          {cases.filter(c=>c.severity!=="LOW").map((candidate,index)=>(
            <div key={candidate.case_id} className="case-row" style={{gridTemplateColumns:"1fr 72px"}}>
              <div>
                <div className={`status ${severityClass(candidate.severity)}`}><span className="status-dot"/>{candidate.severity}</div>
                <div className="case-account mono" style={{marginTop:7}}>{candidate.case_id}</div>
                <div className="case-signal">{candidate.account} · {index===0||packageReady?"Sealed":"Draft"}</div>
              </div>
              <div className="case-score">{Math.round(candidate.risk_score)}</div>
            </div>
          ))}
        </div>
        <div className="callout" style={{marginTop: 20}}>
          <div className="eyebrow">Decision Ledger</div>
          <p className="small muted" style={{marginTop:8,lineHeight:1.6}}>The ledger records the signal, recommendation, analyst review state, and integrity hash as one case event.</p>
          <div className="ledger-preview">
            {stampStage >= 0 && (
              <div className="ledger-row-stamp">
                <span className="stamp-chip active">DETECTED</span>
                <span className="small muted font-mono">19 Jul 2026 02:22 UTC</span>
              </div>
            )}
            {stampStage >= 1 && (
              <div className="ledger-row-stamp" style={{marginTop: 6}}>
                <span className="stamp-chip active">RECOMMENDED</span>
                <span className="small muted font-mono">19 Jul 2026 02:23 UTC</span>
              </div>
            )}
            {stampStage >= 2 && (
              <div className="ledger-row-stamp" style={{marginTop: 6}}>
                <span className="stamp-chip active">{packageReady ? "SEALED" : "DRAFT"}</span>
                <span className="small muted font-mono">{packageReady ? "19 Jul 2026 02:24 UTC" : "PENDING REVIEW"}</span>
              </div>
            )}
          </div>
        </div>
      </section>
      <section className="card">
        <div className="eyebrow">Report-ready package</div>
        <h2 style={{marginTop:9}}>Case {item.account}</h2>
        <div className="report-preview" style={{marginTop:18}}>
          <div className="eyebrow">MuleShield AI · Investigation report</div>
          <h2>Suspicious activity case brief</h2>
          <div className="report-row"><span>Case reference</span><span className="mono">{item.case_id}</span></div>
          <div className="report-row"><span>Composite assessment</span><span>{Math.round(item.risk_score)} / 100 · {item.severity}</span></div>
          <div className="report-row"><span>Lifecycle stage</span><span>{labelStage(item.mule_stage)}</span></div>
          <div className="report-rule"/>
          <p style={{fontSize:13,lineHeight:1.6}}>{item.explanation}</p>
          <div className="report-rule"/>
          <p style={{fontSize:11,color:"#71727b",lineHeight:1.5}}>This package is prepared for investigator review and export. It does not execute automatic account freezing or regulatory submission.</p>
        </div>
        <div className="hash" style={{marginTop:16}}>
          <ShieldCheck size={18} color="#89e4bd"/>
          <div>
            <div className="eyebrow" style={{color:"#89e4bd"}}>Evidence integrity · {packageReady?"sealed":"available"}</div>
            <code>{item.evidence_hash}</code>
          </div>
        </div>
        <div style={{display:"flex",gap:9,marginTop:16,flexWrap:"wrap"}}>
          <button className="button" onClick={()=>downloadText(item.goaml_xml || `<case>${item.case_id}</case>`,`${item.case_id}.xml`)}><FileText size={15}/> Export XML</button>
          <button className="button ghost" onClick={()=>downloadText(JSON.stringify(item,null,2),`${item.case_id}.json`)}><ClipboardCheck size={15}/> Export case JSON</button>
        </div>
      </section>
    </div>
  </>;
}

function Methodology() {
  return <>
    <div className="page-heading">
      <div>
        <div className="eyebrow">Methodology / Provenance</div>
        <h1>How the decision is formed.</h1>
        <p className="muted" style={{marginTop:8}}>Technical context stays available without taking over the investigation.</p>
      </div>
      <span className="status low"><span className="status-dot"/> Backend unchanged</span>
    </div>
    <div className="grid method-grid">
      <Weight value="40%" label="Profile behavior" text="XGBoost profile inference and SHAP attribution." icon={Activity}/>
      <Weight value="40%" label="Transaction behavior" text="Velocity, layering, cycles, structuring, and anomaly signals." icon={Waypoints}/>
      <Weight value="20%" label="Network context" text="Graph relationship evidence when enrichment is available." icon={GitBranch}/>
    </div>
    <div className="card" style={{marginTop:14}}>
      <div className="eyebrow">Decision boundary</div>
      <h2 style={{marginTop:9}}>Evidence before automation.</h2>
      <div className="callout">
        <Info size={16} color="#a4a6ff"/>
        <p className="small muted" style={{marginTop:8}}>MuleShield presents a risk recommendation and prepares evidence for investigator review. It does not automatically freeze an account or claim that a report has been submitted.</p>
      </div>
      <div className="grid two-col" style={{marginTop:14}}>
        <div>
          <h3>Graceful degradation</h3>
          <p className="small muted" style={{lineHeight:1.6,marginTop:8}}>If network enrichment is unavailable, profile and transaction evidence remain visible and the limitation is explicit.</p>
        </div>
        <div>
          <h3>Traceable narrative</h3>
          <p className="small muted" style={{lineHeight:1.6,marginTop:8}}>Case briefs are generated from response fields and mapped feature labels, not an unconstrained chatbot.</p>
        </div>
      </div>
    </div>
  </>;
}

function Weight({value,label,text,icon:Icon}:{value:string;label:string;text:string;icon:typeof Activity}) {
  return <div className="card">
    <Icon size={18} color="#a4a6ff"/>
    <div className="weight">{value}</div>
    <h3>{label}</h3>
    <p className="small muted" style={{lineHeight:1.6,marginTop:8}}>{text}</p>
  </div>;
}

function normalizeCase(raw: any): CaseItem {
  const score=Number(raw.risk_score ?? raw.composite_score ?? 0);
  return {
    account:String(raw.account ?? raw.account_no ?? "UNKNOWN"),
    risk_score:score,
    severity:(raw.severity || tier(score)) as Severity,
    mule_stage:String(raw.mule_stage || "LEGITIMATE"),
    profile_risk:Number(raw.profile_risk ?? raw.ml_score ?? 0),
    transaction_risk:Number(raw.transaction_risk ?? 0),
    graph_risk:Number(raw.graph_risk ?? raw.graph_score ?? 0),
    explanation:String(raw.explanation || "Risk assessment available for investigator review."),
    shap_signals:raw.shap_signals || {},
    evidence_hash:String(raw.evidence_hash || "Not returned"),
    case_id:String(raw.case_id || `CASE-${Date.now()}`),
    goaml_xml:String(raw.goaml_xml || ""),
    evidence:raw.evidence || [],
    reasons:raw.reasons || []
  };
}

function tier(score:number): Severity { return score>=80?"CRITICAL":score>=60?"HIGH":score>=40?"MEDIUM":"LOW"; }
function downloadText(content:string,name:string) {
  const blob=new Blob([content],{type:"text/plain"});
  const url=URL.createObjectURL(blob);
  const a=document.createElement("a");
  a.href=url;
  a.download=name;
  a.click();
  URL.revokeObjectURL(url);
}

export default App;
