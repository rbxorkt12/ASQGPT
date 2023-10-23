import os
import openai
import sys
from functions import read_file, check_completion
from metagpt.config import CONFIG


openai.api_key = CONFIG.openai_api_key


class Boss:
    def __init__(self, model_type="gpt-4"):
        # Reads the boss' prompt.
        boss_prompt = read_file("boss_prompt.md")
        # Sets the model that will be powering the boss.
        self.model_type = model_type
        # Initializes the first context to be delivered to the language model.
        self.messages = [{"role": "system", "content": boss_prompt}]

    def greetings(self):
        welcome_text = read_file("welcome.txt")
        print(welcome_text)

    def listen(self):
        """
        The agent waits and listens to the user's message.
        :return:
        """
        try:
            message = input("User: ").strip()
            if not message:
                self.listen()
            else:
                self.messages.append({"role": "user", "content": message})
        except KeyboardInterrupt:
            print("\nASQ: Good talk! I'll see you later :)")
            sys.exit(1)

    def speak(self):
        """
        The agent responds to the user's message.
        :return:
        """
        # Receive a chat completion object from the OpenAI API.
        response = openai.ChatCompletion.create(
            model=self.model_type,
            messages=self.messages,
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        response_message = response["choices"][0]["message"]
        # Show the boss' response to the user.
        print(f'ASQ: {response_message["content"]}')
        check_completion("[GOAL]", response_message["content"])
        # Add the boss' message to the context.
        self.messages.append(response_message)

    def conversation(self):
        """
        The agent has a conversation with the user.
        :return:
        """
        self.listen()
        print("---")
        self.speak()
        self.conversation()

    def run(self):
        """
        The agent starts to have a conversation.
        :return:
        """
        self.greetings()
        self.conversation()
