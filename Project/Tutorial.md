# Tutorial

**1. Import requirements**
    We need 3 libraires: 
    - Pandas
    - Requests
    - Matplotlib

 Code: 
 ```
 import pandas as pd
 import requests
 import matplotlib.pyplot as plt
 ```

**2. City name and Open Meteo fetching**

The code starts by asking the user, which city do they live in.
Add: 
 ```
 city = input("Enter a city name: ")
 ```

Now, we access the url of the city, inputted by the user. 
```
city = input("Enter a city name: ")
```

Now, we need to make a URL for Open-Meteo's geocoding API, inserting the city name so the API can look up its geographic coordinates. We do this with an f-string, a sort of function that replace the city entered into the URL. 
```
geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
```
```
To get a request to the geocoding API and convert the resulting JSON data (weather data will be stored in JSON) into a Python dictionary, we need to add this: 
geo_response = requests.get(geo_url).json()  
```

So now, our code is: 
```
import pandas as pd
import requests
import matplotlib.pyplot as plt

city = input("Enter a city name: ")

geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
geo_response = requests.get(geo_url).json()  # saves the data obtained from geo_url
```

3. Creating the Edge case
   If the city entered is not correct(typo or it doesn't exist) or if the cty entered could not fetch any data from the API, the program will crash if there is no value for ```geo_response```. So, we add an if statement that will check if the "result" was correctly fetched from the API.
   We add: <br>
   ```
   if "results" not in geo_response:  
    print(f"Couldn't find a city called '{city}'. Try a different spelling.")
   ```

   But, what if it entered a correct value? Our program will still crash as there is nothing to do if a corret value is reached!
   so, we now add:
   ```
   else:
        place = geo_response["results"][0]     # Open the box "Results" and grab the first item(Index 0)
        latitude = place["latitude"]           # Pull out latitude from place
        longitude = place["longitude"]    
        found_name = place["name"]
        country = place["country"]
        print(f" Found: {found_name}, {country} ({latitude}, {longitude})")  # Prints the values obtained above.
   ```
   This makes us get the geographical location of the place

   Our total code is now:
   ```
import requests 
import requests
import matplotlib.pyplot as plt

city = input("Enter a city name: ")


geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
geo_response = requests.get(geo_url).json()  # saves the data obtained from geo_url
```


if "results" not in geo_response: 
    print(f"Couldn't find a city called '{city}'. Try a different spelling.")
else:
    place = geo_response["results"][0]     
    latitude = place["latitude"]         
    longitude = place["longitude"]
    found_name = place["name"]
    country = place["country"]

    print(f" Found: {found_name}, {country} ({latitude}, {longitude})")
   ```

4.
```
weather_url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={latitude}&longitude={longitude}"
    f"&hourly=temperature_2m&past_days=7&timezone=auto"
)
response = requests.get(weather_url).json()  # Fetches the weather data as JSON.
```
 Builds the API request URL for Open-Meteo's forecast service using the retrieved coordinates. It asks for hourly temperatures (hourly=temperature_2m) covering the past 7 days (past_days=7) with local timezone adjustments, then fetches and parses the JSON response.
5. Grab the list of hours and the list of temperatures

hours = response['hourly']['time']  # Open response, then hourly, then time -> store as hours.
temps = response['hourly']['temperature_2m']  # Same, but for temperature at 2 metres above ground.
