import requests

response = requests.post(
    "http://127.0.0.1:8000/chat",
    json={"message": "What is humidity?"}
)

print("Status Code:", response.status_code)
print("Raw Text:", response.text)  # This shows what came back from the server
