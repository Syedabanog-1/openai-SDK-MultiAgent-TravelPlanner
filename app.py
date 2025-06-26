from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel
import requests
from dotenv import find_dotenv, get_key

# ✅ Load Gemini API key
GEMINI_API_KEY = get_key(find_dotenv(), "GOOGLE_API_KEY")

# ✅ Tool 1: Weather function
@function_tool
def getWeather(city: str) -> str:
    """
    Get the weather for a given city.
    """
    try:
        response = requests.get(
            f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}"
        )
        if response.status_code == 200:
            data = response.json()
            return f"The weather in {city.title()} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."
        else:
            return "❌ Sorry, I couldn't fetch the weather data."
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

# ✅ Tool 2: Flight finder (Karachi flights customized)
@function_tool
def find_flights(destination: str, date: str):
    """
    Find flights from Karachi to a specified destination.
    """
    destination = destination.lower()
    possible_destinations = ["lahore", "islamabad", "multan", "peshawar", "quetta", "sialkot", "skardu", "gilgit"]

    if destination in possible_destinations:
        return [
            {
                "airline": "PIA",
                "price": 30000,
                "departure": "Karachi",
                "arrival": destination.title(),
                "date": date
            },
            {
                "airline": "Air Blue",
                "price": 27000,
                "departure": "Karachi",
                "arrival": destination.title(),
                "date": date
            },
            {
                "airline": "Air Sial",
                "price": 28000,
                "departure": "Karachi",
                "arrival": destination.title(),
                "date": date
            }
        ]
    else:
        return f"❌ Sorry, no flights found from Karachi to {destination.title()}. Please try a valid destination."

# ✅ Agent setup
agent: Agent = Agent(
    name="hello",
    instructions="You are a helpful travel assistant. You can provide weather updates and find flights from Karachi to major Pakistani cities.",
    model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=GEMINI_API_KEY),
    tools=[getWeather, find_flights],
)

# ✅ Runner function
def run(message: str) -> str:
    print("Run message:", message)
    result = Runner.run_sync(agent, f"{message}?")
    return result.final_output
