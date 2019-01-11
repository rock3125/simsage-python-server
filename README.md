# SimSage Python 3 Server example

written using Python 3.5 / 3.6

Small SimSage Python Server for HTTP/HTTPS access.

## installation
assuming you use a virtual environment with Python 3
```
pip install -r requirements
```
Don't forget to get your keys from SimSage 
visit https://simsage.nz/api.html for more details.

```
# replace these three IDs in server.py before starting!
securityId = "?"
organisationId = "?"
kbId = "?"
```

## run/serve using gunicorn on port 9000
```
gunicorn -k gevent --bind 0.0.0.0:9000 server:app
```

## quick sanity check
post some text to the service using curl
```
curl -X POST --header "Content-Type: application/json" --data '{"query": "what are you?", "customerId": "12345"}' http://localhost:9000/query
```
