# Bluestock 22A22J - Indian Village Location API Platform

A production-grade API platform serving hierarchical location data for every Indian village. Built as a B2B-ready SaaS solution for address forms, KYC, logistics, and more.

## Tech Stack

- **Backend**: FastAPI, Python 3.11+
- **Database**: PostgreSQL 15+
- **Cache**: Redis
- **Frontend**: React (Vite), Recharts
- **Testing**: PyTest, Jest
- **CI/CD**: GitHub Actions
- **Deployment**: Docker, AWS/Heroku

## Architecture

```
Country → State → District → Sub-District → Village
```

## Project Structure

```
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/       # API endpoints
│   │   ├── models/    # DB models
│   │   ├── services/  # Business logic
│   │   ├── core/      # Config, security
│   │   └── db/        # Database setup
│   ├── scripts/       # Data import scripts
│   └── tests/
├── frontend/
│   ├── admin/         # Admin dashboard
│   └── demo-client/   # Demo client
├── data/              # Dataset files
└── docs/              # Documentation
```

## Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend/admin && npm install && npm run dev
cd frontend/demo-client && npm install && npm run dev
```

## API Endpoints

- `GET /countries` - List all countries
- `GET /states?country_id=` - List states
- `GET /districts?state_id=` - List districts
- `GET /sub-districts?district_id=` - List sub-districts
- `GET /villages?state_id=&district_id=&sub_district_id=` - List villages

## Success Metrics

- API Latency: ≤ 200ms (cached)
- Uptime: 99.9%
- Data Accuracy: < 0.5% errors
- Real-time dashboard analytics
