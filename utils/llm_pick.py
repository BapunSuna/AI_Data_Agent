from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os

load_dotenv()


def pick_llm(level: str):
    """
    Picks the appropriate llm based on the level of question

    Args:
        level(str): The level of the question. Can be "low", "medium" or "high"

    Returns:
        ChatOpenAI: The LLM instance to be used
    """
    if level.lower() == "low":
        llm = ChatOpenAI(
            model="openai/gpt-5.6-luna",
            temperature=0,
            # model_kwargs={"reasoning_effort": "none"},
            reasoning_effort="none",
            base_url="https://api.aicredits.in/v1",
            api_key=os.environ["AICREDITS_API_KEY"],
        )
    elif level.lower() == "medium":
        llm = ChatOpenAI(
            model="openai/gpt-5.6-terra",
            temperature=0,
            # model_kwargs={"reasoning_effort": "none"},
            reasoning_effort="none",
            base_url="https://api.aicredits.in/v1",
            api_key=os.environ["AICREDITS_API_KEY"],
        )
    elif level.lower() == "high":
        llm = ChatOpenAI(
            model="openai/gpt-5.6-sol",
            temperature=0,
            # model_kwargs={"reasoning_effort": "none"},
            reasoning_effort="none",
            base_url="https://api.aicredits.in/v1",
            api_key=os.environ["AICREDITS_API_KEY"],
        )
    elif level.lower() == "claude":
        llm = ChatAnthropic(
            model="anthropic/claude-sonnet-4.6",
            base_url="https://api.aicredits.in",
            api_key=os.environ["AICREDITS_API_KEY"],
        )
    else:
        raise ValueError(f"Unsupported level: {level}")

    return llm


if __name__ == "__main__":
    llm_obj = pick_llm("low")
    print(llm_obj.invoke("What is the capital of France"))
