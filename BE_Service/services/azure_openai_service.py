from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    azure_deployment="gpt-4o-mini",  # or your deployment
    api_version="2023-06-01-preview",  # or your api version
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

def make_api_call(system_prompt:str, user_prompt:str):
    messages = [
        (
            "system",
            system_prompt,
        ),
        ("human", user_prompt),
    ]

    ai_msg = llm.invoke(messages)

    return ai_msg.content
