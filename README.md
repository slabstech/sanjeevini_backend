# sanjeevni_backend
Server for Sanjeevini Health App


- Check the project demo on Youtube - 

<a href="https://www.youtube.com/watch?v=KHK_jaB4D0g" target="_blank">
  <img src="https://img.youtube.com/vi/KHK_jaB4D0g/0.jpg" alt="Watch the video">
</a>



- Setup
  - Create virtual environment
    - `python -m venv venv`
  - Activate virtual enviroment
    - `source venv/bin/activate`
  - Install required libraries
    - `pip install -r requirements.txt`

  - For Inference
    - local
      - Run ollama 
    - cloud
      - Add Mistral API Key
        - export MISTRAL_API_KEY='Your-Mistral-Api-Key'
  - Run migrations
    - `python manage.py migrate`
  - Start server
    - `python manage.py runserver`


