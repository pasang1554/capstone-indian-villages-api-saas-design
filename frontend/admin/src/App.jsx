import React, { useState, useEffect } from 'react'
import axios from 'axios'

const API = '/api/admin'
const API_KEY = prompt('Enter Admin API Key:') || ''

const api = axios.create({ baseURL: API, headers: { 'X-API-Key': API_KEY } })

function App() {
  const [tab, setTab] = useState('keys')
  const [keys, setKeys] = useState([])
  const [analytics, setAnalytics] = useState({})
  const [logs, setLogs] = useState([])
  const [newKeyName, setNewKeyName] = useState('')

  const fetchKeys = () => api.get('/keys').then(r => setKeys(r.data))
  const fetchAnalytics = () => api.get('/analytics').then(r => setAnalytics(r.data))
  const fetchLogs = () => api.get('/logs').then(r => setLogs(r.data))

  useEffect(() => { fetchKeys(); fetchAnalytics(); fetchLogs() }, [])

  const createKey = () => {
    if (!newKeyName) return
    api.post('/keys', null, { params: { name: newKeyName } }).then(r => {
      alert(`New key: ${r.data.key}`)
      setNewKeyName('')
      fetchKeys()
    })
  }

  const toggleKey = (id) => api.put(`/keys/${id}/toggle`).then(() => fetchKeys())

  return (
    <div style={{ fontFamily: 'sans-serif', maxWidth: 1200, margin: '0 auto', padding: 20 }}>
      <h1>Village API - Admin Dashboard</h1>
      <div style={{ marginBottom: 20 }}>
        {['keys', 'analytics', 'logs'].map(t => (
          <button key={t} onClick={() => setTab(t)} style={{ marginRight: 10, background: tab === t ? '#333' : '#eee', color: tab === t ? '#fff' : '#000', padding: '8px 16px' }}>{t.toUpperCase()}</button>
        ))}
      </div>

      {tab === 'keys' && (
        <div>
          <h2>API Key Management</h2>
          <div style={{ marginBottom: 20 }}>
            <input placeholder="Key name" value={newKeyName} onChange={e => setNewKeyName(e.target.value)} style={{ padding: 8, marginRight: 10 }} />
            <button onClick={createKey} style={{ padding: '8px 16px' }}>Create Key</button>
          </div>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead><tr><th style={{ textAlign: 'left', padding: 8 }}>Name</th><th>Key</th><th>Requests</th><th>Status</th><th>Action</th></tr></thead>
            <tbody>
              {keys.map(k => (
                <tr key={k.id} style={{ borderBottom: '1px solid #eee' }}>
                  <td style={{ padding: 8 }}>{k.name}</td>
                  <td>{k.key}</td>
                  <td>{k.requests}</td>
                  <td>{k.is_active ? 'Active' : 'Inactive'}</td>
                  <td><button onClick={() => toggleKey(k.id)}>{k.is_active ? 'Disable' : 'Enable'}</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === 'analytics' && (
        <div>
          <h2>Usage Analytics</h2>
          <p>Total Requests: <strong>{analytics.total_requests || 0}</strong></p>
          <h3>Top Endpoints</h3>
          <ul>
            {(analytics.top_endpoints || []).map((e, i) => (
              <li key={i}>{e.endpoint} - {e.count} requests</li>
            ))}
          </ul>
        </div>
      )}

      {tab === 'logs' && (
        <div>
          <h2>Request Logs</h2>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead><tr><th style={{ textAlign: 'left', padding: 8 }}>Time</th><th>Endpoint</th><th>Status</th><th>Latency</th></tr></thead>
            <tbody>
              {logs.map(l => (
                <tr key={l.id} style={{ borderBottom: '1px solid #eee' }}>
                  <td style={{ padding: 8 }}>{new Date(parseFloat(l.timestamp)*1000).toLocaleString()}</td>
                  <td>{l.endpoint}</td>
                  <td>{l.status}</td>
                  <td>{l.latency_ms}ms</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default App
