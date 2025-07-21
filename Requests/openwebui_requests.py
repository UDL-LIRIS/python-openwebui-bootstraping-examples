import os
import sys

########## Configuring the context and defining the model
OPENWEBUI_SERVER_URL = "https://some-server.organisation.org/"  # TO BE EDITED

### The following variables should work by default
MODEL_ID = "llama3:70b"
OPENWEBUI_API_ENDPOINT = "ollama/v1/chat/completions"
# the API_KEY imported from the environment variable as follows
try:
    API_KEY = os.environ["API_KEY"]
except KeyError:
    print("API_KEY environment variable was not set.")
    print("Exiting.")
    sys.exit(1)


### Using the model directly through the API with the requests package
if __name__ == "__main__":

    import requests

    text_to_translate = (
        "Lo digo cada pocos dias y lo repito: TODO esto se "
        "pudo evitar si se hubiera parado el gamergate a tiempo"
    )
    source_language = "spanish"
    target_language = "english"

    # Prepare the prompt for translation
    prompt = f"Translate the following tweet from {source_language} to {target_language}: {text_to_translate}"

    # Create the request
    payload = {
        "model": MODEL_ID,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    # Post the request to the Ollama API
    response = requests.post(
        OPENWEBUI_SERVER_URL + OPENWEBUI_API_ENDPOINT, headers=headers, json=payload
    )

    # Check the response and extract content
    if response.status_code == 200:
        choices = response.json().get("choices", [])
        if choices:
            text_translated_to_english = choices[0]["message"]["content"].strip()
        else:
            raise Exception(f"Following response doesn't offer choices: {response}")
    else:
        raise Exception(f"Erreur API : {response.status_code} - {response.text}")

    # Display input and results
    print("Original tweet:", text_to_translate)
    print(text_translated_to_english)
