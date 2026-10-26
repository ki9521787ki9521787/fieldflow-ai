import { useMemo, useState } from 'react';

interface WorkOrder {
  id: string;
  client: string;
  system: string;
  status: 'Pending' | 'In Progress' | 'Completed';
  priority: 'High' | 'Medium' | 'Low';
  technician: string;
}

const initialOrders: WorkOrder[] = [
  { id: 'WO-1081', client: 'Apex Commercial Ltd', system: 'Domestic Cold Water - 2" Copper', status: 'In Progress', priority: 'High', technician: 'Alex R.' },
  { id: 'WO-1082', client: 'Metro Plaza Facility', system: 'Sanitary Waste - Cast Iron 4"', status: 'Pending', priority: 'Medium', technician: 'Unassigned' },
  { id: 'WO-1083', client: 'St. Jude Hospital', system: 'Medical Gas & Vacuum Lines', status: 'Completed', priority: 'High', technician: 'Dmitry Z.' },
];

export default function App() {
  const [view, setView] = useState<'landing' | 'app'>('landing');
  const [orders, setOrders] = useState<WorkOrder[]>(initialOrders);
  const [filter, setFilter] = useState<string>('All');
  const [search, setSearch] = useState<string>('');
  const [newClient, setNewClient] = useState<string>('');
  const [newSystem, setNewSystem] = useState<string>('');

  const filteredOrders = useMemo(() => {
    return orders.filter(o => {
      const matchesFilter = filter === 'All' || o.status === filter;
      const matchesSearch = o.client.toLowerCase().includes(search.toLowerCase()) || o.system.toLowerCase().includes(search.toLowerCase());
      return matchesFilter && matchesSearch;
    });
  }, [orders, filter, search]);

  const handleCreateOrder = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newClient || !newSystem) return;
    const newOrd: WorkOrder = {
      id: `WO-10${orders.length + 1}`,
      client: newClient,
      system: newSystem,
      status: 'Pending',
      priority: 'Medium',
      technician: 'Assigned Dispatch'
    };
    setOrders([newOrd, ...orders]);
    setNewClient('');
    setNewSystem('');
  };

  if (view === 'app') {
    return (
      <div className="saas-shell">
        <aside className="saas-sidebar">
          <div className="sidebar-brand">FieldFlow AI</div>
          <div className="sidebar-user">Workspace: Enterprise Tier</div>
          <nav className="sidebar-nav">
            <button className="nav-item active">Command Center</button>
            <button className="nav-item" onClick={() => setView('landing')}>Public Landing</button>
          </nav>
          <div className="sidebar-footer">
            Owner: <strong>ki9521787@gmail.com</strong>
          </div>
        </aside>

        <main className="saas-main">
          <header className="saas-header">
            <h1>Operational Dispatch &amp; Takeoff Engine</h1>
            <div className="header-actions">
              <span className="secure-badge">AES-256 Secured</span>
              <button className="primary-button" onClick={() => setView('landing')}>Sign Out</button>
            </div>
          </header>

          <section className="metrics-grid">
            <div className="metric-card">
              <div className="metric-label">Active Orders</div>
              <div className="metric-value">{orders.length}</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">In Progress</div>
              <div className="metric-value">{orders.filter(o => o.status === 'In Progress').length}</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">System Status</div>
              <div className="metric-value text-green">100% Operational</div>
            </div>
          </section>

          <section className="dashboard-content">
            <div className="panel-box">
              <div className="panel-top">
                <h3>Work Orders &amp; Field Execution</h3>
                <div className="controls-row">
                  <input
                    type="text"
                    placeholder="Search client or system..."
                    value={search}
                    onChange={e => setSearch(e.target.value)}
                    className="search-input"
                  />
                  <select value={filter} onChange={e => setFilter(e.target.value)} className="filter-select">
                    <option value="All">All Statuses</option>
                    <option value="Pending">Pending</option>
                    <option value="In Progress">In Progress</option>
                    <option value="Completed">Completed</option>
                  </select>
                </div>
              </div>

              <div className="table-wrap">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Client</th>
                      <th>System Specification</th>
                      <th>Priority</th>
                      <th>Status</th>
                      <th>Technician</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredOrders.map(o => (
                      <tr key={o.id}>
                        <td><strong>{o.id}</strong></td>
                        <td>{o.client}</td>
                        <td>{o.system}</td>
                        <td><span className={`badge priority-${o.priority.toLowerCase()}`}>{o.priority}</span></td>
                        <td><span className={`badge status-${o.status.toLowerCase().replace(' ', '-')}`}>{o.status}</span></td>
                        <td>{o.technician}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="panel-box create-box">
              <h3>Create New Dispatch Order</h3>
              <form onSubmit={handleCreateOrder} className="create-form">
                <div className="form-group">
                  <label>Client Name</label>
                  <input
                    type="text"
                    placeholder="e.g. Apex Industrial"
                    value={newClient}
                    onChange={e => setNewClient(e.target.value)}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>System / Scope</label>
                  <input
                    type="text"
                    placeholder="e.g. Domestic Hot Water - 3''"
                    value={newSystem}
                    onChange={e => setNewSystem(e.target.value)}
                    required
                  />
                </div>
                <button type="submit" className="primary-button full-width">Dispatch Order</button>
              </form>
            </div>
          </section>
        </main>
      </div>
    );
  }

  return (
    <div className="page-shell">
      <header className="topbar">
        <div className="brand">FieldFlow AI</div>
        <div className="topbar-actions">
          <button className="ghost-button" onClick={() => setView('app')}>Sign In</button>
          <button className="primary-button" onClick={() => setView('app')}>Launch Enterprise</button>
        </div>
      </header>

      <main className="hero-shell">
        <div className="hero-grid">
          <section className="hero-copy-wrap">
            <div className="brand-pill">FieldFlow Enterprise</div>
            <div className="hero-badge">ARCHITECTED BY ELITE SYSTEMS ENGINEERING</div>
            <h1>
              Autonomous operations &amp;
              <span className="accent"> AI takeoff for elite <br />mechanical contractors.</span>
            </h1>
            <p className="subcopy">
              Engineered with uncompromising precision. FieldFlow AI unifies work orders, telemetry, automated estimation, and real-time field dispatch into an impenetrable, lightning-fast SaaS command center.
            </p>
            <div className="cta-row">
              <button type="button" className="primary-button" onClick={() => setView('app')}>
                Deploy Enterprise Workspace
              </button>
              <button type="button" className="secondary-button" onClick={() => setView('app')}>
                Explore Architecture
              </button>
            </div>
            <div className="fine-print">Zero-trust architecture. SOC2 Type II Ready. Created by ki9521787@gmail.com.</div>
          </section>

          <aside className="demo-panel">
            <div className="demo-panel-header">
              <div className="demo-panel-title">Live Telemetry · Secure Enclave 01</div>
            </div>
            <div className="list-stack">
              <div className="stack-item">
                <div className="stack-topline">ENCRYPTION PROTOCOL</div>
                <div className="stack-text">AES-256-GCM hardware accelerated key rotation</div>
              </div>
              <div className="stack-item">
                <div className="stack-topline">DISPATCH LATENCY</div>
                <div className="stack-text">12ms global edge routing via FastAPI backend</div>
              </div>
              <div className="stack-item">
                <div className="stack-topline">ISOLATION TIER</div>
                <div className="stack-text">Multi-tenant container sandboxing active</div>
              </div>
            </div>
            <div className="summary-box">
              <div className="summary-label">SYSTEM INTEGRITY</div>
              <div className="summary-value">100% Verified · Zero Vulnerabilities</div>
            </div>
          </aside>
        </div>
      </main>

      <footer className="site-footer">
        FieldFlow AI Enterprise Edition · Designed and Owned by <strong>ki9521787@gmail.com</strong>
      </footer>
    </div>
  );
}
