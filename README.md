# Gamuda Flutter App (Assignment) Backend

This repository contains the backend API service for [Gamuda Flutter App](https://gamuda-flutter-homework-01.web.app/), providing endpoint connections to a PostgreSQL database. The frontend source code can be found at [HJWongAtWork/gamuda_flutter_app](https://github.com/HJWongAtWork/gamuda_flutter_app).

NOTE: THIS IS NOT AN OFFICIAL GAMUDA PROJECT. THIS IS PART OF A PERSONAL ASSIGNMENT.

## Prerequisites

Install PostgreSQL if you haven't already, and create a PostgreSQL database:

```bash
createdb your_database_name
```

## Setup Instructions

### Environment Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # For Unix/macOS
```
or
```bash
python3 -m venv venv
.\venv\Scripts\activate  # For Windows
```

### Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a .env file in the root directory using .env.example as template:

```bash
# .env example
# Database Configuration
DB_USERNAME=your_db_username
DB_PASSWORD=your_db_password
DB_HOSTPORT=localhost:5432
DB_DBNAME=your_db_name

# Security
SECRET_KEY=your_secret_key

# OAuth Configuration (to be provided from the relevant Google Project)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

## Running the Application

Start the server from the root directory:

```bash
python3 main.py
```
or
```bash
python3 -m uvicorn main:app --reload
```

The API will be available at http://localhost:8000.
