def response_generator_system_prompt():

    prompt = """
    # Task:
    You are provided with a summary of symptoms and key phrases extracted from a conversation between a doctor and a patient,
    along with a list of relevant documents, for those symptoms and key phrases.

    Your task is to generate a response addressing the patient's questions and concerns, in a concise, informative, and professional manner.

    The response should:
    - Offer suggestions and recommendations based on the provided symptoms and key phrases.
    - Be empathetic, informative, and professional.
    - Be concise and written in an easy-to-understand manner.
    - Be in Markdown format.
    - Must not be in the format of en email or a text message. Only reply as regular text.

    Remember to use the relevant documents to support your recommendations.
    """

    return prompt

def response_generator_user_prompt(symptoms: str, relevant_docs: list):

    prompt = f"""
    # Context:

    - Symptoms and Key Phrases:
        {symptoms}

    - Relevant Documents for Reference:
        {', '.join(relevant_docs)}

    """

    return prompt
