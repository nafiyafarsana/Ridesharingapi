import requests


# User registration
registration_data = {'email': 'user@example.com', 'password': 'password123'}
response = requests.post('http://127.0.0.1:8000/api/v1/register/', json=registration_data)
if response.status_code == 201:
    print("User registered successfully.")
    print(response.content.decode())  # Print response content
else:
    print("Failed to register user. Status code:", response.status_code)

# User login
login_data = {'email': 'user@example.com', 'password': 'password123'}
response = requests.post('http://127.0.0.1:8000/api/v1/login/', json=login_data)
if response.status_code == 200:
    token = response.json().get('token')
    print("Token obtained successfully:", token)
else:
    print("Failed to obtain token. Status code:", response.status_code)