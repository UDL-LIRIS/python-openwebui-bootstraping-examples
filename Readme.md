# Using LLM through Open-WebUI with Python: examples for a quick bootstrap<!-- omit from toc -->

## Table of contents<!-- omit from toc -->

- [Introduction](#introduction)
- [What you need to provide](#what-you-need-to-provide)
- [Method and hints to bootstrap your usage](#method-and-hints-to-bootstrap-your-usage)
  - [Define the `OPENWEBUI_SERVER_URL`](#define-the-openwebui_server_url)
  - [Define the `API_KEY`](#define-the-api_key)
  - [Define the model through `MODEL_ID`](#define-the-model-through-model_id)
  - [Define the API endpoint through `OPENWEBUI_API_ENDPOINT`](#define-the-api-endpoint-through-openwebui_api_endpoint)
- [Run the examples and experiment code modifications](#run-the-examples-and-experiment-code-modifications)
- [Troubleshooting out of error messages](#troubleshooting-out-of-error-messages)
  - [Simple layer ordered table of errors (non exhaustive)](#simple-layer-ordered-table-of-errors-non-exhaustive)
  - [Example of 405 Method Not Allowed](#example-of-405-method-not-allowed)
  - [Example of Method Not Allowed (without a numbered error code)](#example-of-method-not-allowed-without-a-numbered-error-code)

## Introduction

Assume you have the following context:

- you have a remote access to an [Open WebUI deployment/server](https://github.com/open-webui/open-webui), through which you need to use on (or a set of) models/LLMs,
- you are a Python developer,
- the application you are working on encourages you to use some dedicated python package that
  - unifies/abstracts the usage of the great variety/diversity of models e.g. [`litellm`](https://docs.litellm.ai/)
  - provides added layer of specialization (for a specific sub-domain of model usage) e.g. [`smolagents`](https://github.com/huggingface/smolagents)

Then, in such a context, you will have to align each of the above ressources (or layers) in order to get things working.

The **purpose of this documentation/repository is to provide some hints/methodology to help you quickly bootstrap** your remote usage of the models.

## What you need to provide

The information that you need to provide/configure boils down to four parameters (that will end up as python variables)

- `OPENWEBUI_SERVER_URL` that is the URL through which the [Open WebUI](https://github.com/open-webui/open-webui) server can be reached e.g. `https://some-server.organisation.org/`
- `OPENWEBUI_API_ENDPOINT` that as to be chosen among [available Open WebUI endpoints](https://docs.openwebui.com/getting-started/api-endpoints/) e.g. `ollama/v1`
- `MODEL_ID` that designates model/LLM e.g. `llama3:70b` or `qwen2.5-coder:32b-instruct` you need to use
- `API_KEY` that holds your credentials for using the designated Open WebUI server

that you will handle hover to the python library of your choice.

The **difficulties arise** from the fact that

- those variables are not independent e.g.
  - the name of model (`MODEL_ID`) might depend from the package you use. For example the [`litellm`](https://docs.litellm.ai/) library requires the model name to be prefixed with a "correct" [provider name](https://docs.litellm.ai/docs/providers),
  - the endpoint (`OPENWEBUI_ENDPOINT`) might depend on the model (`MODEL_ID`). This is because different models expose different APIs,
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

:warning: for the following `curl` examples to work, do not add a trailing `/` to the `OPENWEBUI_SERVER_URL` definition

For example when working with the [litellm](./Litellm/) package, and when misconfiguring `OPENWEBUI_SERVER_URL` you will get a message of the form

```bash
litellm.exceptions.InternalServerError: [...] Exception - Connection error
```

### Define the `API_KEY`

First, you have to [retrieve your API key](https://docs.openwebui.com/getting-started/api-endpoints/#authentication) through the web ui for which your admin should provide you with the proper credentials. Once retrieved you have to handle that key to your python code. In doing so, the general recommandation is to avoid writing the key value inside your application code (and afterwards, most often through a mistaken `git commit`, diffusing it). Instead, you might prefer to define environment variable that your application code will import at run time.

:warning: In the rest of this documentation, we will assume that the `API_KEY` environment variable is properly configured.

Assert that authentication is functional by accessing the server through its API with the command

```bash
echo $API_KEY     # Just to assert the key is properly defined
curl -X GET $OPENWEBUI_SERVER_URL'/ollama/api/ps' -H 'Authorization: BEARER '$API_KEY
```

**Typical error message**: a response of the form `{"detail":"Not authenticated"}` generally indicates that your `API_KEY` is not properly set. In which case correct your `API_KEY` until you obtain some JSON object as response to the command.

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

Asserting that the model is functional requires a proper `OPENWEBUI_API_ENDPOINT` definition.

**Typical error message**: if you get an error message of the form

```bash
{"detail":"Model 'llamaaa3:70' was not found"}
```

(where the model was voluntarily misspelled with a trailing triple `aaa`) then you should probably tune the `MODEL_ID` variable. <!-- cspell:ignore llamaaa -->

### Define the API endpoint through `OPENWEBUI_API_ENDPOINT`

```bash
echo $OPENWEBUI_SERVER_URL  # Assert variables are defined
echo $API_KEY
echo $MODEL_ID

export OPENWEBUI_API_ENDPOINT=ollama/api/generate
curl -X 'POST' $OPENWEBUI_SERVER_URL'/'$OPENWEBUI_API_ENDPOINT -H 'Authorization: BEARER '$API_KEY -H 'Content-Type: application/json'  -d '{ "model": "'$MODEL_ID'", "prompt": "How are you today?"}'
```

**Typical error message**: an error code of `405` generally indicates that the endpoint/route is not implemented.

## Run the examples and experiment code modifications

The different subdirectories hold self-contained examples. Feel free to experiment with the one at your convenience

- [Requests](./Requests/): an http level model usage
- [OpenAI](./OpenAI/): using a `OpenAPI` API example
- [LiteLLM](./Litellm): using the `LiteLLM` API (using the OpenAI format) example
- [Smolagents](./Smolagents)

In particular, after running an example, don't hesitate to slightly alter its parameters in order to explore the space of error messages.

## Troubleshooting out of error messages

### Simple layer ordered table of errors (non exhaustive)

| Layer/Mechanism/Protocol | Typical error message | Possible reasons for failure | Possible actions |
| :-------------- | :-------------------- | :---------------- | :----------------- |
| IP | <ul><li>`Failed to connect to <your-server-name> port 443 after 75003 ms`</li><li>`Couldn't connect to server`</li><li>`Could not resolve host: ollama-ui.pagoda.liris.cnrs.fr`</li></ul> | IP connectivity, FireWall between client and server, server is down | Check your network, assert the server is not behind a FW...|
| SSL ([Secure Sockets Layer](https://en.wikipedia.org/wiki/SSL)) | `SSL certificate problem: unable to get local issuer certificate` | Unable to verify the SSL certificate chain | Contact the server admin? |
| DNS ([Domain Name Server](https://en.wikipedia.org/wiki/Domain_Name_System))        | <ul><li>`nodename nor servname provided, or not known`</li><li>`Connection error`</li></ul> | Erroneous (Open WebUI) server name | [`OPENWEBUI_SERVER_URL`](#define-the-openwebui_server_url) |
| Authentication/Access rights | `Error code: 401 [...] Your session has expired or the token is invalid.` | Erroneous credentials (key or token) | Modify [`API_KEY`](#define-the-api_key)|
| [API route/endpoint](https://danaepp.com/endpoints-vs-routes) | `Error code: 405 - [...] Method Not Allowed` | Erroneous endpoint | Modify [`OPENWEBUI_API_ENDPOINT`](#define-the-api-endpoint-through-openwebui_api_endpoint) |
| Model/LLM access | `403 - [...] Model not found` | Model not installed or ill-referenced | Assert the model is installed and/or modify [`MODEL_ID`](#define-the-model-through-model_id) |

### Example of 405 Method Not Allowed

If you modify the [`litellm` example](./Litellm/Readme.md) in order to make the following call

```python
litellm.completion(model="https://some-server.organisation.org/ollama/v1/chat")
```

then the execution will trigger (because `litellm` plays some tricks/helpers under the hood) an http request of the form

```bash
"POST /ollama/v1/chat/chat/completions/ HTTP/1.1"
```

that will in turn trigger the following error

```bash
litellm.exceptions.APIError: [...] Error code: 405 - {'detail': 'Method Not Allowed'}
```

### Example of Method Not Allowed (without a numbered error code)

Consider the [`Smolagents/openwebui_smolagents.py`](./Smolagents/openwebui_smolagents.py) python example where you modified the value of `MODEL_ID` from `MODEL_ID = "featherless_ai/qwen2.5-coder:32b-instruct-fp16` to be `ollama_chat/qwen2.5-coder:32b-instruct-fp16`, as suggested by [this litellm example usage](https://docs.litellm.ai/docs/providers/ollama#example-usage---tool-calling).

Then `openwebui_smolagents.py` will fail with the following message

```bash
litellm.APIConnectionError: Ollama_chatException - {"detail":"Method Not Allowed"}
```

which should not be confused we the [above described error `405: Method Not Allowed`](#example-of-405-method-not-allowed) (there is no mention of `405` error code).
A possible interpretation of this error is that the [`ollama API`](https://ollama.readthedocs.io/en/api/) does not recognize the model ?
