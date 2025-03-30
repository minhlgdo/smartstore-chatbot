from fastapi import FastAPI
import logging

from fastapi.responses import StreamingResponse

from app.chroma_utils import get_relevant_faq, is_relevant_query
from app.db_utils import get_chat_history, insert_chat_log
from app.models import QueryInput
from app.openai_client import generate_answer, generate_followup_questions
from app.variables import ANSWER_ERROR_MESSAGE, QUESTION_ERROR_MESSAGE

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize
app = FastAPI(
    title="RAG 챗봇",
    description="스마트스토어에 관련 질문에 대한 답변을 제공하는 챗봇입니다.",
)


async def generate_full_chat_answer(session_id: str, faq_context: str, question: str):
    full_answer = ""

    # Check the relevance of the question to the SmartStore
    is_relevant = is_relevant_query(question)
    if not is_relevant:
        answer = "저는 스마트 스토어 FAQ를 위한 챗봇입니다. 스마트 스토어에 대한 질문을 부탁드립니다."
        full_answer += answer
        yield answer
    else:
        # Generate answer chunk
        async for answer_chunk in generate_answer(
            faq_context=faq_context, question=question
        ):
            if answer_chunk == ANSWER_ERROR_MESSAGE:
                yield answer_chunk
                return
            full_answer += answer_chunk
            yield answer_chunk

    insert_chat_log(
        session_id=session_id,
        user_query=question,
        chatbot_response=full_answer,
    )

    history = get_chat_history(session_id=session_id)
    yield "\n\n"

    # Generate follow-up question
    async for question_chunk in generate_followup_questions(
        history=history,
        faq_context=faq_context,
        is_previously_relevant=is_relevant,
    ):
        if question_chunk == QUESTION_ERROR_MESSAGE:
            yield question_chunk
            return
        yield question_chunk


@app.post("/chat")
async def chat(query: QueryInput):
    session_id = query.session_id
    question = query.question

    # Generate relevant FAQ context
    faq_context = get_relevant_faq(question)
    if not faq_context or faq_context == "":
        return StreamingResponse(
            iter(["응답을 생성 중에 오류가 발생했습니다. 다시 시도해주세요."]), media_type="text/event-stream"
        )
    
    logging.info(f"FAQ context: {faq_context}")

    return StreamingResponse(
        generate_full_chat_answer(
            session_id=session_id, faq_context=faq_context, question=question
        ),
        media_type="text/event-stream",
    )
