import { useState } from 'react'
import Dashboard from './components/Dashboard'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  return (
    <div className="app-container">
      <aside className="sidebar">
        <h1 className="title-glow" style={{ fontSize: '1.8rem', marginBottom: '40px' }}>Bot DCA</h1>
        
        <nav>
          <a href="#" className={`nav-link ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveTab('dashboard')}>
             Dashboard
          </a>
          <a href="#" className={`nav-link ${activeTab === 'strategy' ? 'active' : ''}`} onClick={() => setActiveTab('strategy')}>
             Strategies & AI
          </a>
          <a href="#" className={`nav-link ${activeTab === 'rounds' ? 'active' : ''}`} onClick={() => setActiveTab('rounds')}>
             Rounds Tracker
          </a>
        </nav>
      </aside>
      
      <main className="content-area">
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'strategy' && (
          <div className="glass-panel animate-slide-up">
            <h2>Strategy & Recommendation Engine</h2>
            <br/>
            <p className="text-muted">The Recommendation Engine predicts optimal DCA configurations based on historical backtesting.</p>
            <br/>
            <button className="btn-neon">Analyze DCA Logic</button>
          </div>
        )}
        {activeTab === 'rounds' && (
          <div className="glass-panel animate-slide-up">
            <h2>Rounds Tracker</h2>
            <br/>
            <p className="text-muted">Detailed timeline of entry and exit points for all trades.</p>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
