import { useState, useRef, useCallback, useEffect } from 'react';

/* ══════════════════════════════════════════
   TYPES
   ══════════════════════════════════════════ */
interface Analysis {
  ats_score: number;
  matching_skills: string[];
  missing_skills: string[];
  strengths: string[];
  weaknesses: string[];
  suggestions: string[];
  summary: string;
}

type Phase = 'idle' | 'loading' | 'done' | 'error';

/* ══════════════════════════════════════════
   DEMO DATA
   ══════════════════════════════════════════ */
const DEMO: Analysis = {
  ats_score: 72,
  matching_skills: ['React', 'TypeScript', 'Node.js', 'REST APIs', 'Git', 'CSS', 'SQL', 'Agile'],
  missing_skills: ['Kubernetes', 'GraphQL', 'AWS Lambda', 'Redis', 'Terraform'],
  strengths: [
    'Strong frontend engineering background with 4+ years of hands-on React experience.',
    'Demonstrated ability to lead cross-functional teams and deliver projects on schedule.',
    'Excellent communication skills evidenced by technical writing and open-source contributions.',
    'Solid understanding of software architecture patterns and design principles.',
  ],
  weaknesses: [
    'Limited cloud infrastructure experience — the role requires AWS certification.',
    'No mention of performance optimization metrics or quantifiable impact.',
    'Backend service orchestration and microservices architecture experience not demonstrated.',
  ],
  suggestions: [
    'Add quantifiable achievements to each role (e.g., "reduced load time by 40%") to stand out in ATS filters.',
    'Obtain an AWS Certified Developer associate certification to close the most critical skill gap.',
    'Include a skills matrix or technical proficiency section to help ATS scanners better parse your expertise.',
    'Tailor your professional summary to mirror the exact language used in this job description.',
    'Add GraphQL and Apollo Client to your project examples — even personal projects count.',
    'Highlight any Kubernetes or Docker orchestration work, even in a team context.',
  ],
  summary:
    'This candidate demonstrates strong frontend engineering fundamentals and team collaboration experience. The resume aligns well with the core technical requirements but falls short on cloud infrastructure and DevOps skills which are critical for this senior-level role. With targeted upskilling in AWS and containerization, and quantified impact statements, the ATS score could reach 85+.',
};

/* ══════════════════════════════════════════
   HELPERS
   ══════════════════════════════════════════ */
function scoreColor(s: number) {
  if (s >= 80) return '#39ff9f';
  if (s >= 60) return '#00e5ff';
  if (s >= 40) return '#ffcc02';
  return '#ff6b8a';
}
function verdictClass(s: number) {
  if (s >= 80) return 'exc';
  if (s >= 60) return 'goo';
  if (s >= 40) return 'avg';
  return 'por';
}
function verdictText(s: number) {
  if (s >= 80) return '✦ EXCELLENT MATCH';
  if (s >= 60) return '◈ STRONG CANDIDATE';
  if (s >= 40) return '⚡ ROOM TO IMPROVE';
  return '⚠ NEEDS SIGNIFICANT WORK';
}
const EMOJIS = ['💡', '🚀', '🎯', '⚡', '🔧', '📊', '🌟', '🔮', '⚙️', '🛸'];

/* ══════════════════════════════════════════
   SPACE BACKGROUND
   ══════════════════════════════════════════ */
function SpaceBg() {
  return (
    <div className="space-canvas">
      <div className="neb neb-1" />
      <div className="neb neb-2" />
      <div className="neb neb-3" />
      <div className="neb neb-4" />
      <div className="stars-layer" />
      <div className="perspective-grid" />
      <div className="orb orb-1" />
      <div className="orb orb-2" />
      <div className="orb orb-3" />
      <div className="orb orb-4" />
      <div className="orb orb-5" />
    </div>
  );
}

/* ══════════════════════════════════════════
   METRIC CARD
   ══════════════════════════════════════════ */
function MetricCard({ val, lbl }: { val: string; lbl: string }) {
  return (
    <div className="metric">
      <div className="metric-val">{val}</div>
      <div className="metric-lbl">{lbl}</div>
      <div className="metric-pip" />
    </div>
  );
}

