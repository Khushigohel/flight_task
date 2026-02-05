from amadeus import Client, ResponseError
from datetime import datetime, timedelta
import pandas as pd
import time

# today = datetime.now()
# FLIGHT_DATE = today.strftime("%Y-%m-%d")
FLIGHT_DATE="2026-02-12"

SOURCE = "AMD"
DESTINATIONS = ["DEL"]

amadeus = Client(
    client_id="BwyvDrPaFMewXc2aba6ke6PIEG6ImscT",
    client_secret="7L7Qeoo3uAbTv4TL"
)

results = []

for dest in DESTINATIONS:
    try:
        print(f"Fetching flights: {SOURCE} -> {dest} on {FLIGHT_DATE}")

        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=SOURCE,
            destinationLocationCode=dest,
            departureDate=FLIGHT_DATE,
            adults=1,
            currencyCode="INR"
        )
        
        
        if not response.data:
            print(f"No flights found for {dest} tomorrow.")
            continue

        for offer in response.data:
            itinerary = offer["itineraries"][0]
            segment = itinerary["segments"][0]
            carrier_code = segment["carrierCode"]
            
        
            try:
                airline_resp = amadeus.reference_data.airlines.get(airlineCodes=carrier_code)
                airline_name = airline_resp.data[0]["businessName"]
            except:
                airline_name = carrier_code  

            results.append({
                "date": FLIGHT_DATE,
                "source": SOURCE,
                "destination": dest,
                "departure_time": segment["departure"]["at"],
                "arrival_time": segment["arrival"]["at"],
                "airline": airline_name,
                "stops": len(itinerary["segments"]) - 1,
                "price": offer["price"]["total"]
            })
            # Respect API rate limits
            #time.sleep(1)

    except ResponseError as err:
        print("Amadeus error:", err)

# 2. SAVE TO CSV
if results:
    df = pd.DataFrame(results)
    filename = f"amadeus_flights1_{FLIGHT_DATE}.csv"
    df.to_csv(filename, index=False)
    print(f"\n Done! Saved {len(results)} flights to: {filename}")
else:
    print("\n No data collected.")