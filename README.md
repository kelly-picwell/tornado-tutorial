# A Quick Tornado Demo

A quick demo of Tornado, with basic endpoints & testing.

## Establishing a virtualenv and dependencies

**To set up development environment:**
Make sure you have docker running.
This assumes you are using Docker for Mac.

```python
virtualenv env
pip install -r requires/development.txt
source ./bootstrap.sh
```

## Running the server

At any commit, you should be able to run:

```python tornado_tutorial/__init__.py```

## Running the tests

```nosetests -sxv```
