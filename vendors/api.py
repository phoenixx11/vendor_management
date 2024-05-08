import requests

# Base API URL (replace with your actual URL)
base_url = "http://localhost:8000/api/"

# Example: Create a new vendor
data = {'name': 'New Vendor', 'contact_info': 'new@vendor.com', 'address': '123 Main St'}
response = requests.post(base_url + 'vendors/', json=data)

# Check response status code
if response.status_code == 201:
    print("Vendor created successfully!")
else:
    print("Error creating vendor:", response.text)

# Example: Retrieve all vendors
response = requests.get(base_url + 'vendors/')
if response.status_code == 200:
    vendors = response.json()
    for vendor in vendors:
        print(vendor['name'], vendor['contact_info'])
else:
    print("Error retrieving vendors:", response.text)

# ... (Similar logic for GET, PUT, DELETE requests for other endpoints)
