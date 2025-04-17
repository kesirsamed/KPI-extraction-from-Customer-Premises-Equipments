import geocoder

# Get the location using your current IP address (IP geolocation)
g = geocoder.ip('me')

# Print the latitude and longitude
print(f"Latitude: {g.latlng[0]}")
print(f"Longitude: {g.latlng[1]}")
