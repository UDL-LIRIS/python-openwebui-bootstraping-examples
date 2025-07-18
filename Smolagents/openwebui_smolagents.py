# A tiny AI example
# - using the smolagents library
# - running on top of an Open WebUI server

import os
import sys
from smolagents import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool

########## Configuring the context and defining the model
OPENWEBUI_SERVER_URL = "https://ollama-ui.pagoda.liris.cnrs.fr/"  # TO BE EDITED

### The following variables should work by default
MODEL_ID = "featherless_ai/qwen2.5-coder:32b-instruct-fp16"
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

    # The following code is the one of the original smolagents' example, refer to
    # https://github.com/huggingface/smolagents/blob/main/examples/multi_llm_agent.py
    model = LiteLLMModel(
        model_id=MODEL_ID,
        api_key=API_KEY,
        api_base=OPENWEBUI_SERVER_URL + OPENWEBUI_API_ENDPOINT,
        stream_outputs=False,
    )
    search_agent = CodeAgent(
        model=model,
        tools=[DuckDuckGoSearchTool()],
        stream_outputs=True,
        return_full_result=True,
        # Refer to https://github.com/huggingface/smolagents/issues/640
        name="search_agent",
    )

    full_result = search_agent.run(
        "How many seconds would it take for a leopard at full speed to run through Pont des Arts?"
    )

    print(full_result)
