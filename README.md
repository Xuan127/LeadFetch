# LeadFetch - Influencer Marketing Platform

LeadFetch is a web application that helps marketing teams find and connect with social media influencers. The platform consists of a React frontend and a Flask backend with a PostgreSQL database.

## Project Structure

- `frontend/`: React frontend built with TypeScript and Vite
- `backend/`: Flask API for data processing and storage
- `influencerOutreach/`: Python modules for influencer discovery and outreach

## Setup Instructions

### Prerequisites

- Node.js (v16+) and npm
- Python (v3.8+) and pip
- PostgreSQL database

### Backend Setup

1. Create a virtual environment and install dependencies:

```bash
cd LeadFetch
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
```

2. Configure your environment variables in `backend/.env`:

```
DATABASE_URL=postgresql://username:password@hostname:5432/database_name
APIFY_API_KEY=your_apify_api_key
```

3. Start the Flask server:

```bash
cd backend
flask run
```

The API will be accessible at http://localhost:5000

### Frontend Setup

1. Install dependencies:

```bash
cd frontend
npm install
```

2. Start the development server:

```bash
npm run dev
```

The frontend will be accessible at http://localhost:5173

## Features

- **Client Brief Creation**: Create and upload marketing campaign briefs
- **Influencer Discovery**: Find influencers based on platform, followers, and engagement
- **Influencer Outreach**: Contact influencers directly through the platform
- **Performance Tracking**: Monitor campaign performance metrics

## API Endpoints

### Health Check
- `GET /api/health`: Check if the API is running

### Influencers
- `GET /api/influencers`: Get all influencers
- `POST /api/influencers/search`: Search for influencers by query

### Client Briefs
- `POST /api/briefs`: Create a new client brief

### Contact
- `POST /api/contact`: Send a contact request to an influencer

## Development Notes

- Frontend state is managed via React hooks
- Backend uses Flask with a PostgreSQL database
- TikTok scraping is performed via the Apify API

## Deployment

For production deployment:

1. Build the frontend:
```bash
cd frontend
npm run build
```

2. Set the Flask environment to production in `.env`:
```
FLASK_ENV=production
```

3. Use a WSGI server like Gunicorn to serve the Flask application.
