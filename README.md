# FAQ RAG Chatbot API
[🇰🇷 한국어 상세문서](./README_kr.md)

This is a simple RAG Chatbot API that answers questions related to [Naver SmartStore](https://help.sell.smartstore.naver.com/index.help). It first prepopulates the vector store and creates a database, then handles user's queries by comparing these embeddings with existing documents. 

## User manual
### Project configuration
**1. Create a virtual environment**
```bash
python3 -m venv .venv
```

**2. Activate the environment**
```bash
source .venv/bin/activate
```

**3. Install dependecies**
```bash
pip3 install -r requirements.txt
```

**4. Setting environment variables**
- Copy the `.env.example` file.

```bash
cp .env.example .env
```

- Add an OpenAI key to the `.env` file

### Running the server
```bash
uvicorn app.main:app --reload
```
You can access the API document at http://127.0.0.1:8000/docs

### Demo
There are two ways to check out the result.
1. Run the demo code in the repository. Make sure to run the server before executing this snippet.
```bash
cd demo
python3 demo.py
```
2. Access the API document in Swagger UI, and process the POST endpoint to start chatting.

## Project structure overview
```plaintext
smartstore-chatbot/
├── README.md
├── README_kr.md
├── app
│   ├── chroma_utils.py                     # Implementation logic for managing Chroma vector store
│   ├── db_utils.py                         # Implementation logic for managing the SQLite database
│   ├── main.py                             # Entry point for the FastAPI application
│   ├── models.py                           # API response models
│   ├── openai_client.py                    # Implementation logic for generating answers and follow-up questions
│   ├── text_utils.py                       # Implementation logic for handling text
│   └── variables.py                        # Store commonly used variables
├── assets
│   └── final_result.pkl                    # Reference data               
├── chatbot_db                              # SQLite database storing conversation history
├── chroma                                  # Vector store for RAG
├── demo
│   └── demo.py                             # Implementation logic for demo
├── requirements.txt
```
