import os

########## Configuring the context and defining the model
OPENWEBUI_SERVER_URL = "https://some-server.organisation.org/"  # TO BE EDITED

### The following variables should work by default
MODEL_ID = "featherless_ai/qwen2.5-coder:32b-instruct-fp16"
OPENWEBUI_API_ENDPOINT = "ollama/v1/"
# the API_KEY imported from the environment variable as follows
try:
    API_KEY = os.environ["API_KEY"]
except KeyError:
    print("API_KEY environment variable was not set.")
    print("Exiting.")
    os.exit(1)

### Using the model through the Litellm package
if __name__ == "__main__":
    from litellm import completion

    response = completion(
        model=MODEL_ID,
        api_key=API_KEY,
        api_base=OPENWEBUI_SERVER_URL + OPENWEBUI_API_ENDPOINT,
        messages=[{"content": "Hello, how are you?", "role": "user"}],
    )
    print(response["choices"][0]["message"]["content"])
