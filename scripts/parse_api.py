import requests
import json
from ollama import Client

def get_all_api():

    # Step 1: Fetch data from the URL
    url = "https://gaganyatri-sanjeevini-backend.hf.space/swagger/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Failed to fetch data from {url}")
        exit(1)

    # Step 2: Parse the data to extract required information
    # Assuming we want to extract the list of endpoints from the Swagger JSON
    endpoints = []
    for path, methods in data['paths'].items():
        for method, details in methods.items():
            endpoint = {
                'path': path,
                'method': method,
                'summary': details.get('summary', 'No summary available'),
                'description': details.get('description', 'No description available')
            }
            endpoints.append(endpoint)

    # Step 3: Format the extracted data
    formatted_data = json.dumps(endpoints, indent=2)

    return formatted_data


def get_appointment_data():
    print('hello')

def send_to_ollama(user_query, api_data):
    # Step 4: Send the formatted data to Ollama
    # Assuming Ollama has an API endpoint to accept input

    system_prompt = "Please summarize the following prompt into a concise and clear statement:"

    prompt = f"Here is more data: {api_data}. Please answer the following question: {user_query}"
    
    model = "llama3.2:latest"
    client = Client(host='http://localhost:11434')
    response = client.chat(
    model=model,
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": prompt,
        }
    ],
    )

    # Extract the model's response about the image
    response_text = response['message']['content'].strip()

   


