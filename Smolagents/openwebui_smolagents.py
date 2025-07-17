# A tiny AI example
# - using the smolagents library
# - running on top of an Open WebUI server

import os
import sys
from smolagents import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool

##### CUSTOMIZE section: adpat the following variables to your context
OPENWEBUI_SERVER_URL = "https://ollama-ui.pagoda.liris.cnrs.fr"
API_KEY = None  # Replace with your API key or define environment variable

#### Other meaningful variables
# The following variables are required in order to define and use an
# llm served by the Open WebUI server (and that you should NOT need to
# customize for this example to run).
MODEL_ID = "featherless_ai/qwen2.5-coder:32b-instruct-fp16"
API_END_POINT = OPENWEBUI_SERVER_URL + "/ollama/v1"
# Notes:
# - notice that API_END_POINT omits to mention "chat/completions". This is
#   because litellm is used as underlying library (refer to
#   smolagents.LiteLLMModel), and, by default, litellm will extend the provided
#   end point with "chat/completions"
# - API_END_POINT might need to be adapted if you change the MODEL_ID

if __name__ == "__main__":
    if API_KEY is None:
        try:
            API_KEY = os.environ["API_KEY"]
        except KeyError:
            print("API_KEY is missing:")
            print(" - either define the API_KEY variable in the code")
            print(" - or define the API_KEY environment variable")
            print("Exiting.")
            sys.exit(1)

    ###########
    # We are done with the definition of the variables required for the LLM
    # usage. The following code is the one of the original smolagents' example,
    # refer to
    # https://github.com/huggingface/smolagents/blob/main/examples/multi_llm_agent.py
    model = LiteLLMModel(
        model_id=MODEL_ID,
        api_base=API_END_POINT,
        api_key=API_KEY,
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
