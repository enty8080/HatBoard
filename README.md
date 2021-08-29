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

<img width="1440" alt="129620228-da3bddf7-7d12-4b3b-a0b7-60a763eae939" src="https://user-images.githubusercontent.com/54115104/129756400-afc45088-d434-4db8-996f-21fcccddda00.png">

## Benefits

1. **Modern & User-friendly Interface**: HatBoard has modern, beautiful and user-friendly interface, so it is very easy to navigate.
2. **Synchronization with HatSploit Framework**: you can handle and manipulate sessions through HatBoard in real time.
3. **Pop-Up Terminal Emulator**: interact with sessions through HatBoard via user-friendly pop-up terminal emulator.
4. **Command & Control**: send commands directly to session and retrieve output and also close session if you need to.
5. **Sessions Lookup**: retrieve session location, country, city and etc. using only its IP address.

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
