from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict

# Create a FastAPI app instance
app = FastAPI()

# Define a model for fuel inputs
class Fuel(BaseModel):
    gas: float = Field(..., alias="gas(euro/MWh)")
    kerosine: float = Field(..., alias="kerosine(euro/MWh)")
    co2: float = Field(..., alias="co2(euro/ton)")
    wind: float = Field(..., alias="wind(%)")

    class Config:
        allow_population_by_field_name = True

# Define a model for power plant details
class PowerPlant(BaseModel):
    name: str
    type: str
    efficiency: float
    pmin: float
    pmax: float
    cost: float = 0.0  # Initialize cost with a default value
    max_power: float = 0.0  # Initialize max_power with a default value

# Define a model for the input payload
class ProductionPlanInput(BaseModel):
    load: float
    fuels: Fuel
    powerplants: List[PowerPlant]

# Define a model for the output payload
class ProductionPlanOutput(BaseModel):
    name: str
    p: float

# Define the endpoint to calculate the production plan
@app.post("/productionplan", response_model=List[ProductionPlanOutput])
def calculate_production_plan(input_data: ProductionPlanInput):
    load = input_data.load
    fuels = input_data.fuels.dict()
    powerplants = input_data.powerplants

    # Calculate cost per MWh for each powerplant
    for plant in powerplants:
        if plant.type == "windturbine":  # Wind turbines have zero cost
            plant.cost = 0
            plant.max_power = plant.pmax * (fuels['wind'] / 100)  # Scale max power by wind efficiency
        else:
            fuel_cost = fuels["gas"] if plant.type == "gasfired" else fuels["kerosine"]  # Select fuel cost based on type
            plant.cost = fuel_cost / plant.efficiency  # Calculate cost per MWh based on efficiency
            plant.max_power = plant.pmax  # Maximum power is pmax for other plants

    # Sort powerplants by cost (merit order)
    powerplants.sort(key=lambda x: x.cost)

    # Allocate load based on merit order
    production_plan = []
    remaining_load = load

    for plant in powerplants:
        if remaining_load <= 0:  # If the load is already met, set power to 0
            production_plan.append({"name": plant.name, "p": 0})
            continue

        available_power = min(plant.max_power, remaining_load)  # Determine the available power for the plant
        if available_power < plant.pmin:  # If the available power is less than the minimum, skip the plant
            production_plan.append({"name": plant.name, "p": 0})
            continue

        power = max(plant.pmin, available_power)  # Allocate power, respecting pmin and available power
        production_plan.append({"name": plant.name, "p": round(power, 1)})  # Add the plant's output to the plan
        remaining_load -= power  # Subtract the allocated power from the remaining load

    # Verify if we met the load exactly
    total_power = sum([p["p"] for p in production_plan])
    if abs(total_power - load) > 0.1:  # Allow small floating-point tolerance
        raise HTTPException(status_code=400, detail="Unable to match the exact load with given powerplants.")

    return production_plan
