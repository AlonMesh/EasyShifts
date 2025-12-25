# Docker Instructions for EasyShifts

This directory contains the configuration files for containerizing the EasyShifts application. The setup includes three services:
1. **Frontend**: React application served via Nginx.
2. **Backend**: Python/Flask API.
3. **Database**: MySQL 8.0.

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine.
- [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop).

## Running the Application

1. **Navigate to the project root directory** (where `docker-compose.yaml` is located):
   ```bash
   cd /path/to/EasyShifts
   ```

2. **Build and start the containers**:
   ```bash
   docker-compose up --build
   ```
   *The `--build` flag ensures that the images are rebuilt if you've made changes to the code.*

3. **Access the application**:
   - **Frontend**: [http://localhost:3001](http://localhost:3001)
   - **Backend API**: [http://localhost:8080](http://localhost:8080)
   - **Database**: `localhost:3306` (User: `root`, Password: `root`, DB: `easyshifsdb`)

## Stopping the Application

To stop the containers and remove the created networks:

```bash
docker-compose down
```

To stop the containers and also remove the database volume (resetting data):

```bash
docker-compose down -v
```

## Directory Structure

- `backend/`: Dockerfile for the Python backend.
- `frontend/`: Dockerfile and Nginx configuration for the React frontend.
