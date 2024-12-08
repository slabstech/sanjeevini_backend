import prance
from typing import List
from mistral_common.protocol.instruct.messages import UserMessage
import json
import requests
import functools
import ollama


def getDoctorById(id: int) -> str:
    try:
        method = 'GET'
        headers=None
        data=None
        url =  'http://localhost:8000/api/v1/doctorapp/' + str(id)
        response = requests.request(method, url, headers=headers, data=data)
        # Raise an exception if the response was unsuccessful
        response.raise_for_status()
        #response = make_api_call('GET', url + str(petId))
        if response.ok :
            json_response = response.json()
            if id == json_response['id']:
                return json_response
        return json.dumps({'error': 'Pet id not found.'})
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return json.dumps({'error': 'Pet id not found.'})
        else:
            return json.dumps({'error': 'Error with API.'})

def getUserByName(username: str) -> str:
    try:
        url = 'https://petstore3.swagger.io/api/v3/user/' + username
        response = requests.get(url)
        # Raise an exception if the response was unsuccessful
        response.raise_for_status()
        if response.ok :
            json_response = response.json()
            if username == json_response['username']:
                return json_response
        return json.dumps({'error': 'Username id not found.'})
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return json.dumps({'error': 'Username not found.'})
        else:
            return json.dumps({'error': 'Error with API.'})

names_to_functions = {
    'get_doctorapp': functools.partial(getDoctorById, id='')
}

#names_to_functions = {
#  'getDoctorById': functools.partial(getDoctorById, petId=''),
#  'getUserByName': functools.partial(getUserByName, username='')  
#}



def load_model(ollama_url, model_name):
    command = "/api/pull"
    url = ollama_url + command
    model = model_name + ":latest"
    payload = {"name": model}
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print("Request successful!")
        #print(response.text)
    else:
        print(f"Request failed with status code: {response.status_code}")
        ##print(response.text)


def get_user_messages(queries: List[str]) -> List[UserMessage]:
    user_messages=[]
    for query in queries:
        user_message = UserMessage(content=query)
        user_messages.append(user_message)
    return user_messages

def generate_tools_prompt(objs, function_end_point):
    parser = prance.ResolvingParser(function_end_point, backend='openapi-spec-validator')
    spec = parser.specification

    system_message = """
        You are a helpful assistant that parses OpenAPI specifications. Here are the key instructions:
        1. Parse the provided OpenAPI specification.
        2. Return values for function parameters only when the specification is complete.
        3. Do not return values for empty specifications.
        4. Do not explain or provide additional details.
        5. Do not hallucinate or add extra information.
    """

    # Split the user message into smaller parts
    user_message_part1 = f"""
    Parse this OpenAPI spec {spec} and return values of {objs} for function parameters. 
    Only return values in JSON for which the spec is complete. 
    Do not return values for empty specs. Do not explain, do not hallucinate. 
    Just return json, without any explanation.
    """

    user_message_part2 = """
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather for a city",
            "parameters": {
            "type": "object",
            "properties": {
                "city": {
                "type": "string",
                "description": "The name of the city",
                },
            },
            "required": ["city"],
            },
        }
    }
    """
    user_message = user_message_part1 + user_message_part2 


    combined_prompt = f"{system_message}\n\n{user_message}"
    
    model='mistral'
    result = execute_prompts(prompt=combined_prompt, model=model)
    #print(result['response'])
    function_value = result['response']
    #print(function_value)

    tool_json_value = json.loads(function_value) 
    #print(tool_json_value)
    return tool_json_value
    


def execute_prompts(prompt, model="llama3.2",url ="http://localhost:11434/api/generate", stream=False, raw=False):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream,
        "raw": raw,
    }
    result = ''
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        result = response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

    return result

def execute_generator():
    #queries = ["What's the status of my Pet 1?", "Find information of user user1?" ,  "What's the status of my Store Order 3?"]
    #return_objs = [['pet','petId'], ['user', 'username'], ['store/order','orderId']]
    queries = ["What is the status of User 1?"]
    return_objs = [['doctorapp','id']]
    function_end_point =  'http://localhost:8000/api/schema/?format=json'
    user_messages=get_user_messages(queries)
    #TODO - fix generate_tool_prompts to return correct json
    #user_tools = generate_tools_prompt(return_objs, function_end_point)

    user_tools_str = """
    {
    "type": "function",
    "function": {
        "name": "get_doctorapp",
        "description": "Get a doctor appointment by id",
        "parameters": {
        "type": "object",
        "properties": {
            "id": {
            "type": "integer"
            }
        },
        "required": ["id"]
        }
    }
    }
    """
    user_tools_json = json.loads(user_tools_str)
    #print(user_tools_json)
    tool_calls = tool_prompts_executor(user_tools_json)

    process_tool_calls(tool_calls, names_to_functions)



class Function:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class ToolCall:
    def __init__(self, function):
        self.function = function
 

def process_tool_calls(tool_calls, names_to_functions):
    index = 0
    try:
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_params = tool_call.function.arguments
            function_result = names_to_functions[function_name](**function_params)
            print(function_result)
            index += 1
    except KeyError:
        print(f"{function_name} is not defined")


def tool_prompts_executor(tools_json):
    response = ollama.chat(
        model='mistral',
        messages=[{'role': 'user', 'content':
            'What is the status of User 1?'}],

            # provide a weather checking tool to the model
        tools=[tools_json],
    )

    #print(response['message']['tool_calls'])
    tool_calls_result = response['message']['tool_calls']
    return tool_calls_result

execute_generator()