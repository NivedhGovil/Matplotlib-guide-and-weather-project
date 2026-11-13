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



## 6. Saving the Data to a CSV File

Now that we have the lists of hours and temperatures, we need to save them into a spreadsheet-style format called a **CSV (Comma-Separated Values)** file. 

To do this safely, we use Python's `with open()` statement:
* **`'Temperature.csv'`**: The name of the file Python will create (or overwrite if it already exists).
* **`'w'` (Write Mode)**: Tells Python we are writing new data into the file.
* **`with ... as file`**: Automatically closes and saves the file once the code inside the block finishes running, preventing data loss.

Inside the file, we first write the column headers (`Time,Temperature`) followed by `\n`, which acts like hitting the **Enter** key to move to a new line. 

Next, we use a `for` loop with `range(168)` because 7 days × 24 hours equals **168 total hours**. On each pass of the loop, the variable `i` grabs the matching hour and temperature from our lists and writes them as a new comma-separated row:

```python
    # Open (or create) Temperature.csv and write the data into it
    with open('Temperature.csv', 'w') as file:
        file.write("Time,Temperature\n")  # Write the column headers at the top

        for i in range(168):  # i goes 0, 1, 2 ... all the way to 167 (24 hours x 7 days)
            file.write(f"{hours[i]},{temps[i]}\n")  # Writes one row per hour

    print("Saved 7 days of live weather data into Temperature.csv!")
```

---

## 7. Analyzing the Data with Pandas

Next, we load the CSV file we just saved into a Pandas DataFrame (a table-shaped structure). We convert the timestamps into a cleaner date format (`Day-Month-Year`) and store it in a new `"Date"` column:

```python
    data = pd.read_csv("Temperature.csv")  # Reads the file and loads it into a table-shaped box
    data["Date"] = pd.to_datetime(data["Time"]).dt.strftime("%d-%b-%Y")  # New column: nicely formatted date
```

Now, we group all the hourly rows that share the same date together and calculate the minimum, mean, median, and maximum temperatures for each day. We also round the decimals, add the city name to the first column, print the table, and save it as a new CSV file:

```python
    daily = data.groupby("Date", sort=False)["Temperature"].agg(["min", "mean", "median", "max"])
    # Take all rows with the same Date, keep their original order (sort=False), and calculate stats

    daily["mean"] = daily["mean"].round(2)      # Rounds the mean to 2 decimal places
    daily["median"] = daily["median"].round(2)  # Rounds the median to 2 decimal places
    daily.insert(0, "City", found_name)         # Inserts a column at index 0 labeled "City"

    print(daily)  # Prints the summary table
    daily.to_csv("Daily_Summary.csv")  # Saves the summary table to a new CSV
```

---

## 8. Plotting the Chart with Matplotlib

Finally, we visualize our daily temperature summary using Matplotlib. We plot the data with circular markers, add labels and a grid, prevent the borders from cutting off text using `tight_layout()`, save the image as a PNG file, and display it on screen:

```python
    daily.plot(marker="o", figsize=(10, 5), title=f"Daily Temperature Summary of {city}")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()  # Ensures labels don't get cut off by graph borders
    plt.savefig("weekly_temperature.png")  # Saves the chart as a PNG
    plt.show()
```

---

## Complete Code

Here is the entire working script from start to finish:

```python
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
```
