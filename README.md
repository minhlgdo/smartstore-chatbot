# chatbot-api

## User manual

### Project configuration 프로젝트 설정
**1. Create a virtual environment **
```
python3 -m venv .venv
```

**2. Activate the environment **
```
source .venv/bin/activate
```

**3. Install dependecies**
```
pip3 install -r requirements.txt
```

### Running the server
```
uvicorn chatbot.main:app --reload
```
You can access the API document at http://127.0.0.1:8000/docs

