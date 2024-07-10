from flask import Flask, jsonify
import requests

app = Flask(__name__)

window_size = 10

numbers_store = []

THIRD_PARTY_SERVER = "http://20.244.56.144/test/"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzIwNTkyNzI1LCJpYXQiOjE3MjA1OTI0MjUsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjdmNzExN2RhLTczODQtNDIyZS05YmY5LTZmNWNhY2ViOTc5NyIsInN1YiI6InNlMjF1Y3NlMDMzQG1haGluZHJhdW5pdmVyc2l0eS5lZHUuaW4ifSwiY29tcGFueU5hbWUiOiJNYWhpbmRyYSBVbml2ZXJzaXR5IiwiY2xpZW50SUQiOiI3ZjcxMTdkYS03Mzg0LTQyMmUtOWJmOS02ZjVjYWNlYjk3OTciLCJjbGllbnRTZWNyZXQiOiJ0dXlLY3pmakxFWWxmeWJ6Iiwib3duZXJOYW1lIjoiQmhhdmVzaCBLdW1hciBSYWt0YW5pIiwib3duZXJFbWFpbCI6InNlMjF1Y3NlMDMzQG1haGluZHJhdW5pdmVyc2l0eS5lZHUuaW4iLCJyb2xsTm8iOiJTRTIxVUNTRTAzMyJ9.mPC1AJuAoT-WmeOP26hymRpehxQGHfYGiZh8rfQ7u70"

def fetch_numbers(number_id):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    try:
        response = requests.get(f"{THIRD_PARTY_SERVER}{number_id}", headers=headers, timeout=0.5)
        response.raise_for_status() 
        return response.json().get('numbers', [])
    except (requests.RequestException, ValueError):
        return []

@app.route('/numbers/<number_id>', methods=['GET'])
def get_numbers(number_id):
    global numbers_store
    if number_id not in ['p', 'f', 'e', 'r']:
        return jsonify({"error": "Invalid number ID"}), 400

    new_numbers = fetch_numbers(number_id)
    unique_numbers = list(set(new_numbers))  


    numbers_store.extend(unique_numbers)
    numbers_store = numbers_store[-window_size:]  

    avg = sum(numbers_store) / len(numbers_store) if numbers_store else 0

    response = {
        "windowPrevState": numbers_store[:-len(unique_numbers)],
        "windowCurrState": numbers_store,
        "numbers": new_numbers,
        "avg": round(avg, 2)
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(port=9876)
