# Running an `OpenAI` model on top of Open WebUI<!-- omit from toc -->

## Table of contents<!-- omit from toc -->

- [Introduction](#introduction)
- [Setup your python virtual environment](#setup-your-python-virtual-environment)
- [Parametrize your Open WebUI platform access](#parametrize-your-open-webui-platform-access)
- [Running things](#running-things)

## Introduction

The [`openwebui_openai.py`](./openwebui_openai.py) python example illustrates the usage of a model with the help of the [`openai`](https://github.com/openai/openai-python) library through an Open WebUI server.

## Setup your python virtual environment

Apply commands similar to

```bash
cd `git rev-parse --show-toplevel`/OpenAI
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Parametrize your Open WebUI platform access

[Retrieve you api key](../Readme.md#define-the-api_key) and define API_KEY environment variable with e.g.

```bash
export API_KEY=<your-api-key>
```

Edit the [`openwebui_openai.py`](./openwebui_openai.py) code and configure the `OPENWEBUI_SERVER_URL` to point to the Open WebUI server you wish to use.

## Running things

This boils down to running the following command

```bash
(venv) python openwebui_openai.py
```
