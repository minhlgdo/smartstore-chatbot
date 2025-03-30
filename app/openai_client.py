import openai
import asyncio
import logging

from app.variables import ANSWER_ERROR_MESSAGE, OPENAI_API_KEY, OPENAI_MODEL, QUESTION_ERROR_MESSAGE

openai.api_key = OPENAI_API_KEY
client = openai.OpenAI()
logging.basicConfig(level=logging.INFO)


async def generate_answer(faq_context: str, question: str):
    request = f"""
    Generate an answer to the following question with the following supported documents.
    Question: {question}
    Relevant documents: {faq_context}
    """
    try:
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
    except Exception as e:
        logging.error(f"Error generating answer: {e}")
        yield ANSWER_ERROR_MESSAGE
    except openai.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        yield ANSWER_ERROR_MESSAGE


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
        
    try: 
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
    
    except Exception as e:
        logging.error(f"Error generating follow-up questions: {e}")
        yield QUESTION_ERROR_MESSAGE
    except openai.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        yield QUESTION_ERROR_MESSAGE

