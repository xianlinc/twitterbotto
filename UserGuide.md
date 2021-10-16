# User Guide
## How to use the CLI

1. Clone the repo at this [link](https://github.com/mt-tai/twitterbotto)
2. Run the Parser.py file with python3 in a terminal
   1. eg. `$ python3 Parser.py <OPERATION> --handle <HANDLE>`

## Features
### check - List the new accounts the user is following, compared to the database version

Example:

`$ python3 Parser.py check --handle biyu`

### list - List the names all accounts stored in the database

Example:

`$ python3 Parser.py list`

### following - Retrieve who this user is following in the database

Example:

`$ python3 Parser.py following --handle ben_yorke`