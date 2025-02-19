import requests

# API URL (Replace with your actual Render API URL)
url = "https://fastapi-gpt-api.onrender.com/upload/"

# Path to the PDF file you want to upload (Make sure the file exists)
file_path = "example.pdf"

# Open the file and send it to the API
with open(file_path, "rb") as file:
    files = {"file": file}
    response = requests.post(url, files=files)

# Print the response from the API
print(response.json())
