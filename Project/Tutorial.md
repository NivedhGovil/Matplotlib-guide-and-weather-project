# Tutorial

## 1. Import Requirements

We need 3 libraries:
* Pandas
* Requests
* Matplotlib

**Code:**
```python
import pandas as pd
import requests
import matplotlib.pyplot as plt
```

---

## 2. City Name and Open-Meteo Fetching

The code starts by asking the user which city they live in.

```python
city = input("Enter a city name: ")
```

Next, we need to create a URL for Open-Meteo's geocoding API, inserting the city name so the API can look up its geographic coordinates. We do this with an f-string, which replaces the variable inside the curly braces with the city entered by the user.

```python
geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
```

To send a request to the geocoding API and convert the resulting JSON weather data into a Python dictionary, add this line:

```python
geo_response = requests.get(geo_url).json()
```

**Your code so far:**
```python
import pandas as pd
import requests
import matplotlib.pyplot as plt

city = input("Enter a city name: ")
geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
geo_response = requests.get(geo_url).json()  # Saves the data obtained from geo_url
```

---

## 3. Handling Edge Cases

If the city entered is misspelled, doesn't exist, or fails to fetch data from the API, the program will crash if there are no results in `geo_response`. 

We can add an `if` statement to check if `"results"` was successfully fetched from the API:

```python
if "results" not in geo_response:
    print(f"Couldn't find a city called '{city}'. Try a different spelling.")
```

Now, we need to handle what happens when a valid city *is* found. We add an `else` block to extract the geographic location details:

```python
else:
    place = geo_response["results"][0]  # Open "results" and grab the first item (Index 0)
    latitude = place["latitude"]        # Pull out latitude from place
    longitude = place["longitude"]
    found_name = place["name"]
    country = place["country"]
    print(f"Found: {found_name}, {country} ({latitude}, {longitude})")  # Prints the values obtained above
```

**Your total code so far:**
```python
import pandas as pd
import requests
import matplotlib.pyplot as plt

city = input("Enter a city name: ")
geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
geo_response = requests.get(geo_url).json()  # Saves the data obtained from geo_url

if "results" not in geo_response:
    print(f"Couldn't find a city called '{city}'. Try a different spelling.")
else:
    place = geo_response["results"][0]
    latitude = place["latitude"]
    longitude = place["longitude"]
    found_name = place["name"]
    country = place["country"]
    print(f"Found: {found_name}, {country} ({latitude}, {longitude})")
```

---

## 4. Fetching Weather Data

Next, we build the API request URL for Open-Meteo's forecast service using the retrieved coordinates. It asks for hourly temperatures (`hourly=temperature_2m`) covering the past 7 days (`past_days=7`) with local timezone adjustments, then fetches and parses the JSON response.

```python
weather_url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={latitude}&longitude={longitude}"
    f"&hourly=temperature_2m&past_days=7&timezone=auto"
)
response = requests.get(weather_url).json()  # Fetches the weather data as JSON
```

---

## 5. Extracting Hours and Temperatures

Finally, we grab the list of hours and the list of temperatures from the JSON response:

```python
hours = response['hourly']['time']             # Open response -> hourly -> time -> store as hours
temps = response['hourly']['temperature_2m']   # Same, but for temperature at 2 meters above ground
```
