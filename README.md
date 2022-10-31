# Flask Survey

A Flask app for completing customer surveys. Uses Flask sessions to persist user data for browser session. Redirects user to correct chronological question with a flash message.

## Developer Environment Setup

This project requires Python 3.8 or later.

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

To start a server:
`flask run`

In your browser, open [http://127.0.0.1:5000](http://127.0.0.1:5000) 

For Mac users:
`flask run -p 5001`

In your browser, open [http://127.0.0.1:5001](http://127.0.0.1:5001)