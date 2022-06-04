# SERENE REST APIs

This set of APIs allow you to access the SERENE prediction model. To start the
server, after having installed all the dependencies (using `pipenv install`),
simply run:

```sh
pipenv run uvicorn main:app --reload
# or, in a deployment environment
pipenv run  gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --daemon
```

The APIs documentation is available at http://127.0.0.1:8000/docs (note: the IP
and port may differ for you, depending on the configuration with which the
server has been started).
