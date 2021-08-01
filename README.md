# HatBoard

<p>
    <a href="https://entysec.netlify.app">
        <img src="https://img.shields.io/badge/developer-EntySec-3572a5.svg">
    </a>
    <a href="https://github.com/EntySec/HatBoard">
        <img src="https://img.shields.io/badge/language-Python-3572a5.svg">
    </a>
    <a href="https://github.com/EntySec/HatBoard/stargazers">
        <img src="https://img.shields.io/github/stars/EntySec/HatBoard?color=yellow">
    </a>
</p>

HatBoard is a HatSploit Framework web interface for executing attacks, handling and manipulating sessions and traffic.

## Features

* Handling and displaying sessions via HatSploit Framework.
* Optimized to send commands to sessions and recieve output.
* Beautiful interface and powerful analytics tools like map or diagrams.

## Installation

```shell
pip3 install git+https://github.com/EntySec/HatBoard
```

## Basic usage

To use HatBoard just type `hatboard -h` in your terminal.

```
usage: hatboard [-h] [--create-user] [--address ADDRESS]

HatBoard is a HatSploit Framework web interface for executing attacks,
handling and manipulating sessions and traffic.

optional arguments:
  -h, --help         show this help message and exit
  --create-user      Create new user for HatBoard.
  --address ADDRESS  Run HatBoard on custom address.
```

First you need to create user to login to HatBoard web interface.

```
hatboard --create-user
```

Then you need to just type `hatboard` to make HatBoard to start its interface on port `8000`.

```
hatboard
```
