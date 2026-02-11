# Invoice Parser Application

A full-stack application for parsing invoice text using Regex, featuring a FastAPI backend and a React (Vite) TypeScript frontend.

## Features

- **Regex-First Parsing**: Efficient extraction of product names, quantities, units, and prices.
- **Interactive UI**: Paste invoice text, view extracted items in a table, and edit results manually.
- **API Security**: Includes rate limiting (5 requests per minute) and payload size restrictions (100KB).
- **Idempotency**: Support for `request-id` headers to prevent duplicate processing.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/regex-assessment.git
cd regex-assessment
```

### 2. Start the Backend

The backend uses FastAPI. It is recommended to run it from the `backend` directory.

```bash
cd backend
# Install dependencies (if not already installed)
pip install -r requirements.txt

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`.

### 3. Start the Frontend

The frontend is built with React, Vite, and TypeScript.

```bash
cd frontend
# Install dependencies
npm install

# Start the development server
npm run dev
```

The UI will be available at `http://localhost:5173`.

---

## Testing

### Backend Tests

The backend includes a comprehensive test suite using `pytest` covering regex patterns, rate limiting, and API logic.

To run the tests:

```bash
cd backend
PYTHONPATH=. pytest
```

---

## API Constraints

### Rate Limiting

To ensure fair usage and protect the server, the `/parse` endpoint is rate-limited:

- **Limit**: 5 requests per minute per IP address.
- **Exceeding Limit**: Returns a `429 Too Many Requests` response.

### Payload Size

- **Limit**: Maximum request size is **100KB**.
- **Exceeding Limit**: Returns a `413 Payload Too Large` response.
