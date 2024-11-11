# Mutant DNA API

This project provides a REST API that determines whether a given DNA sequence belongs to a mutant or not. It also allows saving DNA sequences to a database and calculating statistics about mutants and humans. This service is built using **FastAPI**, **SQLAlchemy**, and **PostgreSQL** for the database.

## Features

- Check if a DNA sequence is from a mutant or not.
- Store DNA sequences in a PostgreSQL database.
- Expose statistics about mutants and humans, including the ratio of mutants to humans.
- Expose endpoints to handle requests for DNA analysis and statistics.
  
## Requirements

- Python 3.7 or higher.
- Docker (optional, for containerized deployment).
- PostgreSQL (if not using Docker for DB).

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/mutant_dna_api.git
    cd mutant_dna_api
    ```

2. **Create a virtual environment** (recommended):
    ```bash
    python3 -m venv venv
    ```

3. **Activate the virtual environment**:
    - On **Windows**:
        ```bash
        .\venv\Scripts\activate
        ```
    - On **macOS/Linux**:
        ```bash
        source venv/bin/activate
        ```

4. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the application locally**:
    ```bash
    uvicorn app.main:app --reload
    ```

    Your API will be available at `http://127.0.0.1:8000`.

## Docker Setup

To deploy the API using Docker, follow the steps below:

1. **Build the Docker image**:
    ```bash
    docker build -t mutant-analyzer-api .
    ```

2. **Run the Docker container**:
    ```bash
    docker run -it -v $(pwd)/mutant_dna_api:/var/app -p 3002:8000 mutant-analyzer-api
    ```

    This will run the API on port `3002`. You can access it at `http://localhost:3002`.

### Docker Compose (Optional)

If you wish to use Docker Compose to simplify the deployment of both the application and PostgreSQL, follow these steps:

1. **Create a `docker-compose.yml` file** (if not already provided):
    ```yaml
    version: "3.7"

    services:
      app:
        build: .
        volumes:
          - .:/app
        ports:
          - "8000:8000"
        environment:
          - DATABASE_URL=postgresql://mutantanalizer:mutantanalizerpassword@db:5432/mutantanalizerdb
        depends_on:
          - db

      db:
        image: postgres:latest
        environment:
          POSTGRES_USER: mutantanalizer
          POSTGRES_PASSWORD: mutantanalizerpassword
          POSTGRES_DB: mutantanalizerdb
        ports:
          - "5432:5432"
    ```

2. **Start both the application and database**:
    ```bash
    docker-compose up
    ```

    This will set up and run both the application and the PostgreSQL database in Docker containers.

## Endpoints

### 1. `/mutant` - Check if a DNA sequence is mutant

- **Method**: `POST`
- **Request body**:
    ```json
    {
      "dna": ["ATGCGA", "CAGTGC", "TTATTT", "AGAAGG", "CCCCTA", "TCACTG"]
    }
    ```

- **Response**:
    - **200 OK**: If the DNA is from a mutant:
        ```json
        { "message": "DNA is mutant" }
        ```
    - **403 Forbidden**: If the DNA is from a human:
        ```json
        { "detail": "DNA is not mutant" }
        ```

### 2. `/stats` - Get the statistics of mutant vs human DNA sequences

- **Method**: `GET`
- **Response**:
    ```json
    {
      "count_mutant_dna": 10,
      "count_human_dna": 100,
      "ratio": 0.1
    }
    ```

    - `count_mutant_dna`: The total number of mutant DNA sequences stored in the database.
    - `count_human_dna`: The total number of human DNA sequences stored in the database.
    - `ratio`: The ratio of mutant to human DNA sequences (mutants/humans).

### 3. `/health` - Health Check Endpoint

- **Method**: `GET`
- **Description**: This endpoint is used to check the health status of the application.
- **Response**:
    - **200 OK**: If the application is running correctly:
        ```json
        {
          "status": "ok"
        }
        ```

    This endpoint is useful for monitoring purposes, allowing you to check if the application and its services are up and running.



## Database Schema

The application uses PostgreSQL for storing DNA sequences. The `dna_records` table is created with the following schema:

- `sequence` (VARCHAR, primary key): The DNA sequence.
- `is_mutant` (BOOLEAN): Whether the DNA sequence belongs to a mutant (`True`) or a human (`False`).

## Environment Variables

The application requires the following environment variable to connect to the database:

- `DATABASE_URL`: The PostgreSQL database URL. If using Docker, this should be set to:
    ```bash
    postgresql://mutantanalizer:mutantanalizerpassword@db:5432/mutantanalizerdb
    ```

    Replace with your actual PostgreSQL connection string if not using Docker.

## Running Tests

To run tests for the API, use `pytest` (or any testing framework you prefer):

1. **Install testing dependencies**:
    ```bash
    pip install -r requirements-dev.txt
    ```

2. **Run the tests**:
    ```bash
    pytest
    ```

## Troubleshooting

- **Error: `ModuleNotFoundError: No module named 'pydantic_settings'`**
    - If you are using **Pydantic v2**, make sure you have the `pydantic-settings` module installed:
    ```bash
    pip install pydantic-settings
    ```

- **Error: Database connection issues**
    - Make sure PostgreSQL is running (either locally or via Docker).
    - Ensure that the `DATABASE_URL` environment variable is correctly set.

## License

MIT License. See `LICENSE` for more information.
