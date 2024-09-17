def get_query_extractor_system_prompt():

    prompt = """
    # Task:
    You are analyzing a transcription of a conversation between a doctor and a patient.
    Your job is to extract key symptoms, concerns, and any medical conditions mentioned by the patient.
    Rephrase these key details in a concise, search-friendly format suitable for a search engine query.

    The summary should be:
    - Focused on the patient's symptoms and concerns.
    - Rewritten in a way that would help a search engine find relevant medical information.
    - No longer than 2 sentences.

    If the transcription is unclear, make reasonable assumptions based on the context of the conversation.
    """

    return prompt

def get_query_extractor_user_prompt(transcription: str):

    prompt = f"""
    # Context:
    Below is the transcription of a conversation between a doctor and a patient.
    Extract key phrases related to the patient's symptoms, conditions, and concerns:

    Transcription:
    {transcription}

    Provide a search-friendly summary based on the above conversation.
    """

    return prompt