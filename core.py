import random
import re
from nltk.chat.util import Chat, reflections
from db_handler import CatDB
from call_genai import GenAIClient
import click


class CatAI:
    def __init__(self, api_key, path_to_rule_file):
        self.db = CatDB()
        self.pairs = self.db.get_all_questions_answers()
        self.chatbot = Chat(self.pairs, reflections)
        self.chat_google = GenAIClient(api_key, path_to_rule_file)

    def respond(self, human_input):
        answer = self.check_db(human_input)
        random_number = random.randint(0, 1)
        if random_number == 0 and answer:
            return self.chatbot.respond(human_input)
        else:
            answer = self.chat_google.process_input(human_input)
            self.db.insert_question_answer(human_input, answer)
            self.chatbot._pairs.append((re.compile(human_input, re.IGNORECASE), answer))
        return answer
            
    def check_db(self, human_input):
        return self.db.get_answers(human_input)


@click.command()
@click.option('--context_file', '-c', required=True, help='Path to the context file.')
@click.option('--api_key', '-a', required=True, help='API key for CatAI.')
def chat_with_cat(context_file, api_key):
    """Starts a chat session with the cat AI."""
    cat_ai = CatAI(api_key=api_key, path_to_rule_file=context_file)
    
    while True:
        user_input = click.prompt("Say something to the cat", default="", show_default=False)
        if user_input.lower() == "exit":
            click.echo("Exiting chat...")
            break
        response = cat_ai.respond(user_input)
        click.echo(response)

if __name__ == "__main__":
    chat_with_cat()