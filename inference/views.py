from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from mistralai import Mistral
import os
import requests
from openai import OpenAI
from ollama import Client
from django.http import FileResponse
import io
from rest_framework.generics import GenericAPIView


from rest_framework import serializers

class TextLLMSerializer(serializers.Serializer):
    isOnline = serializers.BooleanField()
    model = serializers.CharField(max_length=100)
    messages = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(max_length=100)
        )
    )

class SpeechASRSerializer(serializers.Serializer):
    audio = serializers.FileField()
    prompt = serializers.CharField(required=False)

class SpeechLLMSerializer(serializers.Serializer):
    audio = serializers.FileField()
    prompt = serializers.CharField(required=False)

class SpeechToSpeechSerializer(serializers.Serializer):
    audio = serializers.FileField()
    prompt = serializers.CharField(required=False)

class TTSSerializer(serializers.Serializer):
    tts_text = serializers.CharField(max_length=1000)

class TTSView(GenericAPIView):
    serializer_class = TTSSerializer
    def post(self, request, format=None):
        # Define the API endpoint
        # Define the URL for the TTS API
        url = 'http://localhost:5002/api/tts'

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data['tts_text']
        # Define the multiline text
        text = "This is the first line"

        # Prepare the parameters for the GET request
        params = {
            'text': text
        }

        # Make the GET request
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the audio response as a WAV file
            # Create a file-like object with the audio data
            audio_data = io.BytesIO(response.content)

            # Return the audio file as a response
            return FileResponse(audio_data, as_attachment=True, filename='audio_output.wav')
        else:
            return Response({"error": "Failed to synthesize speech"}, status=response.status_code)

class SpeechASRView(GenericAPIView):
    serializer_class = SpeechASRSerializer

    def post(self, request, format=None):
        try: 
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            audio = serializer.validated_data['audio']
            client = OpenAI(api_key="cant-be-empty", base_url="http://0.0.0.0:11800/v1/")
            #filename= '/home/gaganyatri/Music/test1.flac'
            audio_bytes = audio.read()

            #audio_file = open(filename, "rb")

            transcript = client.audio.transcriptions.create(
                model="Systran/faster-distil-whisper-small.en", file=audio_bytes
            )

            #print(transcript.text)
            voice_content = transcript.text
            return Response({"response": voice_content})
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({'error': 'Something went wrong'}, status=500)


class SpeechToSpeechView(GenericAPIView):
    serializer_class = SpeechToSpeechSerializer

    def post(self, request, format=None):
        try: 
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            audio = serializer.validated_data['audio']

            client = OpenAI(api_key="cant-be-empty", base_url="http://0.0.0.0:11800/v1/")

            #filename= '/home/gaganyatri/Music/test1.flac'
            audio_bytes = audio.read()

            #audio_file = open(filename, "rb")

            transcript = client.audio.transcriptions.create(
                model="Systran/faster-distil-whisper-small.en", file=audio_bytes
            )

            #print(transcript.text)
            voice_content = transcript.text
                        #content = 'audio recieved'
            system_prompt = "Please summarize the following prompt into a concise and clear statement:"


            model = "mistral-nemo:latest"
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
                    "content": voice_content,
                }
            ],
            )

            # Extract the model's response about the image
            response_text = response['message']['content'].strip()

            url = 'http://localhost:5002/api/tts'

            # Define the multiline text
            #text = "This is the first line"

            # Prepare the parameters for the GET request
            params = {
                'text': response_text
            }

            # Make the GET request
            response = requests.get(url, params=params)

            # Check if the request was successful
            if response.status_code == 200:
                # Save the audio response as a WAV file
                # Create a file-like object with the audio data
                audio_data = io.BytesIO(response.content)

                # Return the audio file as a response
                return FileResponse(audio_data, as_attachment=True, filename='audio_output.wav')
            else:
                return Response({"error": "Failed to synthesize speech"}, status=response.status_code)

        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({'error': 'Something went wrong'}, status=500)

class SpeechLLMView(GenericAPIView):
    serializer_class = SpeechLLMSerializer

    def post(self, request, format=None):
        try: 
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            audio = serializer.validated_data['audio']

            client = OpenAI(api_key="cant-be-empty", base_url="http://localhost:11800/v1/")

            #filename= '/home/gaganyatri/Music/test1.flac'
            audio_bytes = audio.read()

            #audio_file = open(filename, "rb")

            transcript = client.audio.transcriptions.create(
                model="Systran/faster-distil-whisper-small.en", file=audio_bytes
            )

            #print(transcript.text)
            voice_content = transcript.text
                        #content = 'audio recieved'

            model = "llama3.2:latest"
            client = Client(host='http://localhost:11434')
            response = client.chat(
            model=model,
            messages=[{
            "role": "user",
            "content": voice_content,
            }],
            )

            # Extract the model's response about the image
            response_text = response['message']['content'].strip()

            return Response({"response": response_text})
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({'error': 'Something went wrong'}, status=500)

class TextLLMView(GenericAPIView):
    serializer_class = TextLLMSerializer
    def post(self, request, format=None):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            data = serializer.validated_data
            isOnline = True

            prompt =  data['messages'][0]['prompt']
            # Specify model
            #model = "pixtral-12b-2409"
            model = data['model']
            # Define the messages for the chat
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]

            if(isOnline): 
                api_key = os.environ["MISTRAL_API_KEY"]

                # Initialize the Mistral client
                client = Mistral(api_key=api_key)


                # Get the chat response
                chat_response = client.chat.complete(
                    model=model,
                    messages=messages
                )

                content = chat_response.choices[0].message.content
            else:
                content = "helloWorld"

            #print(chat_response.choices[0].message.content)
            # Return the content of the response
            return Response({"response": content})
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({'error': 'Something went wrong'}, status=500)

