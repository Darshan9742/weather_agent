import os
import requests
from dotenv import load_dotenv
from langchain.tools import tool
from pydantic import BaseModel, Field

load_dotenv()

# --- Weather API Tool ---
@tool
def get_current_weather(location: str) -> dict:
    """Fetches current weather for a given location using WeatherAPI.com."""
    import requests
    api_key = os.getenv("WEATHERAPI_KEY")
    url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": api_key,
        "q": location,
        "aqi": "no"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return {
            "city": data["location"]["name"],
            "temperature": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "description": data["current"]["condition"]["text"],
            "humidity": data["current"]["humidity"]
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"WeatherAPI request failed: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}


# --- Appliance Pydantic Model ---
class Appliance(BaseModel):
    name: str = Field(..., description="The name of the appliance (e.g., 'Refrigerator', 'LED TV').")
    wattage: float = Field(..., description="The power consumption of the appliance in watts.")
    hours: float = Field(..., description="The daily usage of the appliance in hours.")

# --- Energy Calculation Function ---
def _calculate_energy_consumption_func(appliances: list) -> dict:
    """Calculates total energy consumption and identifies high-use appliances from a list of appliance data."""
    total_kwh = 0
    appliance_kwh = []
    for app in appliances:
        try:
            name = app.get("name")
            wattage = float(app.get("wattage"))
            hours = float(app.get("hours"))
            daily_kwh = (wattage * hours) / 1000
            total_kwh += daily_kwh
            appliance_kwh.append({"name": name, "kwh": daily_kwh})
        except (ValueError, TypeError):
            continue

    appliance_kwh.sort(key=lambda x: x['kwh'], reverse=True)
    high_consumers = [app['name'] for app in appliance_kwh[:2]]

    return {
        "total_kwh_per_day": round(total_kwh, 2),
        "high_consumers": high_consumers,
        "appliance_data": appliance_kwh
    }

# --- Energy Calculation Tool ---
@tool("calculate_energy_consumption")
def calculate_energy_consumption_tool(appliances: list[Appliance]) -> dict:
    """Calculates total energy consumption and identifies high-use appliances from a list of appliance data."""
    appliance_dicts = [app.dict() for app in appliances]
    return _calculate_energy_consumption_func(appliance_dicts)