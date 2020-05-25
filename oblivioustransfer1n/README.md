# Oblivious transfer between two parties 1 out of n(100)
The server does not know the index the client chose and the client cannot know any message other than the one they asked for  
## Usage:
Install the dependencies, for python3
```
pip install pycryptodome pyzmq tqdm
```
Then, open two terminals  
On the first one run
```
python3 server.py
```
On the second one run
```
python3 client.py
```
In that order!  
The server's script prompts for the correct index to verify the results.
