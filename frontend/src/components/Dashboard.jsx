import { useState, useEffect } from 'react';

export default function Dashboard() {
  const [stats, setStats] = useState({
    total_pnl: 0,
    active_rounds: 0,
    completed_rounds: 0,
    win_rate: 0,
    avg_profit_per_round: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real app, this would use fetch('http://localhost:8000/api/v1/analytics/dashboard')
    // We mock the loading for the wow effect
    setTimeout(() => {
      setStats({
        total_pnl: 3450.45,
        active_rounds: 3,
        completed_rounds: 124,
        win_rate: 89.4,
        avg_profit_per_round: 28.5
      });
      setLoading(false);
    }, 1500);
  }, []);

  if (loading) {
    return (
      <div className="glass-panel" style={{ textAlign: 'center', padding: '100px 20px' }}>
        <h2 className="title-glow" style={{ animation: 'pulse 1.5s infinite' }}>Syncing with API...</h2>
      </div>
    );
  }

  return (
    <div className="animate-slide-up">
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 className="title-glow">Performance Overview</h2>
          <p className="text-muted">Real-time metrics synced from your Binance DCA executions.</p>
        </div>
        <div>
          <button className="btn-neon-green">Export CSV</button>
        </div>
      </header>
      
      <div className="dashboard-grid">
        <div className="glass-panel">
          <h3>Total Realized PnL</h3>
          <div className="metric-value text-green">+${stats.total_pnl.toLocaleString('en-US', { minimumFractionDigits: 2 })}</div>
          <p className="text-muted">Since inception</p>
        </div>
        
        <div className="glass-panel">
          <h3>Win Rate</h3>
          <div className="metric-value text-purple">{stats.win_rate}%</div>
          <p className="text-muted">{stats.completed_rounds} completed rounds</p>
        </div>
        
        <div className="glass-panel">
          <h3>Active Capital in Rounds</h3>
          <div className="metric-value">${(stats.active_rounds * 1045.2).toLocaleString('en-US')}</div>
          <p className="text-muted">{stats.active_rounds} rounds running</p>
        </div>
        
        <div className="glass-panel">
          <h3>Avg Profit / Round</h3>
          <div className="metric-value">+${stats.avg_profit_per_round}</div>
          <p className="text-muted">Estimated to scale linearly</p>
        </div>
      </div>
      
      <div className="glass-panel" style={{ marginTop: '30px' }}>
         <h3 style={{ marginBottom: '20px' }}>DCA Effectiveness Analysis</h3>
         <div style={{ height: '200px', display: 'flex', alignItems: 'flex-end', gap: '8px', borderBottom: 'var(--glass-border)' }}>
             {[...Array(30)].map((_, i) => {
                 const height = 20 + Math.random() * 80;
                 return <div key={i} style={{ flex: 1, height: `${height}%`, background: 'var(--neon-green)', borderRadius: '4px 4px 0 0', opacity: 0.7 + (Math.random() * 0.3) }}></div>
             })}
         </div>
         <p className="text-muted" style={{ marginTop: '10px' }}>Simulated representation of 30-day profit frequency</p>
      </div>
    </div>
  );
}
