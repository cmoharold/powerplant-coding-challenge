# Powerplant Coding Challenge Solution

## Overview
This application calculates how much power each powerplant needs to produce to match a given load while minimizing costs.

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/cmoharold/powerplant-coding-challenge.git
    cd powerplant-coding-challenge
    ```

2. Create and activate a virtual environment:
    ```
    python -m venv env
    source env/Scripts/activate
    ```

3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

## Usage

1. Start the FastAPI server:
    ```
    uvicorn main:app --host 0.0.0.0 --port 8888
    ```

2. Access the API documentation at `http://localhost:8888/docs`.

3. Test the `/productionplan` endpoint by sending a POST request with a JSON payload. Example payloads are provided in the challenge description.

## Deploying with Docker

1. Build the Docker image:
    ```
    docker build -t powerplant-api .
    ```

2. Run the Docker container:
    ```
    docker run -p 8888:8888 powerplant-api
    ```

3. Access the API documentation at `http://localhost:8888/docs`.

## Example

Request:
```json
{
  "load": 910,
  "fuels":
  {
    "gas(euro/MWh)": 13.4,
    "kerosine(euro/MWh)": 50.8,
    "co2(euro/ton)": 20,
    "wind(%)": 60
  },
  "powerplants": [
    {
      "name": "gasfiredbig1",
      "type": "gasfired",
      "efficiency": 0.53,
      "pmin": 100,
      "pmax": 460
    },
    {
      "name": "gasfiredbig2",
      "type": "gasfired",
      "efficiency": 0.53,
      "pmin": 100,
      "pmax": 460
    },
    {
      "name": "gasfiredsomewhatsmaller",
      "type": "gasfired",
      "efficiency": 0.37,
      "pmin": 40,
      "pmax": 210
    },
    {
      "name": "tj1",
      "type": "turbojet",
      "efficiency": 0.3,
      "pmin": 0,
      "pmax": 16
    },
    {
      "name": "windpark1",
      "type": "windturbine",
      "efficiency": 1,
      "pmin": 0,
      "pmax": 150
    },
    {
      "name": "windpark2",
      "type": "windturbine",
      "efficiency": 1,
      "pmin": 0,
      "pmax": 36
    }
  ]
}
```

Response:
```json
[
  {
    "name": "windpark1",
    "p": 90
  },
  {
    "name": "windpark2",
    "p": 21.6
  },
  {
    "name": "gasfiredbig1",
    "p": 460
  },
  {
    "name": "gasfiredbig2",
    "p": 338.4
  },
  {
    "name": "gasfiredsomewhatsmaller",
    "p": 0
  },
  {
    "name": "tj1",
    "p": 0
  }
]
```

## Notes
- This solution doesn't use external linear programming solvers.
- Assumes inputs are well-formed; minimal input validation is implemented.

