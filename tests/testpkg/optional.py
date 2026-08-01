try:
    import ujson as json
except ImportError:
    import json

print(json.dumps({"a": 1}))