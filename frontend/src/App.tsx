import { FormEvent, useEffect, useMemo, useState } from 'react';

type OrderStatus = 'new' | 'scheduled' | 'in_progress' | 'completed' | 'on_hold';
type OrderPriority = 'normal' | 'high' | 'urgent';

type WorkOrder = {
  id: number;
  order_number: string;
  client_name: string;
  site_name: string;
  address: string;
  status: OrderStatus;
  priority: OrderPriority;
  assigned_to: string;
  scheduled_at: string;
  description: string;
  task_count: number;
  completion_percent: number;
  notes: string;
  created_at: string;
};

type Client = {
  id: number;
  name: string;
  company: string;
  email: string;
  phone: string;
};

type Site = {
  id: number;
  name: string;
  address: string;
  city: string;
  timezone: string;
};

const emptyForm = {
  order_number: '',
  client_name: '',
  site_name: '',
  address: '',
  status: 'new' as OrderStatus,
  priority: 'normal' as OrderPriority,
  assigned_to: '',
  scheduled_at: '',
  description: '',
  task_count: 1,
  completion_percent: 0,
  notes: '',
};

function App() {
  const [orders, setOrders] = useState<WorkOrder[]>([]);
  const [clients, setClients] = useState<Client[]>([]);
  const [sites, setSites] = useState<Site[]>([]);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin123');
  const [form, setForm] = useState(emptyForm);
  const [metrics, setMetrics] = useState({ total: 0, active: 0, urgent: 0, completed: 0, clients: 0, sites: 0 });

  const loadOrders = async () => {
    const res = await fetch('/api/orders');
    const data = await res.json();
    setOrders(data);
  };

  const loadClients = async () => {
    const res = await fetch('/api/clients');
    const data = await res.json();
    setClients(data);
  };

  const loadSites = async () => {
    const res = await fetch('/api/sites');
    const data = await res.json();
    setSites(data);
  };

  const loadMetrics = async () => {
    const res = await fetch('/api/metrics');
    const data = await res.json();
    setMetrics(data);
  };

  useEffect(() => {
    if (isLoggedIn) {
      loadOrders();
      loadMetrics();
      loadClients();
      loadSites();
    }
  }, [isLoggedIn]);

  const handleLogin = async (event: FormEvent) => {
    event.preventDefault();
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });

    if (res.ok) {
      setIsLoggedIn(true);
    }
  };

  const filteredOrders = useMemo(() => {
    return orders.filter((order) => {
      const matchesSearch = `${order.order_number} ${order.client_name} ${order.site_name}`.toLowerCase().includes(search.toLowerCase());
      const matchesStatus = statusFilter === 'all' || order.status === statusFilter;
      return matchesSearch && matchesStatus;
    });
  }, [orders, search, statusFilter]);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    const payload = { ...form, task_count: Number(form.task_count), completion_percent: Number(form.completion_percent) };
    const res = await fetch('/api/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (res.ok) {
      setForm(emptyForm);
      loadOrders();
      loadMetrics();
    }
  };

  const handleDelete = async (id: number) => {
    await fetch(`/api/orders/${id}`, { method: 'DELETE' });
    loadOrders();
    loadMetrics();
  };

  const updateField = (key: keyof typeof emptyForm, value: string | number) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  if (!isLoggedIn) {
    return (
      <div className="login-shell">
        <div className="login-card">
          <div className="brand-wrap">
            <div className="brand-mark">F</div>
            <div>
              <div className="eyebrow">Field service SaaS</div>
              <h1>FieldFlow AI</h1>
            </div>
          </div>

          <form onSubmit={handleLogin} className="login-form">
            <label>
              Username
              <input value={username} onChange={(e) => setUsername(e.target.value)} />
            </label>
            <label>
              Password
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            </label>
            <button type="submit" className="primary-button full-width">Sign in</button>
          </form>

          <div className="login-footer">Built by ki9521787@gmail.com</div>
        </div>
      </div>
    );
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-wrap">
          <div className="brand-mark">F</div>
          <div>
            <div className="eyebrow">B2B SaaS</div>
            <h1>FieldFlow AI</h1>
          </div>
        </div>

        <nav className="nav-links">
          <button className="nav-item active">Dashboard</button>
          <button className="nav-item">Orders</button>
          <button className="nav-item">Dispatch</button>
          <button className="nav-item">Reports</button>
          <button className="nav-item">Clients</button>
        </nav>

        <div className="sidebar-panel">
          <div className="panel-title">Operational pulse</div>
          <div className="mini-metric"><span>Open work</span><strong>{metrics.active}</strong></div>
          <div className="mini-metric"><span>Urgent</span><strong>{metrics.urgent}</strong></div>
          <div className="mini-metric"><span>Completed</span><strong>{metrics.completed}</strong></div>
        </div>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div>
            <div className="eyebrow">Operations overview</div>
            <h2>Service work orders</h2>
          </div>
          <button className="primary-button">+ New order</button>
        </header>

        <section className="metrics-grid">
          <div className="metric-card accent"><span>Total orders</span><strong>{metrics.total}</strong></div>
          <div className="metric-card"><span>Open jobs</span><strong>{metrics.active}</strong></div>
          <div className="metric-card"><span>Urgent</span><strong>{metrics.urgent}</strong></div>
          <div className="metric-card"><span>Clients</span><strong>{metrics.clients}</strong></div>
          <div className="metric-card"><span>Sites</span><strong>{metrics.sites}</strong></div>
          <div className="metric-card"><span>Completed</span><strong>{metrics.completed}</strong></div>
        </section>

        <section className="clients-grid">
          <div className="stats-box">
            <h3>Clients</h3>
            <ul>
              {clients.slice(0, 5).map((client) => (
                <li key={client.id}>{client.company || client.name}</li>
              ))}
            </ul>
          </div>
          <div className="stats-box">
            <h3>Sites</h3>
            <ul>
              {sites.slice(0, 5).map((site) => (
                <li key={site.id}>{site.name}</li>
              ))}
            </ul>
          </div>
        </section>

        <section className="content-grid">
          <div className="orders-panel">
            <div className="panel-header">
              <h3>Orders</h3>
              <div className="toolbar">
                <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search order, client, site" />
                <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
                  <option value="all">All statuses</option>
                  <option value="new">New</option>
                  <option value="scheduled">Scheduled</option>
                  <option value="in_progress">In progress</option>
                  <option value="completed">Completed</option>
                  <option value="on_hold">On hold</option>
                </select>
              </div>
            </div>

            <div className="order-list">
              {filteredOrders.map((order) => (
                <div key={order.id} className="order-card">
                  <div className="order-row">
                    <div>
                      <div className="order-number">#{order.order_number}</div>
                      <h4>{order.site_name}</h4>
                    </div>
                    <span className={`pill ${order.status}`}>{order.status}</span>
                  </div>
                  <div className="meta-grid">
                    <span>Client: {order.client_name}</span>
                    <span>Assigned: {order.assigned_to}</span>
                    <span>Priority: {order.priority}</span>
                    <span>Date: {order.scheduled_at || 'TBD'}</span>
                  </div>
                  <p>{order.description || 'No description provided.'}</p>
                  <div className="progress-bar-wrap"><div className="progress-bar" style={{ width: `${order.completion_percent}%` }} /></div>
                  <div className="inline-actions">
                    <button className="ghost-button">View</button>
                    <button className="ghost-button danger" onClick={() => handleDelete(order.id)}>Delete</button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="form-panel">
            <div className="panel-header"><h3>Create work order</h3></div>
            <form onSubmit={handleSubmit} className="order-form">
              <label>
                Order number
                <input value={form.order_number} onChange={(e) => updateField('order_number', e.target.value)} required />
              </label>
              <label>
                Client name
                <input value={form.client_name} onChange={(e) => updateField('client_name', e.target.value)} required />
              </label>
              <label>
                Site name
                <input value={form.site_name} onChange={(e) => updateField('site_name', e.target.value)} required />
              </label>
              <label>
                Address
                <input value={form.address} onChange={(e) => updateField('address', e.target.value)} required />
              </label>
              <div className="two-col">
                <label>
                  Status
                  <select value={form.status} onChange={(e) => updateField('status', e.target.value)}>
                    <option value="new">New</option>
                    <option value="scheduled">Scheduled</option>
                    <option value="in_progress">In progress</option>
                    <option value="completed">Completed</option>
                    <option value="on_hold">On hold</option>
                  </select>
                </label>
                <label>
                  Priority
                  <select value={form.priority} onChange={(e) => updateField('priority', e.target.value)}>
                    <option value="normal">Normal</option>
                    <option value="high">High</option>
                    <option value="urgent">Urgent</option>
                  </select>
                </label>
              </div>
              <div className="two-col">
                <label>
                  Assigned to
                  <input value={form.assigned_to} onChange={(e) => updateField('assigned_to', e.target.value)} />
                </label>
                <label>
                  Scheduled date
                  <input type="date" value={form.scheduled_at} onChange={(e) => updateField('scheduled_at', e.target.value)} />
                </label>
              </div>
              <label>
                Description
                <textarea value={form.description} onChange={(e) => updateField('description', e.target.value)} rows={4} />
              </label>
              <div className="two-col">
                <label>
                  Tasks count
                  <input type="number" min={0} value={form.task_count} onChange={(e) => updateField('task_count', Number(e.target.value))} />
                </label>
                <label>
                  Completion %
                  <input type="number" min={0} max={100} value={form.completion_percent} onChange={(e) => updateField('completion_percent', Number(e.target.value))} />
                </label>
              </div>
              <label>
                Notes
                <textarea value={form.notes} onChange={(e) => updateField('notes', e.target.value)} rows={3} />
              </label>
              <button type="submit" className="primary-button full-width">Save order</button>
            </form>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
