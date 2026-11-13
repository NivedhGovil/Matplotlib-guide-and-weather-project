import pandas as pd
import requests
import matplotlib.pyplot as plt

# 1. Ask the user which city they want
city = input("Enter a city name: ")

# 2. Turn that city name into latitude/longitude using Open-Meteo's geocoding API
geo_url = f"https://open-meteo.com{city}&count=1"
geo_response = requests.get(geo_url).json()  # Saves the data obtained from geo_url

if "results" not in geo_response:
    print(f"Couldn't find a city called '{city}'. Try a different spelling.")
else:
    place = geo_response["results"][0]     # Open "results" and grab the first item
    latitude = place["latitude"]           # Pull out latitude from place
    longitude = place["longitude"]
    found_name = place["name"]
    country = place["country"]

    print(f"Found: {found_name}, {country} ({latitude}, {longitude})")

    # 3. Fetch the weather using the coordinates we just found
    weather_url = (
        f"https://open-meteo.com?"
        f"latitude={latitude}&longitude={longitude}"
        f"&hourly=temperature_2m&past_days=7&timezone=auto"
    )
    response = requests.get(weather_url).json()  # Fetches the weather data as JSON

    # Grab the list of hours and the list of temperatures
    hours = response['hourly']['time']
    temps = response['hourly']['temperature_2m']

    # 4. Open (or create) Temperature.csv and write the data into it
    with open('Temperature.csv', 'w') as file:
        file.write("Time,Temperature\n")  # Write the column headers at the top

        for i in range(168):  # i goes 0, 1, 2 ... all the way to 167 (24 hours x 7 days)
            file.write(f"{hours[i]},{temps[i]}\n")  # Writes one row per hour

    print("Saved 7 days of live weather data into Temperature.csv!")

    # 5. Analyze and chart the CSV we just saved
    data = pd.read_csv("Temperature.csv")
    data["Date"] = pd.to_datetime(data["Time"]).dt.strftime("%d-%b-%Y")

    daily = data.groupby("Date", sort=False)["Temperature"].agg(["min", "mean", "median", "max"])
    daily["mean"] = daily["mean"].round(2)
    daily["median"] = daily["median"].round(2)
    daily.insert(0, "City", found_name)

    print(daily)
    daily.to_csv("Daily_Summary.csv")

    daily.plot(marker="o", figsize=(10, 5), title=f"Daily Temperature Summary of {city}")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("weekly_temperature.png")
    plt.show()
