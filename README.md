DJANGO VENDOR MANAGEMENT PROJECT

Description:
A robust and user-friendly Django application for managing vendors, including creating, retrieving, updating, and deleting vendor information, as well as handling purchase orders.

Features:
*Vendor Management: Create, retrieve, update, and delete vendor profiles with details like name, contact information, and address.
*Purchase Order Management: Create, retrieve, update, and delete purchase orders associated with vendors, including items and total cost.
*RESTful API: Exposes a clean and well-documented RESTful API for efficient interaction with the application using various tools and libraries.

Installation:Prerequisites:

Python 3.x (https://www.python.org/downloads/)
pip (https://pip.pypa.io/en/stable/installation/)

Project Setup:

STEP_1)Open a terminal or command prompt.
Navigate to a directory where you want to create your project.
Create a New Django Project:django-admin startproject django-vendor-management

STEP_2)Navigate to the Project Directory:
cd django-vendor-management

STEP_3)Create a Django App (Optional but Recommended):
If you intend to separate the vendor management functionality from your main project, create a Django app:
python manage.py startapp vendors

STEP_4)Create a Virtual Environment:
python3 -m venv venv  # Replace "venv" with your desired environment name
venv\Scripts\activate.bat  # Activate the virtual environment (Windows)

STEP_5)Install Dependencies:pip install -r requirements.txt
(Make sure requirements.txt is present in your project root and lists all necessary packages, including django and djangorestframework.)

STEP_6)Run Migrations:
python manage.py makemigrations
python manage.py migrate
*(mention directory name in the settings file under the INSTALLATIONS)

STEP_7)Start the Development Server:python manage.py runserver
This will typically start the server at http://127.0.0.1:8000/. 

*API Endpoints:*
The project utilizes a RESTful API. Here's an overview of the key endpoints (refer to the documentation for detailed request and response formats):

Vendors:

/vendors/:
Method: POST (Create a new vendor)
Request Body: JSON data containing vendor details (e.g., name, contact_info, address)
Response: JSON object representing the newly created vendor.
/vendors/<int:pk>/:
Method: GET (Retrieve details of a specific vendor)
Parameters: pk (integer ID of the vendor)
Response: JSON object containing the vendor's data.
Methods: PUT (Update an existing vendor), DELETE (Delete a vendor)
/vendors/:
Method: GET (List all vendors)
Response: JSON array containing all vendor objects.
Purchase Orders:

/purchase_orders/:
Method: POST (Create a new purchase order)
Request Body: JSON data containing purchase order details (e.g., vendor, items, total_cost)
Response: JSON object representing the newly created purchase order.
/purchase_orders/<int:pk>/:
Method: GET (Retrieve details of a specific purchase order)
Parameters: pk (integer ID of the purchase order)
Response: JSON object containing the purchase order's data.
Methods: PUT (Update an existing purchase order), DELETE (Delete a purchase order)
/purchase_orders/:
Method: GET (List all purchase orders)
Response: JSON array containing all purchase order objects.
Additional Notes:

Consider using a documentation tool like API3docs to provide a more interactive and user-friendly API reference.


