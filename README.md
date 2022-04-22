## Data Analytics + Python Challenge

The challenge consists in obtain a series of cultural data from Argentina, normalize them and upload them to a database.

### How to run it:

1. Clone the repo:
```
$ git clone https://github.com/nazager/culture_data.git
```

2. Get into the project directory:
```
$ cd culture_data
```

3. Create a virtual environment:
```
$ python3 -m venv <env name>
```

4. Activate environment (bash):
```
$ source <env name>/bin/activate
```

5. Install dependencies:
```
$ pip3 install -r requirements.txt
``` 

### WARNING: A PostgreSQL database has to be running.

6. Fill the .env file with the corresponding data:
``` 
DB_USER=
DB_PASS=
DB_HOST=
DB_PORT=
DB_NAME=
``` 

7. Execute main.py:
``` 
$ cd src/
$ python3 main.py
``` 

### Done!
