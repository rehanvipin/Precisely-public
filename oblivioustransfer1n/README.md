## Oblivious transfer between two parties 1 out of n
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
After the programs have finished, you can verify the result with the server script's prompt
