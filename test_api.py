import requests
import json
# <p><a href="/history">View Analysis History</a></p>
# Test batch analysis
url = "http://localhost:5000/analyze-batch"
data = {
    "texts": [
        "This is a nice comment",
        "I hate you all",
        "Have a great day!"
    ]
}

response = requests.post(url, json=data)
print("Batch Analysis Response:")
print(json.dumps(response.json(), indent=2))

# Test history
history_response = requests.get("http://localhost:5000/history")
print("\nHistory Response:")
print(json.dumps(history_response.json(), indent=2))