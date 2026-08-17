# MoinSystems AI Public Website Chatbot

Backend API for the MoinSystems AI public website chatbot.

## Tech Stack

- Python 3.14.4
- FastAPI## Project Structure

```text
moin-ai-chatbot/
├── app/
├── alembic/
├── tests/
├── .env
├── .env.example
├── requirements.txt
└── README.md
## Installation

Create the virtual environment:

```powershell
python -m venv .venv
## Run the API

Start the development server:

```powershell
uvicorn app.main:app --reload
## Health Check

Open:

http://127.0.0.1:8000/api/v1/health

Expected response:

```json
{
  "status": "ok",
  "database": "ready"
}
## Database Migrations

Generate a migration:

```powershell
alembic revision --autogenerate -m "migration message"
## Testing

Run all tests:

```powershell
pytest