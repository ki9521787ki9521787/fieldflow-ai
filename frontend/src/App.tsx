import { useEffect, useState } from 'react';

interface Order {
  id: string;
  client: string;
  system: string;
  status: string;
  priority: string;
  technician: string;
}

export default function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [role, setRole] = useState<string>(localStorage.getItem('role') || 'GUEST');
  const [view, setView] = useState<'landing' | 'app' | 'pricing'>('landing');
  const [orders, setOrders] = useState<Order[]>([]);
  const [email, setEmail] = useState('admin@fieldflowai.com');
  const [password, setPassword] = useState('admin123');
  const [clientInput, setClientInput] = useState('');
  const [systemInput, setSystemInput] = useState('');
  const [error, setError] = useState('');

  const fetchOrders = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/orders');
      const data = await res.json();
      if (data.data) setOrders(data.data);
    } catch (err) {
      console.error('Failed to fetch orders', err);
    }
  };

  useEffect(() => {
    if (token) {
      fetchOrders();
    }
  }, [token]);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const res = await fetch('http://localhost:8000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData,
      });
      const data = await res.json();
      if (res.ok) {
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('role', data.role);
        setToken(data.access_token);
        setRole(data.role);
        setView('app');
      } else {
        setError(data.detail || 'Login failed');
      }
    } catch (err) {
      setError('Connection error with backend server');
    }
  };

  const handleLogout = () => {
    localStorage.clear();
    setToken(null);
    setRole('GUEST');
    setView('landing');
  };

  const handleCreateOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!clientInput || !systemInput) return;
    try {
      const res = await fetch('http://localhost:8000/api/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ client: clientInput, system: systemInput, priority: 'High' }),
      });
      if (res.ok) {
        setClientInput('');
        setSystemInput('');
        fetchOrders();
      }
    } catch (err) {
      console.error('Failed to create order', err);
    }
  };

  if (view === 'app' && token) {
    return (
      <div className="saas-shell">
        <aside className="saas-sidebar">
          <div className="sidebar-brand">FieldFlow AI</div>
          <div className="sidebar-user">Role: {role}</div>
          <nav className="sidebar-nav">
            <button className="nav-item active">Command Center</button>
            <button className="nav-item" onClick={() => setView('pricing')}>Pricing Tiers</button>
            <button className="nav-item" onClick={() => setView('landing')}>Public Site</button>
          </nav>
          <div className="sidebar-footer">
            Owner &amp; Author:<br /><strong>ki9521787@gmail.com</strong>
          </div>
        </aside>

        <main className="saas-main">
          <header className="saas-header">
            <h1>Operational Dispatch Dashboard</h1>
            <div className="header-actions">
              <span className="secure-badge">Connected to API</span>
              <button className="primary-button" onClick={handleLogout}>Sign Out</button>
            </div>
          </header>

          <section className="metrics-grid">
            <div className="metric-card">
              <div className="metric-label">Total Work Orders</div>
              <div className="metric-value">{orders.length}</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">System Status</div>
              <div className="metric-value text-green">Online</div>
            </div>
          </section>

          <section className="dashboard-content">
            <div className="panel-box">
              <h3>Active Service Dispatches</h3>
              <table className="data-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Client</th>
                    <th>System</th>
                    <th>Priority</th>
                    <th>Status</th>
                    <th>Technician</th>
                  </tr>
                </thead>
                <tbody>
                  {orders.map((o) => (
                    <tr key={o.id}>
                      <td><strong>{o.id}</strong></td>
                      <td>{o.client}</td>
                      <td>{o.system}</td>
                      <td><span className="badge priority">{o.priority}</span></td>
                      <td><span className="badge status">{o.status}</span></td>
                      <td>{o.technician}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="panel-box create-box">
              <h3>Create Order via API</h3>
              <form onSubmit={handleCreateOrder} className="create-form">
                <div className="form-group">
                  <label>Client Name</label>
                  <input type="text" value={clientInput} onChange={(e) => setClientInput(e.target.value)} placeholder="Client Name" required />
                </div>
                <div className="form-group">
                  <label>System Specification</label>
                  <input type="text" value={systemInput} onChange={(e) => setSystemInput(e.target.value)} placeholder="System Scope" required />
                </div>
                <button type="submit" className="primary-button full-width">Dispatch Order</button>
              </form>
            </div>
          </section>
        </main>
      </div>
    );
  }

  if (view === 'pricing') {
    return (
      <div className="page-shell">
        <header className="topbar">
          <div className="brand" onClick={() => setView('landing')} style={{ cursor: 'pointer' }}>FieldFlow AI</div>
          <button className="ghost-button" onClick={() => setView('landing')}>Home</button>
        </header>
        <main className="pricing-wrap" style={{ padding: '3rem', textAlign: 'center' }}>
          <h1>Transparent Pricing</h1>
          <p>Choose your tier to scale field operations.</p>
          <div style={{ display: 'flex', gap: '2rem', justifyContent: 'center', marginTop: '2rem' }}>
            <div className="panel-box" style={{ width: '300px' }}>
              <h3>Starter</h3>
              <h2>$199 / mo</h2>
              <button className="primary-button full-width" onClick={() => setView('landing')}>Select</button>
            </div>
            <div className="panel-box" style={{ width: '300px', border: '1px solid #5bb0f0' }}>
              <h3>Enterprise Pro</h3>
              <h2>$599 / mo</h2>
              <button className="primary-button full-width" onClick={() => setView('landing')}>Select</button>
            </div>
          </div>
        </main>
        <footer className="site-footer">Created by <strong>ki9521787@gmail.com</strong></footer>
      </div>
    );
  }

  return (
    <div className="page-shell">
      <header className="topbar">
        <div className="brand">FieldFlow AI</div>
        <div className="topbar-actions">
          <button className="ghost-button" onClick={() => setView('pricing')}>Pricing</button>
          <button className="primary-button" onClick={() => setView('app')}>Sign In</button>
        </div>
      </header>

      <main className="hero-shell">
        <div className="hero-grid">
          <section className="hero-copy-wrap">
            <div className="brand-pill">FieldFlow AI Platform</div>
            <h1>Autonomous operations &amp; <span className="accent">AI takeoff for mechanical teams.</span></h1>
            <p className="subcopy">
              Manage work orders, track telemetry, and automate dispatch from a secure single source of truth.
            </p>

            <div className="panel-box" style={{ marginTop: '2rem', maxWidth: '400px' }}>
              <h3>Sign In to Workspace</h3>
              {error && <div style={{ color: '#e74c3c', fontSize: '0.85rem', marginBottom: '0.5rem' }}>{error}</div>}
              <form onSubmit={handleLogin} className="create-form">
                <div className="form-group">
                  <label>Email</label>
                  <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                </div>
                <div className="form-group">
                  <label>Password</label>
                  <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                </div>
                <button type="submit" className="primary-button full-width">Authorize &amp; Enter</button>
              </form>
            </div>
            <div className="fine-print">Default admin: admin@fieldflowai.com / admin123. Owner: ki9521787@gmail.com</div>
          </section>
        </div>
      </main>

      <footer className="site-footer">
        FieldFlow AI · Built and Owned by <strong>ki9521787@gmail.com</strong>
      </footer>
    </div>
  );
}
