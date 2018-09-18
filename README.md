# inkyphat-trains
Upcoming train departures using inkyphat eink display

## Installation

Register for a Darwin openLDBWS account. Put the API key you receive into a file called `secrets.py` like

```python
api_key = 'foo'
```

Install the pip requirements

```
> pip install -r requirements.txt
```

## Running

```
python3 trains.py STATION DESTINATION
```

where the two stations are represented by their three letter codes.