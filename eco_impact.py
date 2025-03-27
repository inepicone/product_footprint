import requests
import random
import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from time import sleep

# Function to fetch a random product
def get_product():
    url = "https://world.openfoodfacts.org/cgi/search.pl?search_simple=1&action=process&json=1&page_size=50"
    response = requests.get(url)
    data = response.json()
    
    valid_products = [
        (p.get("product_name", "Unknown"), p.get("origins", "").strip())
        for p in data.get("products", [])
        if p.get("origins") and p["origins"].strip().lower() != "unknown"
    ]
    
    return random.choice(valid_products) if valid_products else (None, None)

# Function to get coordinates of a location
def get_coordinates(location):
    geolocator = Nominatim(user_agent="eco-impact-app")
    try:
        loc = geolocator.geocode(location)
        return (loc.latitude, loc.longitude) if loc else None
    except:
        sleep(2)
        return get_coordinates(location)

# Main execution
def main():
    product, origin = get_product()
    if not product:
        print("No valid products found.")
        return
    
    print(f"Selected product: {product} from {origin}")
    
    user_location = "Tokyo, Japan"  # Hardcoded or use input()
    
    user_coords = get_coordinates(user_location)
    product_coords = get_coordinates(origin)

    if user_coords and product_coords:
        distance_km = geodesic(user_coords, product_coords).kilometers
        fuel_liters = distance_km / 3  # 3 km per liter
        
        print(f"Distance: {distance_km:.2f} km")
        print(f"Estimated fuel consumption: {fuel_liters:.2f} liters")
        
        # Create map
        m = folium.Map(location=[(user_coords[0] + product_coords[0]) / 2, 
                                 (user_coords[1] + product_coords[1]) / 2], zoom_start=5)
        folium.Marker(user_coords, popup="User", icon=folium.Icon(color="blue")).add_to(m)
        folium.Marker(product_coords, popup=f"Origin: {origin}", icon=folium.Icon(color="green")).add_to(m)
        folium.PolyLine([user_coords, product_coords], color="red", weight=2.5).add_to(m)
        m.save("map.html")
    else:
        print("Could not calculate distance.")

if __name__ == "__main__":
    main()
