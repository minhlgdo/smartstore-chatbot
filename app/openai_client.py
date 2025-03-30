import openai
import asyncio
import logging

from app.variables import OPENAI_API_KEY, OPENAI_MODEL

openai.api_key = OPENAI_API_KEY
client = openai.OpenAI()
logging.basicConfig(level=logging.INFO)


async def generate_answer(faq_context: str, question: str):
    request = f"""
    Generate an answer to the following question with the following supported documents.
    Question: {question}
    Relevant documents: {faq_context}
    """
    response = client.responses.create(
            model=OPENAI_MODEL,
            instructions="You are a Naver Smart Store chatbot that generates answers based on the user's queries, conversation history, and related documents.",
            input=request,
            stream=True,
        )
    
    for chunk in response:
        if chunk.type == "response.completed":
            logging.info("Answer generation completed")
        elif chunk.type == "response.output_text.delta":
            await asyncio.sleep(0)
            yield chunk.delta


async def generate_followup_questions(history: str, faq_context: str, is_previously_relevant: bool = False):
    if is_previously_relevant:
        request = f"""
        Generate 1-2 follow-up questions based on the conversation history and supported documents. These questions should only related to the Smart Store. The output should start with -.
        Conversation history: \n{history}
        Relevant documents: {faq_context}
        """
    else:
        request = f"""
        Generate 1-2 follow-up questions based on the conversation history and relevant documents. These questions should only related to the Smart Store. The output should start with -.
        Conversation history: \n{history}
        """

    # logging.info(f"Request for follow-up questions: {request}")

    raw_response = client.responses.create(
        model=OPENAI_MODEL,
        instructions="You are a Naver Smart Store chatbot that generates answers based on the user's queries, conversation history, and related documents.",
        input=request,
        stream=True,
    )

    for chunk in raw_response:
        if chunk.type == "response.completed":
            logging.info("Follow-up questions generation completed")
        elif chunk.type == "response.output_text.delta":
            await asyncio.sleep(0)
            yield chunk.delta

