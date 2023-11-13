import time
from openai import OpenAI
from recruit_flow_ai.settings import env_settings

API_KEY = env_settings.api_key.get_secret_value()


class CVParser:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
        self.client = OpenAI(api_key=API_KEY)

        self.cv_file = self.client.files.create(
            file=open(pdf_file, "rb"), purpose="assistants"
        )

        self.assistant = self.client.beta.assistants.create(
            name="CV Parser",
            description=""" 
              You are a CV parser recruiter assistant. 
              You only return JSON objects with data being asked, NOTHING ELSE. 
              Valid response example: `{name: "John Doe"}`
              Unvalid response example: `json {"name": "John Doe"}`
              Unvalid response example: `here's you json: {"name": "John Doe"}`
              """,
            model="gpt-4-1106-preview",
            tools=[{"type": "retrieval"}],
        )

        self.thread = self.client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": """
                    Help me to get this candidate name.
                    Provide your response as a JSON object with the following schema:\n 
                        { 
                          "name": ${candidate_name},
                        }
                    ONLY RETURN VALID JSON OBJECT, NOTHING ELSE!
                  """,
                },
                {
                    "role": "user",
                    "content": "Here's the file. Your response: \n",
                    "file_ids": [self.cv_file.id],
                },
            ]
        )

    def parse_cv(self):
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id, assistant_id=self.assistant.id
        )

        # Wait for the run to complete
        # rn we have to poll manually until it's done
        while True:
            thread = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id, run_id=run.id
            )
            status = thread.status
            if status == "completed":
                break
            elif status in ["failed", "cancelled"]:
                raise Exception(f"Run failed or cancelled: {status}")
            else:
                time.sleep(2)
                continue

        # Retrieve parsed data from assistant
        messages = self.client.beta.threads.messages.list(thread_id=self.thread.id).data
        response = messages[0].content[0].text.value

        # Clean up and return parsed data
        self.client.beta.assistants.delete(assistant_id=self.assistant.id)
        self.client.files.delete(file_id=self.cv_file.id)

        return response
