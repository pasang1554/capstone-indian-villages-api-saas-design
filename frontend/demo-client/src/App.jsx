import React, { useState, useEffect } from 'react'
import axios from 'axios'

const API = '/api/v1'
const API_KEY = prompt('Enter API Key:') || ''

const api = axios.create({ baseURL: API, headers: { 'X-API-Key': API_KEY } })

function App() {
  const [countries, setCountries] = useState([])
  const [states, setStates] = useState([])
  const [districts, setDistricts] = useState([])
  const [subDistricts, setSubDistricts] = useState([])
  const [villages, setVillages] = useState([])
  const [selected, setSelected] = useState({ country: '', state: '', district: '', subDistrict: '' })
  const [search, setSearch] = useState('')

  useEffect(() => { api.get('/countries').then(r => setCountries(r.data)) }, [])

  useEffect(() => {
    if (selected.country) api.get(`/states?country_id=${selected.country}`).then(r => setStates(r.data))
  }, [selected.country])

  useEffect(() => {
    if (selected.state) api.get(`/districts?state_id=${selected.state}`).then(r => setDistricts(r.data))
  }, [selected.state])

  useEffect(() => {
    if (selected.district) api.get(`/sub-districts?district_id=${selected.district}`).then(r => setSubDistricts(r.data))
  }, [selected.district])

  useEffect(() => {
    const params = new URLSearchParams()
    if (selected.subDistrict) params.append('sub_district_id', selected.subDistrict)
    if (selected.district) params.append('district_id', selected.district)
    if (selected.state) params.append('state_id', selected.state)
    if (search) params.append('search', search)
    api.get(`/villages?${params}`).then(r => setVillages(r.data.data))
  }, [selected.subDistrict, search])

  return (
    <div style={{ fontFamily: 'sans-serif', maxWidth: 800, margin: '0 auto', padding: 20 }}>
      <h1>Indian Village Location Lookup</h1>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 15, marginBottom: 20 }}>
        <select onChange={e => setSelected(s => ({...s, country: e.target.value, state: '', district: '', subDistrict: ''}))} value={selected.country}>
          <option value="">Select Country</option>
          {countries.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
        <select disabled={!states.length} onChange={e => setSelected(s => ({...s, state: e.target.value, district: '', subDistrict: ''}))} value={selected.state}>
          <option value="">Select State</option>
          {states.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
        </select>
        <select disabled={!districts.length} onChange={e => setSelected(s => ({...s, district: e.target.value, subDistrict: ''}))} value={selected.district}>
          <option value="">Select District</option>
          {districts.map(d => <option key={d.id} value={d.id}>{d.name}</option>)}
        </select>
        <select disabled={!subDistricts.length} onChange={e => setSelected(s => ({...s, subDistrict: e.target.value}))} value={selected.subDistrict}>
          <option value="">Select Sub-District</option>
          {subDistricts.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
        </select>
      </div>
      <input placeholder="Search villages..." value={search} onChange={e => setSearch(e.target.value)} style={{ padding: 8, width: '100%', marginBottom: 20 }} />
      <h3>Villages ({villages.length})</h3>
      <ul style={{ maxHeight: 400, overflow: 'auto' }}>
        {villages.map(v => <li key={v.id}>{v.name} {v.village_code && `(${v.village_code})`}</li>)}
      </ul>
    </div>
  )
}

export default App
