# Using LLM through Open-WebUI with Python: examples for a quick bootstrap<!-- omit from toc -->

## Table of contents<!-- omit from toc -->

- [Introduction](#introduction)
- [What you need to provide](#what-you-need-to-provide)
- [Method and hints to bootstrap your usage](#method-and-hints-to-bootstrap-your-usage)
  - [Define the `OPENWEBUI_SERVER_URL`](#define-the-openwebui_server_url)
  - [Configure the `API_KEY`](#configure-the-api_key)
  - [Define the model through `MODEL_ID`](#define-the-model-through-model_id)
  - [Define the API endpoint through `OPENWEBUI_API_ENDPOINT`](#define-the-api-endpoint-through-openwebui_api_endpoint)
- [Troubleshooting out of error messages](#troubleshooting-out-of-error-messages)
  - [405: Method Not Allowed](#405-method-not-allowed)
  - [Ollama\_chat Exception "Not authenticated"](#ollama_chat-exception-not-authenticated)
- [Running the examples](#running-the-examples)

## Introduction

Assume you have the following context:

- you have a remote access to an [Open WebUI deployment/server](https://github.com/open-webui/open-webui), through which you need to use on (or a set of) models/LLMs,
- you are a Python developer,
- the application your are working on leads/encourages you to use
  - a single LLM type (or a limited subset of LLMs)
  - a given python package/library e.g. [`litellm`](https://docs.litellm.ai/), [`smolagents`](https://github.com/huggingface/smolagents)...

In such a context you will have to align each of the above ressources in order to get things working.

The **purpose of this documentation/repository is to provide some hints/methodology to help you quickly bootstrap** your remote usage of the models.

## What you need to provide

The information that you need to provide/configure boils down to four parameters (python variables)

- `OPENWEBUI_SERVER_URL` that is the URL through which the [Open WebUI](https://github.com/open-webui/open-webui) server can be reached e.g. `https://some-server.organisation.org/`
- `OPENWEBUI_API_ENDPOINT` to be chose among [available Open WebUI endpoints](https://docs.openwebui.com/getting-started/api-endpoints/) e.g. `ollama/v1`
- `MODEL_ID` that designates the LLM or model e.g. `llama3:70b` or `qwen2.5-coder:32b-instruct` you need to use
- `API_KEY` that holds your credentials for using the designated Open WebUI server

that you will handle hover to the python library of your choice.

The difficulties arise from the fact that

- those variables are not independent e.g.
  - the name of model (`MODEL_ID`) might depend from the package you use. For example the [`litellm`](https://docs.litellm.ai/) library requires the model name to be prefixed with correct [provider name](https://docs.litellm.ai/docs/providers),
  - the endpoint (`OPENWEBUI_ENDPOINT`) might depend on the model (`MODEL_ID`). This is because deferent models expose different APIs,
- the `API_KEY` as well as the available models (`MODEL_ID`) depend on the Open WebUI server,
- the different layers (http API, authentication, the python library and eventually the model itself) error messages come mixed-up and are often a bit harsh/peculiar (at least for newbies),
- as always with servers, response delays and time out vary (although this documentation will leave you alone in the dark on that pitfall).

## Method and hints to bootstrap your usage

### Define the `OPENWEBUI_SERVER_URL`

This can be done at the shell level (most often when working with the [`curl` command](https://en.wikipedia.org/wiki/CURL)) and/or at the python level.
At the shell level you can e.g.

```bash
export OPENWEBUI_SERVER_URL=https://some-server.organisation.org # Adapt to your server
echo $OPENWEBUI_SERVER_URL      # Just to make sure
curl -X GET $OPENWEBUI_SERVER_URL
```

for which you should get some response in the `html` format.

:notebook: If you get an error message stating `Could not resolve host` or `connection error` in it, your probably should assert that `OPENWEBUI_SERVER_URL` is correct.

For example when working with the [litellm](./Litellm/) package, and when misconfiguring `OPENWEBUI_SERVER_URL` you will get a message of the form

```bash
litellm.exceptions.InternalServerError: [...] Exception - Connection error
```

### Configure the `API_KEY`

First, you have to [retrieve your API key](https://docs.openwebui.com/getting-started/api-endpoints/#authentication) through the web ui for which your admin should provide you with the proper credentials. Once retrieved you have to handle that key to your python code. In doing so, the general recommandation is to avoid writing the key value inside your application code (and afterwards, most often through a mistaken `git commit`, diffusing it). Instead, you might prefer to define environment variable that your application code will import at run time.

:warning: In the rest of this documentation, we will assume that the `API_KEY` environment variable is properly configured.

Assert that authentication is functional by accessing the server through its API with the command

```bash
echo $API_KEY     # Just to assert the key is properly defined
curl -X GET $OPENWEBUI_SERVER_URL'/ollama/api/ps' -H 'Authorization: BEARER '$API_KEY
```

If you get a response of the form `{"detail":"Not authenticated"}` then your `API_KEY` is not properly set. In which case correct your `API_KEY` until you obtain some JSON object as response to the command.

Note: in the above command the chosen endpoint `ollama/api/ps` does not mater much, and you can chose any endpoint provided by swagger at the `docs` endpoint (that is web browse `$OPENWEBUI_SERVER_URL/docs`) as far as this endpoint requires authentication.

### Define the model through `MODEL_ID`

First you should assert the availability of the model you wish to work with.
For this task you can either

- use your Open WebUI user interface (available models can be listed/chosen in a pull down menu),
- interrogate the server through the API e.g. with the command

    ```bash
    echo $OPENWEBUI_SERVER_URL  # Assert the server is defined
    echo $API_KEY               # Assert the key is properly defined
    curl -X GET $OPENWEBUI_SERVER_URL'/ollama/v1/models' -H 'Authorization: BEARER '$API_KEY
    ```

    that should return the list of the models installed on the server.

Then, select a model name among the list of available models, and configure the `MODEL_ID` variable (at the shell and/or python level) with e.g.

```bash
export MODEL_ID=llama3:70b
```

Asserting that the model is functional requires a proper `OPENWEBUI_API_ENDPOINT` definition. But if at some point you get an error message of the form `{"detail":"Model 'llamaaa3:70' was not found"}`, (model was misspelled with a trailing triple `aaa`) you should tune the `MODEL_ID` variable. <!-- cspell:ignore llamaaa -->

Note that for some python libraries like LiteL FIXME

### Define the API endpoint through `OPENWEBUI_API_ENDPOINT`

```bash
echo $OPENWEBUI_SERVER_URL  # Assert variables are defined
echo $API_KEY
echo $MODEL_ID

export OPENWEBUI_API_ENDPOINT=ollama/api/generate
curl -X 'POST' $OPENWEBUI_SERVER_URL'/'$OPENWEBUI_API_ENDPOINT -H 'Authorization: BEARER '$API_KEY -H 'Content-Type: application/json'  -d '{ "model": "'$MODEL_ID'", "prompt": "How are you today?"}'
```

If you get  an error code of `405` this generally indicates that the endpoint/route is not implemented.

## Troubleshooting out of error messages

### 405: Method Not Allowed

An error code of `405` this generally indicates that the endpoint/route is not implemented and thus you should probably change the value oe [`OPENWEBUI_API_ENDPOINT`](#define-the-api-endpoint-through-openwebui_api_endpoint).

Example of error: when using the [`litellm` example](./Litellm/Readme.md) and making a call of the form

```python
litellm.completion(model="https://some-server.organisation.org/ollama/v1/chat")
```

will trigger an http request of the form (because `litellm` plays some tricks/helpers under the hood)

```bash
"POST /ollama/v1/chat/chat/completions/ HTTP/1.1"
```

that will in turn trigger the following error

```bash
litellm.exceptions.APIError: [...] Error code: 405 - {'detail': 'Method Not Allowed'}
```

### Ollama_chat Exception "Not authenticated"

FIXME
FIXME

Following will fail with the error message:
  litellm.exceptions.APIConnectionError: Ollama_chatException - {"detail":"Not authenticated"}
MODEL_ID = "ollama_chat/qwen2.5-coder:32b-instruct-fp16"

## Running the examples

The different subdirectories hold self-contained examples. Feel free to experiment with the one at your convenience

- [LiteLLM](./Litellm)
- [Smolagents](./Smolagents)
- [Requests](./Requests/)
- FIXME
