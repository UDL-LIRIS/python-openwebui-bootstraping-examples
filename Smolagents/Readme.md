# Running smolagents on top of Open WebUI

The [`smolagents.py`](./smolagents.py) python example illustrates how to use an LLM server by an Open WebUI server with the [smolagents](https://github.com/huggingface/smolagents) library.

## Setup your python virtual environment

```bash
cd `git rev-parse --show-toplevel`/Smolagents     # The directory of this file
python3.10 -m venv venv                           # Due to smolagents
source venv/bin/activate
pip install -r requirements.txt
```

## Parametrize your Open WebUI platform access

CUSTOMIZE" section. it the OPENWEBUI_SERVER_URL, API_KEY
Retrieve you api your API key from Settings ---> Account tab of the Open WebUI  interface. Then define an `API_KEY` environment variable with the retrieved value (recommended in order to avoid writing down, and possibly diffusing, the key) with

```bash
export API_KEY=<your-api-key>
```

Edit the `smolagents.py` code and customize it to define the following variables

- `OPENWEBUI_SERVER_URL` to the be URL of the Open WebUI server you wish to use
- `API_KEY` only if you didn't already defined it as environment variable  

## Running things

This boils down to running the following command

```bash
(venv) python openwebui_smolagents.py
```

## Troubleshooting

The [smolagents](https://github.com/huggingface/smolagents) python package uses the [`litellm`](https://docs.litellm.ai/) package (through the [`LiteLLMModel`](https://huggingface.co/docs/smolagents/v1.20.0/en/reference/models#smolagents.LiteLLMModel) class).
When troubleshooting the execution of `smolagents.py`, you might it find useful to turn on the [`litellm`](https://docs.litellm.ai/) library debug mode. For this, add the following two lines to the code

```python
import litellm
litellm._turn_on_debug()
```
