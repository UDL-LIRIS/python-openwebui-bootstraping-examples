# Running smolagents on top of Open WebUI<!-- omit from toc -->

## Table of contents<!-- omit from toc -->

- [Introduction](#introduction)
- [Setup your python virtual environment](#setup-your-python-virtual-environment)
- [Parametrize your Open WebUI platform access](#parametrize-your-open-webui-platform-access)
- [Running things](#running-things)
- [Troubleshooting](#troubleshooting)
- [Peculiarities/specificities of `smolagents`](#peculiaritiesspecificities-of-smolagents)

## Introduction

The [`smolagents.py`](./smolagents.py) python example illustrates how to use an LLM server by an Open WebUI server with the [smolagents](https://github.com/huggingface/smolagents) library.

## Setup your python virtual environment

```bash
cd `git rev-parse --show-toplevel`/Smolagents     # The directory of this file
python3.10 -m venv venv                           # Watch out: version constraint due to smolagents
source venv/bin/activate
pip install -r requirements.txt
```

## Parametrize your Open WebUI platform access

[Retrieve you api key](../Readme.md#define-the-api_key) and define API_KEY environment variable with e.g.

```bash
export API_KEY=<your-api-key>
```

Edit the [`smolagents.py`](./smolagents.py) code and configure the `OPENWEBUI_SERVER_URL` to point to the Open WebUI server you wish to use.

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

## Peculiarities/specificities of `smolagents`

Because `smolagents` uses `litellm` as underlying library (refer to [`smolagents.LiteLLMModel`](https://github.com/huggingface/smolagents/blob/main/src/smolagents/models.py#L1074)), `smolagents` "inherits" from [`litellm` peculiarities](../Litellm/Readme.md#peculiaritiesspecificities-of-litellm).