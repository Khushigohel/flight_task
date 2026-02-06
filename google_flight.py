import requests
import csv
import time
from datetime import datetime, timedelta

API_KEY = "52936d7967fabb0ccbcf34e9403c341eb97b5224b82ddc0d16611216f4c589fc"
url = "https://serpapi.com/search"

source = "AMD"
destinations = ["DEL"] 

# Date range
start_date = datetime.strptime("2026-02-10", "%Y-%m-%d")
end_date = datetime.strptime("2026-02-17", "%Y-%m-%d")

def fetch_multi_day_flights():
    all_rows = []

    current_date = start_date
    while current_date <= end_date:
        outbound_date = current_date.strftime("%Y-%m-%d")
        for dest in destinations:
            print(f"Requesting flights from {source} to {dest} on {outbound_date}...")
            
            params = {
                "engine": "google_flights",
                "departure_id": source,
                "arrival_id": dest,
                "outbound_date": outbound_date,
                "currency": "INR",
                "gl": "in",
                "api_key": API_KEY,
                "type": "2"
            }

            response = requests.get(url, params=params)
            data = response.json()
            

            if "error" in data:
                print(f" Error for {dest} on {outbound_date}: {data['error']}")
                continue

            flights = data.get("best_flights", []) + data.get("other_flights", [])
            for f in flights:
                leg = f.get('flights', [{}])[0]
                all_rows.append({
                    "Date": outbound_date,
                    "Source": leg.get('departure_airport', {}).get('id'),      
                    "Destination": leg.get('arrival_airport', {}).get('id'),   
                    "Airline": leg.get('airline'),
                    "Departure_Time": leg.get('departure_airport', {}).get('time'),
                    "Arrival_Time": leg.get('arrival_airport', {}).get('time'),
                    "Price": f.get('price'),
                    "Stops": f.get('extensions', ['Non-stop'])[0]
                })
                time.sleep(1)
        current_date += timedelta(days=1)

    if all_rows:
        filename = 'google_multi_destination_flights.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=all_rows[0].keys())
            writer.writeheader()
            writer.writerows(all_rows)
        print(f"Success! Saved {len(all_rows)} flights to {filename}")

fetch_multi_day_flights()
