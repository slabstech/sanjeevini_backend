import prance
from typing import List
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_common.protocol.instruct.request import ChatCompletionRequest
from mistral_common.protocol.instruct.tool_calls import Function, Tool
from mistral_common.protocol.instruct.messages import UserMessage
import json
import requests
import functools
import os
from ollama import Client
import ollama


def getPetById(petId: int) -> str:
    try:
        method = 'GET'
        headers=None
        data=None
        url =  'http://localhost:8000/api/v1/doctorapp/' + str(petId)
        response = requests.request(method, url, headers=headers, data=data)
        # Raise an exception if the response was unsuccessful
        response.raise_for_status()
        #response = make_api_call('GET', url + str(petId))
        if response.ok :
            json_response = response.json()
            if petId == json_response['id']:
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
  'getPetById': functools.partial(getPetById, petId=''),
  'getUserByName': functools.partial(getUserByName, username='')  
}


import requests

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
    params = ['operationId', 'description',  'parameters']
    parser = prance.ResolvingParser(function_end_point, backend='openapi-spec-validator')
    spec = parser.specification
    #print(spec)

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
    Parse this OpenAPI spec {spec} and return values of {objs} for function parameters. Only return values in JSON for which the spec is complete. Do not return values for empty specs. Do not explain, do not hallucinate.
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
    """

    user_message_part3 = """
                            "format": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"],
                                "description": "The temperature unit to use. Infer this from the users location.",
                            },
                        },
                        "required": ["location", "format"],
                    },
    """

    # Combine the parts
    user_message = user_message_part1 + user_message_part2 

# Combine and send the messages

    # Combine and send the messages
    combined_prompt = f"{system_message}\n\n{user_message}"
    
    model='mistral'
    result = execute_prompts(prompt=combined_prompt, model=model)
    #print(result['response'])
    function_value = result['response']
    print(function_value)

    tool_json_value = json.loads(function_value) 
    print(tool_json_value)
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
    queries = ["What's the status of my Pet 1?"]
    return_objs = [['doctorapp','id']]
    function_end_point =  'http://localhost:8000/api/schema/?format=json'
    user_messages=get_user_messages(queries)
    #user_tools = generate_tools(return_objs, function_end_point)
    user_tools = generate_tools_prompt(return_objs, function_end_point)

    #create tokens for message and tools prompt
    tokenizer = MistralTokenizer.v3()
    completion_request = ChatCompletionRequest(tools=user_tools, messages=user_messages,)
    tokenized = tokenizer.encode_chat_completion(completion_request)
    _, text = tokenized.tokens, tokenized.text

    model = "mistral:7b"
    prompt = text 
    #print(prompt)
    #if ollama_endpoint_env is None:
    #    ollama_endpoint_env = 'http://localhost:11434'
    url = "http://localhost:11434/api/generate"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False,
        "raw": True,

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

    print(result)
    #result = response.json
    process_results(result, user_messages)

 
def process_results(result, messages):

    result_format = result['response'].split("\n\n")
    result_tool_calls = result_format[0].replace("[TOOL_CALLS] ","")

    tool_calls = json.loads(result_tool_calls)
    index = 0 
    try:
        for tool_call in tool_calls:
            function_name = tool_call["name"]
            function_params = (tool_call["arguments"]) 
            #print(messages[index].content)
            function_result = names_to_functions[function_name](**function_params)
            #print(function_result)
            index = index + 1
    except:
        print(function_name + " is not defined")

#execute_generator()

def get_objects_parameters(url):
    parser = prance.ResolvingParser(url, backend='openapi-spec-validator')
    spec = parser.specification
    object_names = spec['components']['schemas'].keys()
    for key in list(object_names):
        #print(key)
        properties = spec['components']['schemas'][key]
        #print(properties)


#tool_call_function()
#execute_generator()
return_objs = [['doctorapp','id']]
function_end_point =  'http://localhost:8000/api/schema/?format=json'
user_tools = generate_tools_prompt(return_objs, function_end_point)
#print(user_tools)

def ollama_tools():
    response = ollama.chat(
        model='mistral',
        messages=[{'role': 'user', 'content':
            'What is the weather in Toronto?'}],

            # provide a weather checking tool to the model
        tools=[{
        'type': 'function',
        'function': {
            'name': 'get_current_weather',
            'description': 'Get the current weather for a city',
            'parameters': {
            'type': 'object',
            'properties': {
                'city': {
                'type': 'string',
                'description': 'The name of the city',
                },
            },
            'required': ['city'],
            },
        },
        },
    ],
    )

    print(response['message']['tool_calls'])



def ollama_tools_prompt(tools_json):
    response = ollama.chat(
        model='mistral',
        messages=[{'role': 'user', 'content':
            'What is the status of User 1?'}],

            # provide a weather checking tool to the model
        tools=[tools_json],
    )

    print(response['message']['tool_calls'])


#ollama_tools_prompt(user_tools)