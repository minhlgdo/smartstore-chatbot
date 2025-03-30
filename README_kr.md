# FAQ RAG Chatbot API
[🇺🇸 English document](./README.md)

[네이버 스마트스토어](https://help.sell.smartstore.naver.com/index.help)와 관련된 질문에 답변하는 RAG 챗봇 API입니다. vector store 미리 채우고 데이터베이스를 셋업한 후에 사용자의 쿼리를 처리합니다.

## 사용문서
### 프로젝트 설정
**1. 가상환경 설정**
```bash
python3 -m venv .venv
```

**2. 가상환경 시작**
```bash
source .venv/bin/activate
```

**3. 필요적인 패키지 설치**
```bash
pip3 install -r requirements.txt
```

**4.환경변수 설정**
- `.env.example` 파일 복사

```bash
cp .env.example .env
```

- `.env` 파일에 `OPENAI_API_KEY` 추가

### 서버 활성화
```bash
uvicorn app.main:app --reload
```
API 문서는 http://127.0.0.1:8000/docs 에서 확인할 수 있습니다.

### 데모 시연
1. 코드 실행하기 전에 서버 시작해야 하여 아래 데모 코드를 실행합니다.
```bash
cd demo
python3 demo.py
```
2. Swagger UI에서 POST `/chat` endpoint 접속하여 시도합니다.

### 프로젝트 구조
```plaintext
smartstore-chatbot/
├── README.md
├── README_kr.md
├── app
│   ├── chroma_utils.py                 # Chroma 벡터 스토어 관리하는 코드 
│   ├── db_utils.py                     # SQLite 데이터베이스 관리하는 코드
│   ├── main.py                         # FastAPI 애플리케이션의 진입점
│   ├── models.py                       # API 응답 모델
│   ├── openai_client.py                # 답변 및 후속 질문 생성하는 코드
│   ├── text_utils.py                   # 텍스트 처리하는 코드
│   └── variables.py                    # 자주 사용되는 변수들을 저장
├── assets
│   └── final_result.pkl                # 참조 데이터           
├── chatbot_db                          # 대화 기록을 저장하는 SQLite 데이터베이스
├── chroma                              # RAG를 위한 벡터 스토어
├── demo
│   └── demo.py                         # 데모를 위한 구현 로직
├── requirements.txt
```


