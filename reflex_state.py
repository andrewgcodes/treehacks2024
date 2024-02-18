import os
import requests
import json
import openai
import reflex as rx
import re
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")


def generate_recipe(prompt):
    url = "https://f40e171a-ade7-40c5-913b-84db8e5fd1f8.monsterapi.ai/generate"
    api_auth_token = #AUTH TOKEN

    headers = {
        "Authorization": f"Bearer {api_auth_token}",
        "Content-Type": "application/json"
    }

    data = {
        "prompt": f"You are an expert chef. You know about a lot of diverse cuisines. You write helpful tasty recipes.\n\n###Instruction: please think step by step and generate a detailed recipe for {prompt}\n\n###Response:",
        "stream": False,
        "max_tokens": 256,
        "n": 1,
        "best_of": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "repetition_penalty": 1,
        "temperature": 0.7,
        "top_p": 1,
        "top_k": -1,
        "min_p": 0,
        "use_beam_search": False,
        "length_penalty": 1,
        "early_stopping": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

    if response.status_code == 200:
        response_text = response.text
        start_str = "recipe name: "
        end_str = "token_counts"
        start_idx = response_text.find(start_str) + len(start_str)
        end_idx = response_text.find(end_str)
        recipe_text = response_text[start_idx:end_idx]
        recipe_text = recipe_text.replace("\\n", "\n").replace('\\"', '"')
        replaced_string = recipe_text.replace("\\\n", "\n")
        lines = replaced_string.split('\n')
        reversed_lines = list(reversed(lines))
        for line in reversed_lines:
            if any(char.isdigit() for char in line):
                index_to_remove = lines.index(line)
                lines = lines[:index_to_remove]
                break
        cleaned_text = '\n'.join(lines)
        final_string = cleaned_text.replace("\\\n", "\n")
        print(final_string)
        return final_string
    else:
        print(f"Error: {response.status_code}, Message: {response.text}")
        return "Error"
    
def get_access_token():
    """
    :return: access_token
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": BAIDU_API_KEY,
        "client_secret": BAIDU_SECRET_KEY,
    }
    return str(requests.post(url, params=params).json().get("access_token"))


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str


DEFAULT_CHATS = {
    "Recipe Wizard": [],
}


class State(rx.State):
    """The app state."""

    chats: dict[str, list[QA]] = DEFAULT_CHATS

    current_chat = "Recipe Wizard"

    question: str

    processing: bool = False

    new_chat_name: str = ""

    drawer_open: bool = False

    modal_open: bool = False

    api_type: str = "baidu" if BAIDU_API_KEY else "openai"

    dialog_open: bool = False

    def create_chat(self):
        """Create a new chat."""
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []

        self.modal_open = False

    def toggle_modal(self):
        """Toggle the new chat modal."""
        self.modal_open = not self.modal_open

    def toggle_drawer(self):
        """Toggle the drawer."""
        self.drawer_open = not self.drawer_open

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]
        self.toggle_drawer()

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name
        self.toggle_drawer()

    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())
    async def process_question(self, form_data: dict[str, str]):
        question = form_data["question"]

        if question == "":
            return
        self.dialog_open = True

        if question.lower().startswith("make me"):
            food_item = question[21:].strip()
            
            recipe = generate_recipe(food_item)
            qa = QA(question=question, answer=recipe)
            self.chats[self.current_chat].append(qa)
            self.chats = self.chats
            return
        if question.lower().startswith("get me"):
            food_item = question[7:].strip()
            
            response = requests.post(
                "https://eofrhbmhilleja4.m.pipedream.net",
                headers={"Content-Type": "application/json"},
                data=json.dumps({"desiredFood": food_item}),
            )

            
            data = response.json()
            recipe = data["generated_recipe"]
            ingredients = data["ingredients"]
            shopping_list_data = data["instacart_and_shopping_list"]["original_shopping_list"]

            qa_recipe = QA(question=question, answer=recipe)
            qa_ingredients = QA(question=question, answer=ingredients)
            self.chats[self.current_chat].extend([qa_recipe, qa_ingredients])

            for store, items in shopping_list_data.items():
                store_message = f"Store: {store},\n"
                for item in items:
                    store_message += f" [Item: {item['title']}, Price: {item['price']}...]\n"
                qa_store = QA(question=question, answer=store_message)
                self.chats[self.current_chat].append(qa_store)

            self.chats = self.chats
            return
        if self.api_type == "openai":
            model = self.openai_process_question

        async for value in model(question):
            yield value
        self.dialog_open = False

    

    async def openai_process_question(self, question: str):
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """

        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Build the messages.
        messages = [
            {"role": "system", "content": "You are a friendly expert nutritionist and dietitian."}
        ]
        for qa in self.chats[self.current_chat]:
            messages.append({"role": "user", "content": "You are an expert in nutrition and food" + qa.question})
            messages.append({"role": "assistant", "content": qa.answer})

        # Remove the last mock answer.
        messages = messages[:-1]

        # Start a new session to answer the question.
        session = openai.ChatCompletion.create(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            messages=messages,
            stream=True,
        )

        # Stream the results, yielding after every word.
        for item in session:
            if hasattr(item.choices[0].delta, "content"):
                answer_text = item.choices[0].delta.content
                self.chats[self.current_chat][-1].answer += answer_text
                self.chats = self.chats
                yield

        # Toggle the processing flag.
        self.processing = False

  
