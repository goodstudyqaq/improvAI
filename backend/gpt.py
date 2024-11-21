from openai import OpenAI


class ImproGPT:
    def __init__(self):
        self.client = OpenAI(
            api_key="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"
        )
        # load prompt from file
        with open("prompt", "r") as file:
            prompt = file.read()
        print(prompt)
        self.messages = [
            {"role": "system", "content": prompt}
        ]
        res = self._do_query("Start")
        print(res)

    def add_character(self, name, personality):
        res = f"[Character Define] {name}: {personality}"
        self.messages.append({"role": "user", "content": res})

    def add_dialogue(self, role, content):
        res = f"[Dialogues] {role}: {content}"
        self.messages.append({"role": "user", "content": res})

    def add_action(self, action):
        res = f"[Action] {action}"
        self.messages.append({"role": "user", "content": res})

    def add_environment(self, environment):
        res = f"[Environment] {environment}"
        self.messages.append({"role": "user", "content": res})

    def _do_query(self, query):
        print(query)
        chat_completion = self.client.chat.completions.create(
            messages=self.messages + [{"role": "user", "content": query}],
            model="gpt-3.5-turbo",
        )
        response = chat_completion.choices[0].message.content
        print("response", response)
        self.messages.append({"role": "assistant", "content": response})
        return response

    def query_dialogue(self, role):
        res = f"? [Dialogues] {role}"
        response = self._do_query(res)
        return response

    def query_action(self):
        res = f"? [Action]"
        response = self._do_query(res)
        return response

    def query_environment(self):
        res = f"? [Environment]"
        response = self._do_query(res)
        return response


impro_gpt = ImproGPT()
