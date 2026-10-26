import { useMemo, useState } from 'react';

const steps = [
  { id: '01', title: 'Upload, review, take off', subtitle: 'FieldFlow draws from your project context' },
  { id: '02', title: 'Estimate with AI', subtitle: 'Materials, labor, risk and pricing' },
  { id: '03', title: 'Export ready', subtitle: 'Send quotes and scope packages fast' },
  { id: '04', title: 'Win more jobs', subtitle: 'Reduce back-and-forth and speed up close' },
];

const workItems = [
  'Domestic cold water',
  'Domestic hot water',
  'Sanitary waste',
  'Rainwater drainage',
];

function App() {
  const [signedIn, setSignedIn] = useState(false);

  const rightPanel = useMemo(
    () => [
      { label: 'Context review', value: 'Drawing set 04-A', detail: 'DOMESTIC COLD WATER', text: 'Type L copper - sweat - 2" and below' },
      { label: 'Domestic hot water', detail: 'DOMESTIC HOT WATER', text: 'Type L copper - sweat - insulate where noted' },
      { label: 'Sanitary waste', detail: 'SANITARY WASTE', text: 'Cast iron - no hub - 2"-4"' },
    ],
    [],
  );

  return (
    <div className="page-shell">
      <header className="topbar">
        <div className="brand">FieldFlow Ai</div>
      </header>

      <main className="hero-shell">
        <div className="hero-grid">
          <section className="hero-copy-wrap">
            <div className="brand-pill">FieldFlow</div>

            <div className="hero-badge">FOUNDING PRICING — NOW AVAILABLE</div>

            <h1>
              AI-assisted takeoff for
              <span className="accent"> plumbing &amp;<br />mechanical estimators.</span>
            </h1>

            <p className="subcopy">
              Upload a drawing set. FieldFlow drafts the project context — systems, materials,
              joining methods, size ranges — so your team can review, measure runs, click fittings,
              and export totals faster than Bluebeam workflows allow.
            </p>

            <div className="cta-row">
              <button type="button" className="primary-button" onClick={() => setSignedIn(true)}>
                Open the app
              </button>
              <button type="button" className="secondary-button">
                See pricing
              </button>
            </div>

            <div className="fine-print">No credit card required for the 14-day trial.</div>
          </section>

          <aside className="demo-panel">
            <div className="demo-panel-header">
              <div className="demo-panel-title">Context review · Drawing set 04-A</div>
            </div>

            <div className="list-stack">
              {rightPanel.map((item) => (
                <div key={item.detail} className="stack-item">
                  <div className="stack-topline">{item.detail}</div>
                  <div className="stack-text">{item.text}</div>
                </div>
              ))}
            </div>

            <div className="summary-box">
              <div className="summary-label">RUN LOGGED</div>
              <div className="summary-value">184 ft · 6 elbows · 2 tees</div>
            </div>
          </aside>
        </div>

        <div className="bottom-section">
          <h2>Upload, review, take off, export.</h2>
          <p>
            FieldFlow stays guided and tied to the drawing language — your team isn&apos;t inventing
            terminology from scratch.
          </p>

          <div className="step-grid">
            {steps.map((step) => (
              <div key={step.id} className="step-card">
                <div className="step-number">{step.id}</div>
                <div className="step-title">{step.title}</div>
                <div className="step-subtitle">{step.subtitle}</div>
              </div>
            ))}
          </div>
        </div>
      </main>

      <footer className="site-footer">
        Built and owned by <strong>ki9521787@gmail.com</strong>
      </footer>
    </div>
  );
}

export default App;

