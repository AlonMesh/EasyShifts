# Handlers

Instead of using the `Server.py` file to handle requests, we can use the `handlers` directory to handle requests. This is a more modular approach to handling requests.

## How to use
1. Create a new file in the `handlers` directory (I created all of them).
2. Copy your handle function (and relevant helpers functions) from `Server.py` to the new file.
3. Import the new file in `Server.py` and use the handle function in the `handle` function in `Server.py`.