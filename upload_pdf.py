import requests

# ✅ Ensure this URL matches your Render deployment
url = "https://fastapi-gpt-api.onrender.com/upload/"

file_path = "example.pdf"  # Ensure this file exists

# Upload the file
with open(file_path, "rb") as file:
    files = {"file": file}
    response = requests.post(url, files=files)

print(response.json())  # See the API response
