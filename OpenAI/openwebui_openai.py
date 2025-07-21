import os
import sys

########## Configuring the context and defining the model
OPENWEBUI_SERVER_URL = "https://some-server.organisation.org/"  # TO BE EDITED

### The following variables should work by default
MODEL_ID = "qwen2.5:32b"
OPENWEBUI_API_ENDPOINT = "ollama/v1"
# the API_KEY imported from the environment variable as follows
try:
    API_KEY = os.environ["API_KEY"]
except KeyError:
    print("API_KEY environment variable was not set.")
    print("Exiting.")
    sys.exit(1)

### Using the model through the smolagents package
if __name__ == "__main__":
    from openai import OpenAI
    openai_client = OpenAI(base_url=OPENWEBUI_SERVER_URL+OPENWEBUI_API_ENDPOINT, 
                           api_key=API_KEY)

    openai_response = openai_client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {
                # System role allows to provide a context to the model
                "role": "system",
                "content": "Tu es un IA qui formule des réponse sous forme de poèmes.",
            },
            {
                # User role describes the user request
                "role": "user",
                "content": "Comment fonctionne le 49.3 en France ?",
            },
        ],
    )

    answer = openai_response.choices[0].message.content
    print(answer)