/* ══════════════════════════════════════════
   ATS SCORE GAUGE
   ══════════════════════════════════════════ */
function Gauge({ score }: { score: number }) {
  const R = 85;
  const C = 2 * Math.PI * R;
  const [n, setN] = useState(0);

  useEffect(() => {
    const t0 = Date.now();
    const dur = 1600;
    const tick = () => {
      const p = Math.min((Date.now() - t0) / dur, 1);
      const e = 1 - Math.pow(1 - p, 4);
      setN(Math.round(e * score));
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }, [score]);

  const fill = (n / 100) * C;
  const color = scoreColor(score);

  return (
    <div className="gauge-panel">
      <div className="gauge-wrap">
        {/* SVG defs for drop shadow filter */}
        <svg width="0" height="0" style={{ position: 'absolute' }}>
          <defs>
            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="3" result="blur" />
              <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
            </filter>
          </defs>
        </svg>

        <svg className="gauge-svg" viewBox="0 0 200 200">
          <circle className="g-track" cx="100" cy="100" r={R} />
          <circle
            className="g-fill"
            cx="100" cy="100" r={R}
            stroke={color}
            strokeDasharray={`${fill} ${C}`}
          />
        </svg>

        <div className="gear-ring" />

        <div className="gauge-center">
          <div className="gauge-num" style={{ color }}>{n}</div>
          <div className="gauge-pct">ATS SCORE</div>
        </div>
      </div>

      <div className="ats-tag" style={{ color }}>APPLICATION TRACKING</div>
      <div className="ats-verdict">{verdictText(score)}</div>
    </div>
  );
}

/* ══════════════════════════════════════════
   HOLOGRAPHIC DOCUMENT ICON
   ══════════════════════════════════════════ */
function HoloDoc() {
  return (
    <div className="holo-doc">
      <div className="holo-doc-body">
        <div className="doc-corner" />
        <div className="doc-line" />
        <div className="doc-line" />
        <div className="doc-line" />
      </div>
    </div>
  );
}

/* ══════════════════════════════════════════
   UPLOAD ZONE
   ══════════════════════════════════════════ */
function UploadZone({
  file, onChange,
}: {
  file: File | null;
  onChange: (f: File | null) => void;
}) {
  const ref = useRef<HTMLInputElement>(null);
  const [drag, setDrag] = useState(false);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDrag(false);
    const f = e.dataTransfer.files[0];
    if (f?.name.toLowerCase().endsWith('.pdf')) onChange(f);
  };

  return (
    <div className="upload-side">
      <div className="side-label">RESUME UPLOAD PLATFORM</div>
      <div
        className={`drop-zone${drag ? ' drag-over' : ''}`}
        id="upload-zone"
        role="button"
        tabIndex={0}
        aria-label="Upload PDF resume"
        onClick={() => ref.current?.click()}
        onKeyDown={e => e.key === 'Enter' && ref.current?.click()}
        onDragEnter={e => { e.preventDefault(); setDrag(true); }}
        onDragOver={e => e.preventDefault()}
        onDragLeave={e => { e.preventDefault(); setDrag(false); }}
        onDrop={handleDrop}
      >
        <input
          ref={ref}
          type="file"
          id="resume-input"
          accept=".pdf"
          style={{ display: 'none' }}
          onChange={e => onChange(e.target.files?.[0] ?? null)}
        />

        <HoloDoc />

        {file ? (
          <>
            <div className="file-chip">
              <span className="chip-icon">📂</span>
              {file.name}
            </div>
            <div className="drop-sub">Click to replace</div>
          </>
        ) : (
          <>
            <div className="drop-label">{drag ? '⚡ DROP IT!' : 'DROP PDF HERE'}</div>
            <div className="drop-sub">or click to browse • PDF only</div>
          </>
        )}
      </div>
    </div>
  );
}

/* ══════════════════════════════════════════
   LOADING STATE
   ══════════════════════════════════════════ */
