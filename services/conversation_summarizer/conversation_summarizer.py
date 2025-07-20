from pydantic_ai import Agent
from pydantic_ai.usage import UsageLimits
from config.llms import conversation_summarizer_llm
from prompts.conversation_summarizer import conversation_summarizer_prompt
from models.schema import ConversationSummaryModel
from fastapi import APIRouter, Body
from utils.agent_execution import execute_agent_safely
# from firestore_utils import store_summary_to_firestore, get_summary_from_firestore


# FastAPI router setup
conversation_summarizer_router = APIRouter()

conversation_summarizer = Agent(
    model=conversation_summarizer_llm,
    system_prompt=conversation_summarizer_prompt,
    result_type=ConversationSummaryModel,
    retries=5
)

# def summarize_and_store(conversation_text: str, workflow_id: str):
#     summary = summarize_conversation(conversation_text)
#     store_summary_to_firestore(workflow_id, summary)
#     return summary
#
# def retrieve_summary(workflow_id: str) -> str:
#     return get_summary_from_firestore(workflow_id)


@conversation_summarizer_router.post("/summarize-conversation", response_model=ConversationSummaryModel)
async def summarize_conversation(conversation_history: str) -> ConversationSummaryModel:
    prompt = f"""
    # Conversation history: {conversation_history}

    *** Summarize the conversation in a concise and detailed manner. ***
    """

    response = await execute_agent_safely(conversation_summarizer, prompt)
    return response.data
