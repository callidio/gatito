from logger_helper import setup_logger
import google.generativeai as genai
import time

class GenAIClient:
    def __init__(self, api_key, path_to_rule_file):
        self.logger = setup_logger(self.__class__.__name__, f"{self.__class__.__name__}.log")
        self.logger.info("Initializing GenAIClient")
        
        # Configure the genai client with the provided API key
        genai.configure(api_key=api_key)
        self.path_to_rule_file = path_to_rule_file
        self.upload_file_content()

    def upload_file_content(self):
        self.logger.info(f"{self.upload_file_content.__name__} - Uploading file content")
        # Upload the file using the Files API
        self.rule_file = genai.upload_file(path=self.path_to_rule_file)
        # Wait for the file to finish processing
        while self.rule_file.state.name == 'PROCESSING':
            self.logger.info('Waiting for rule_file to be processed.')
            time.sleep(2)
            self.rule_file = genai.get_file(self.rule_file.name)
        self.logger.info(f'Rule processing complete: {self.rule_file.uri}')

    def process_input(self, external_prompt):
        self.logger.info(f"{self.process_input.__name__} - Processing input")
        # Directly create a GenerativeModel instance without using cached content
        model = genai.GenerativeModel(
            model_name='models/gemini-1.5-flash-001',
        )
        answer = None
        try:
            # Query the model
            response = model.generate_content([
                external_prompt, 
                'You are a men chat assistant. '
                'And you reply as human cat based on the context file provided.'
                ' Your name is Gatito. Try to be short and concise.',
                self.rule_file
            ])
            self.logger.info(f"Response: {response.usage_metadata}")
            answer = response.text
        except Exception as e:
            self.logger.error(f"Error processing input: {e}")
        return answer
