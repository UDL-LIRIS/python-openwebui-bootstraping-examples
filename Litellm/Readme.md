# Running `litellm` on top of Open WebUI<!-- omit from toc -->

## Table of contents<!-- omit from toc -->

- [Introduction](#introduction)
- [Setup your python virtual environment](#setup-your-python-virtual-environment)
- [Parametrize your Open WebUI platform access](#parametrize-your-open-webui-platform-access)
- [Running things](#running-things)
- [Peculiarities/specificities of Litellm](#peculiaritiesspecificities-of-litellm)
  - [The model name must integrate a known provider](#the-model-name-must-integrate-a-known-provider)
  - [Misspelling a model name](#misspelling-a-model-name)
  - [A "simplified" API endpoint](#a-simplified-api-endpoint)

## Introduction

The [`openwebui_litellm.py`](./openwebui_litellm.py) python example illustrates the usage of a model with the help of the [`litellm`](https://docs.litellm.ai/) library through an Open WebUI server.

## Setup your python virtual environment

Apply commands similar to

```bash
cd `git rev-parse --show-toplevel`/Litellm
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Parametrize your Open WebUI platform access

[Retrieve you api key](../Readme.md#define-the-api_key) and define API_KEY environment variable with e.g.

```bash
export API_KEY=<your-api-key>
```

Edit the [`openwebui_litellm.py`](./openwebui_litellm.py) code and configure the `OPENWEBUI_SERVER_URL` to point to the Open WebUI server you wish to use.

## Running things

This boils down to running the following command

```bash
(venv) python openwebui_litellm.py
```

## Peculiarities/specificities of Litellm

### The model name must integrate a known provider

The [`litellm`](https://docs.litellm.ai/) library seems to expect a model name (`MODEL_ID`) that is prefixed with
a [well known (to the library) provider name](https://docs.litellm.ai/docs/providers) e.g. `huggingface/starcoder`.

For example, if you were to modify [`openwebui_litellm.py`](./openwebui_litellm.py) in order to set

```python
MODEL_ID = "qwen2.5-coder:32b-instruct-fp16"
```

then running [`openwebui_litellm.py`](./openwebui_litellm.py) 
will fail with the error message:

```bash
litellm.exceptions.BadRequestError: LLM Provider NOT provided. Pass in the LLM provider you are trying to call. [...] Pass model as E.g. For 'Huggingface' inference endpoints pass in completion(model='huggingface/starcoder',..)
```

Similarly, if your try guessing the provider (out of misguided google responses) by setting

```python
MODEL_ID = "Qwen/qwen2.5-coder:32b-instruct-fp16"
```

your will get the above error message. This is because `Qwen` or `qwen` are not a providers that is recognized by the `litellm` library

Trying to infer the provider out of the [model names available on your Open WebUI server](../Readme.md#define-the-model-through-model_id) is best done by searching within the [litellm's supported list of providers](https://docs.litellm.ai/docs/providers/featherless_ai).

### Misspelling a model name

Notice that even when the provider is correct (that is `featherless_ai`) is our example, and if you were to modify [`openwebui_litellm.py`](./openwebui_litellm.py) in order to set

```python
MODEL_ID = "featherless_ai/qwen/qwen2.5-coder:32b-instruct-fp16"
```

then you should get error messages of the form

```bash
litellm.exceptions.APIError: [...] Error code: 403 - {'detail': 'Model not found'}
```

### A "simplified" API endpoint

Notice that the [configured value of the `OPENWEBUI_API_ENDPOINT`] (within [`openwebui_litellm.py`](./openwebui_litellm.py)) is reduced to be `ollama/v1/`
when one could expect `ollama/v1/chat/completions`. This is because, by default, `litellm` will extend the provided endpoint (the `api_base` argument of the `litellm.completion()` function) with `chat/completions`.

If we were to modify [`openwebui_litellm.py`](./openwebui_litellm.py) to define

```python
OPENWEBUI_API_ENDPOINT = "ollama/v1/chat/completions"
```

we would get a [`405 [...] Method Not Allowed`](../Readme.md#405-method-not-allowed) error.