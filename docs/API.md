# API Documentation

Base URL: `http://localhost:8000/api/v1`

All endpoints require `X-API-Key` header.

## Endpoints

### GET /countries
List all countries
**Response:** `[{ "id": 1, "name": "India", "code": "IN" }]`

### GET /states?country_id=
List states for a country
**Response:** `[{ "id": 1, "name": "Karnataka", "code": "KA" }]`

### GET /districts?state_id=
List districts for a state
**Response:** `[{ "id": 1, "name": "Bangalore Urban" }]`

### GET /sub-districts?district_id=
List sub-districts for a district
**Response:** `[{ "id": 1, "name": "Bangalore North" }]`

### GET /villages
Query villages with optional filters:
- `state_id` (int)
- `district_id` (int)
- `sub_district_id` (int)
- `search` (string)
- `page` (int, default 1)
- `limit` (int, default 50, max 200)

**Response:**
```json
{
  "total": 100,
  "page": 1,
  "limit": 50,
  "data": [{ "id": 1, "name": "Village Name", "village_code": "123" }]
}
```

### GET /villages/{village_id}
Get single village details

## Admin Endpoints (require admin API key)

### POST /api/admin/keys?name=
Create new API key

### GET /api/admin/keys
List all API keys

### PUT /api/admin/keys/{key_id}/toggle
Enable/disable an API key

### GET /api/admin/analytics
Get usage analytics

### GET /api/admin/logs?limit=100
Get request logs
