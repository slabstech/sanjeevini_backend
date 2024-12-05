import prance
from typing import List
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_common.protocol.instruct.request import ChatCompletionRequest
from mistral_common.protocol.instruct.tool_calls import Function, Tool
import ollama
from mistral_common.protocol.instruct.messages import UserMessage
import json
import requests
import functools
import os


def getPetById(petId: int) -> str:
    try:
        method = 'GET'
        headers=None
        data=None
        url =  'https://petstore3.swagger.io/api/v3/pet/' + str(petId)
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
        print(response.text)
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)

def generate_tools(objs, function_end_point)-> List[Tool]:
    params = ['operationId', 'description',  'parameters']
    parser = prance.ResolvingParser(function_end_point, backend='openapi-spec-validator')
    spec = parser.specification
    
    user_tools = []
    for obj in objs:
        resource, field = obj
        path = '/' + resource + '/{' + field + '}'
        function_name=spec['paths'][path]['get'][params[0]]
        function_description=spec['paths'][path]['get'][params[1]]
        function_parameters=spec['paths'][path]['get'][params[2]]
        func_parameters = {
        "type": "object",
        "properties": {
            function_parameters[0]['name']: {
                "type": function_parameters[0]['schema']['type'],
                "description": function_parameters[0]['description']
            }
        },
        "required": [function_parameters[0]['name']]
    }
        user_function= Function(name = function_name, description = function_description, parameters = func_parameters, )
        user_tool = Tool(function = user_function)
        user_tools.append(user_tool)
    return user_tools


def get_user_messages(queries: List[str]) -> List[UserMessage]:
    user_messages=[]
    for query in queries:
        user_message = UserMessage(content=query)
        user_messages.append(user_message)
    return user_messages


def execute_generator():
    queries = ["What's the status of my Pet 1?", "Find information of user user1?" ,  "What's the status of my Store Order 3?"]
    return_objs = [['pet','petId'], ['user', 'username'], ['store/order','orderId']]
    function_end_point =  'https://petstore3.swagger.io/api/v3/openapi.json'
    user_messages=get_user_messages(queries)
    user_tools = generate_tools(return_objs, function_end_point)

    #create tokens for message and tools prompt
    tokenizer = MistralTokenizer.v3()
    completion_request = ChatCompletionRequest(tools=user_tools, messages=user_messages,)
    tokenized = tokenizer.encode_chat_completion(completion_request)
    _, text = tokenized.tokens, tokenized.text

    ollama_endpoint_env = 'http://localhost:11434'
    #ollama_endpoint_env = os.environ.get('OLLAMA_ENDPOINT')
    model = "mistral:7b"
    prompt = text 

    #if ollama_endpoint_env is None:
    #    ollama_endpoint_env = 'http://localhost:11434'
    ollama_endpoint = ollama_endpoint_env +  "/api/generate"  # replace with localhost

    response = requests.post(ollama_endpoint,
                      json={
                          'model': model,
                          'prompt': prompt,
                          'stream':False,
                          'raw': True
                      }, stream=False
                      )
    
    response.raise_for_status()
    result = response.json()

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
            print(messages[index].content)
            function_result = names_to_functions[function_name](**function_params)
            print(function_result)
            index = index + 1
    except:
        print(function_name + " is not defined")

#execute_generator()

def get_objects_parameters(url):
    parser = prance.ResolvingParser(url, backend='openapi-spec-validator')
    spec = parser.specification
    object_names = spec['components']['schemas'].keys()
    for key in list(object_names):
        print(key)
        properties = spec['components']['schemas'][key]
        print(properties)


def tool_call_function():

    ollama_url = "http://localhost:11434"
    model_name = "mistral"
    load_model( ollama_url, model_name )

    return_objs = [['pet','petId'], ['user', 'username'], ['store/order','orderId']]
    function_end_point =  'https://petstore3.swagger.io/api/v3/openapi.json'

    # return_objs = get_objects_parameters(function_end_point)
    user_tools = generate_tools(return_objs, function_end_point)
    print(user_tools)


tool_call_function()
execute_generator()