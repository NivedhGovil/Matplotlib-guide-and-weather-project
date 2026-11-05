# Tutorial

1. Import requirements
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

2. City name and Open Meteo fetching

The code starts by asking the user, which city do they live in.
Add: 
 ```
 city = input("Enter a city name: ")
 ```

Now, we acces the url of the city. 
```

city = input("Enter a city name: ")

API
geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
geo_response = requests.get(geo_url).json()  
```