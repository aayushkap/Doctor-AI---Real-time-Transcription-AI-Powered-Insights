from prompts.query_extractor_prompt import get_query_extractor_system_prompt, get_query_extractor_user_prompt
from prompts.reponse_generator_prompt import response_generator_system_prompt, response_generator_user_prompt
from services.faiss_service import read_from_vector_db
from services.azure_openai_service import make_api_call

class OrchestratorService:
    def __init__(self, transcription: str):
        self.transcription = transcription

    def query_extractor_bot(self):
        """
        LLM Call to extract Key Phrases from the transcription
        """

        system_prompt = get_query_extractor_system_prompt()
        user_prompt = get_query_extractor_user_prompt(self.transcription)

        res = make_api_call(system_prompt, user_prompt)

        if not res:
            raise Exception("Error in extracting query")
        return res

    def get_relavent_docs(self, query: str):
        """
        Faiss Call to get relevant documents
        """

        res = read_from_vector_db(query, 5)

        if not res:
            raise Exception("Error in getting relevant documents")
        return res


    def response_generator_bot(self, query: str, relevant_docs: list):
        """
        LLM Call to generate final response
        """

        system_prompt = response_generator_system_prompt()
        user_prompt = response_generator_user_prompt(query, relevant_docs)

        res = make_api_call(system_prompt, user_prompt)

        if not res:
            raise Exception("Error in generating response")

        return res