const STEPS = [
  'PARSING RESUME DATA…',
  'EXTRACTING SKILL VECTORS…',
  'COMPUTING ATS ALIGNMENT…',
  'ANALYZING ROLE FIT…',
  'GENERATING INSIGHTS…',
];

function Loader() {
  const [step, setStep] = useState(0);
  useEffect(() => {
    const id = setInterval(() => setStep(s => (s + 1) % STEPS.length), 1100);
    return () => clearInterval(id);
  }, []);
  return (
    <div className="loading-box">
      <div className="loader">
        <div className="loader-ring lr1" />
        <div className="loader-ring lr2" />
        <div className="loader-ring lr3" />
      </div>
      <div className="loading-msg">{STEPS[step]}</div>
      <div className="loading-dots">
        <span /><span /><span />
      </div>
    </div>
  );
}

/* ══════════════════════════════════════════
   RESULTS PANEL
   ══════════════════════════════════════════ */
function Results({ data, isDemo }: { data: Analysis; isDemo: boolean }) {
  const vc = verdictClass(data.ats_score);

  return (
    <div className="results">
      {isDemo && (
        <div className="demo-banner">
          ⚡ DEMO MODE — Start your Flask backend on port 5000 to analyze real resumes
        </div>
      )}

      {/* Score + Summary */}
      <div className="sec-head">
        <div className="sec-title">◈ ANALYSIS DASHBOARD</div>
        <div className="sec-line" />
      </div>

      <div className="dash-row">
        <Gauge score={data.ats_score} />

        <div className="summary-panel">
          {/* Light streaks */}
          <div className="streak" style={{ width: 220, top: '35%', animationDuration: '6s', animationDelay: '0s' }} />
          <div className="streak" style={{ width: 160, top: '65%', animationDuration: '8s', animationDelay: '3s' }} />

          <div className={`verdict-chip ${vc}`}>{verdictText(data.ats_score)}</div>
          <div className="summary-label">// ASSESSMENT_SUMMARY</div>
          <div className="summary-text">{data.summary}</div>
        </div>
      </div>

      {/* Skills */}
      <div className="sec-head">
        <div className="sec-title">◈ SKILL MATRIX</div>
        <div className="sec-line" />
      </div>
      <div className="two-col">
        <div className="skill-panel">
          <div className="panel-title">MATCHING SKILLS</div>
          <div className="tags">
            {data.matching_skills.length > 0
              ? data.matching_skills.map((s, i) => (
                  <span key={s} className="tag match" style={{ animationDelay: `${i * 0.04}s` }}>
                    <span className="tag-dot" />{s}
                  </span>
                ))
              : <span className="tag miss">No matches found</span>
            }
          </div>
        </div>
        <div className="skill-panel right">
          <div className="panel-title">MISSING SKILLS</div>
          <div className="tags">
            {data.missing_skills.length > 0
              ? data.missing_skills.map((s, i) => (
                  <span key={s} className="tag miss" style={{ animationDelay: `${i * 0.04}s` }}>
                    <span className="tag-dot" />{s}
                  </span>
                ))
              : <span className="tag match">All clear — no gaps!</span>
            }
          </div>
        </div>
      </div>

      {/* Strengths & Weaknesses */}
      <div className="sec-head">
        <div className="sec-title">◈ PROFILE EVALUATION</div>
        <div className="sec-line" />
      </div>
      <div className="two-col">
        <div className="skill-panel">
          <div className="panel-title">STRENGTHS</div>
          {data.strengths.map((s, i) => (
            <div key={i} className="sw-item str" style={{ animationDelay: `${i * 0.06}s` }}>
              <span className="sw-icon">✦</span>
              {s}
            </div>
          ))}
        </div>
        <div className="skill-panel right">
          <div className="panel-title">WEAKNESSES</div>
          {data.weaknesses.map((w, i) => (
            <div key={i} className="sw-item wkn" style={{ animationDelay: `${i * 0.06}s` }}>
              <span className="sw-icon">⚠</span>
              {w}
            </div>
          ))}
        </div>
      </div>

      {/* Suggestions */}
      <div className="sec-head">
        <div className="sec-title">◈ IMPROVEMENT VECTORS</div>
        <div className="sec-line" />
      </div>
      <div className="suggestions">
        {data.suggestions.map((s, i) => (
          <div key={i} className="sug-card" style={{ animationDelay: `${i * 0.07}s` }}>
            <div className="sug-num">{String(i + 1).padStart(2, '0')}</div>
            <span className="sug-emoji">{EMOJIS[i % EMOJIS.length]}</span>
            <p className="sug-text">{s}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ══════════════════════════════════════════
   MAIN APP
   ══════════════════════════════════════════ */
export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [jd, setJd] = useState('');
  const [phase, setPhase] = useState<Phase>('idle');
  const [result, setResult] = useState<Analysis | null>(null);
  const [errMsg, setErrMsg] = useState('');
  const [isDemo, setIsDemo] = useState(false);
  const [backendOk, setBackendOk] = useState<boolean | null>(null); // null=checking
  const resultsRef = useRef<HTMLDivElement>(null);

  /* Ping the backend health every 10 s */
  useEffect(() => {
    const check = async () => {
      try {
        const r = await fetch('/analyze', { method: 'OPTIONS' });
        // Any response (even 405) means backend is reachable
        setBackendOk(r.status !== 0);
      } catch {
        setBackendOk(false);
      }
    };
    check();
    const id = setInterval(check, 10_000);
    return () => clearInterval(id);
  }, []);

  const scrollToResults = () =>
    setTimeout(() => resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 300);

  /* Demo mode */
  const handleDemo = useCallback(() => {
    setPhase('loading');
    setErrMsg('');
    setTimeout(() => {
      setResult(DEMO);
      setIsDemo(true);
      setPhase('done');
      scrollToResults();
    }, 2200);
  }, []);

  /* Real analysis */
  const handleAnalyze = useCallback(async () => {
    if (!file) {
      setErrMsg('Upload your resume PDF first — drag a file into the left panel.');
      setPhase('error');
      return;
    }
    if (!jd.trim()) {
      setErrMsg('Paste the job description into the right panel so AI can compare it against your resume.');
      setPhase('error');
      return;
    }

    setPhase('loading');
    setErrMsg('');
    setIsDemo(false);

    const fd = new FormData();
    fd.append('resume', file);
    fd.append('job_description', jd);

    try {
      const res = await fetch('/analyze', { method: 'POST', body: fd });
      const data = await res.json();

      if (!res.ok) {
        // Distinguish between API key error and other server errors
        const serverMsg: string = data.error || '';
        if (serverMsg.includes('GROQ_API_KEY')) {
          throw new Error('GROQ API key not configured. Add your key to the .env file: GROQ_API_KEY=gsk_...');
        }
        throw new Error(serverMsg || `Server error (${res.status})`);
      }

      setResult(data);
      setPhase('done');
      scrollToResults();
    } catch (e: unknown) {
      let msg: string;
      if (e instanceof TypeError && e.message === 'Failed to fetch') {
        msg = 'Cannot reach the Flask backend. Run: .\\venv\\Scripts\\python.exe app.py';
      } else {
        msg = e instanceof Error ? e.message : 'Unknown error — check the browser console.';
      }
      setErrMsg(msg);
      setPhase('error');
    }
  }, [file, jd]);

  const reset = () => { setPhase('idle'); setResult(null); setErrMsg(''); setIsDemo(false); };

  const isLoading = phase === 'loading';

  return (
    <>
      <SpaceBg />
      <div className="app">

        {/* ── HERO ── */}
        <header className="hero">
          <div className="ai-badge">
            <div className="badge-gem" />
            AI POWERED ANALYSIS
            <div className="badge-gem" />
          </div>

          <h1 style={{ position: 'relative' }}>
            <span className="hero-title">AI RESUME ANALYZER</span>
          </h1>

          <p className="hero-sub">Intelligent ATS Scoring &amp; Career Intelligence Platform</p>

          <div className="metrics" role="list" aria-label="Platform statistics">
            <MetricCard val="47+" lbl="Analyzed" />
            <MetricCard val="&lt;5s" lbl="Speed" />
            <MetricCard val="7"   lbl="Metrics" />
            <MetricCard val="100%" lbl="Free" />
          </div>
        </header>

        {/* ── MAIN CARD ── */}
        <main>
          <div className="main-card">
            <div className="card-header">
              <div className="dot-row">
                <div className="dot dot-r" />
                <div className="dot dot-y" />
                <div className="dot dot-g" />
              </div>
              {/* Live backend status */}
              <div
                className={`status-pill ${
                  backendOk === null ? 'chk' : backendOk ? 'ok' : 'err'
                }`}
                title={backendOk === null ? 'Checking backend...' : backendOk ? 'Flask backend connected' : 'Flask backend offline'}
              >
                <div className="status-dot" />
                {backendOk === null ? 'CHECKING' : backendOk ? 'BACKEND ONLINE' : 'BACKEND OFFLINE'}
              </div>
              <div className="card-header-title">INTERACTION_HUB.SYS // v3.0.1</div>
            </div>

            <div className="card-body">
              {/* Upload */}
              <UploadZone file={file} onChange={setFile} />

              {/* Job Description */}
              <div className="jd-side">
                <div className="side-label">JOB DESCRIPTION CONSOLE</div>
                <div className="console-wrap">
                  <div className="console-bar">
                    <div className="cb-dot cb-1" />
                    <div className="cb-dot cb-2" />
                    <div className="cb-dot cb-3" />
                    <span className="console-path">~/job_description.txt</span>
                  </div>
                  <textarea
                    className="console-textarea"
                    id="jd-input"
                    value={jd}
                    onChange={e => setJd(e.target.value)}
                    placeholder={
                      'Paste the job description here...\n\nInclude role requirements, responsibilities,\nand desired qualifications for best results.'
                    }
                    aria-label="Job description"
                  />
                </div>
              </div>
            </div>

            {/* Error */}
            {phase === 'error' && (
              <div className="error-panel" role="alert">
                <div className="error-icon-wrap">⚠</div>
                <div className="error-body">
                  <div className="error-title">ANALYSIS FAILED</div>
                  <div className="error-msg">{errMsg}</div>
                </div>
                <button className="error-close" onClick={() => setPhase('idle')} aria-label="Dismiss error">✕</button>
              </div>
            )}


            {/* Actions */}
            <div className="action-bar">
              <div className="energy-dial" aria-hidden="true">
                <div className="dial-core" />
              </div>

              <button
                className="cta-btn"
                id="analyze-btn"
                onClick={handleAnalyze}
                disabled={isLoading}
                aria-label="Analyze my resume"
              >
                <div className="cta-inner">
                  {isLoading
                    ? <><div className="spinner" /> ANALYZING...</>
                    : <><span className="cta-icon">⚡</span> ANALYZE MY RESUME</>
                  }
                </div>
                <div className="cta-glow" />
              </button>

              <button
                className="demo-btn"
                id="demo-btn"
                onClick={handleDemo}
                disabled={isLoading}
                aria-label="Load demo results"
              >
                ◈ DEMO
              </button>

              {phase === 'done' && (
                <button className="reset-btn" id="reset-btn" onClick={reset} aria-label="Reset">
                  ↺ RESET
                </button>
              )}
            </div>
          </div>

          {/* ── RESULTS AREA ── */}
          <div ref={resultsRef}>
            {phase === 'loading' && <Loader />}

            {phase === 'done' && result && (
              <Results data={result} isDemo={isDemo} />
            )}

            {(phase === 'idle' || phase === 'error') && (
              <div className="empty-box">
                <span className="empty-glyph">🛸</span>
                <div className="empty-title">AWAITING MISSION DATA</div>
                <div className="empty-sub">
                  Upload your resume · paste a job description · click Analyze
                  <br />— or hit DEMO to preview the experience instantly
                </div>
              </div>
            )}
          </div>
        </main>

        {/* ── FOOTER ── */}
        <footer className="footer">
          <p className="footer-txt">
            POWERED BY <span>GROQ AI</span> · <span>LLAMA 3.3</span> · BUILT FOR THE FUTURE
          </p>
        </footer>
      </div>
    </>
  );
}
