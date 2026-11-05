# vial

Tool for visualizing numeric entries, checking if they are outside the normal range and how much they changed since the last entry.


## Usage

To show an overview of all fields in the Nth last entry:

```sh
vial -f data.json -d defs.json list    # list the last entry
vial -f data.json -d defs.json list 2  # list the 2nd last entry
```

To plot any number of fields using matplotlib:

```sh
vial -f data.json -d defs.json plot key1       # plot "key1"
vial -f data.json -d defs.json plot key1 key2  # plot "key1" and "key2"
```


## Data Specs

Data entries are stored in a json list.

```json
[
    {
        "date": "2026-10-18",
        "note": "Very cool entry",
        "data": { "key1": 42.0, "key2": 0.0 }
    },
    {
        "date": "2026-11-05",
        "note": "very cool entry",
        "data": { "key1": 69.0, "key2": 0.1 }
    }
]
```

Definitions are stored in a json dictionary.

```json
{
    "key1": {
        "desc": "Key Name",
        "min": 32.0,
        "max": 69.0,
        "unit": "m/s"
    },
    "key2": {
        "desc": "Key Name",
        "min": 0.0,
        "max": 1.0,
        "unit": "m/s"
    }
}
```
