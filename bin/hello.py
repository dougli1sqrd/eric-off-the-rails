#!/home/ericoff/env/bin/python3

import json
import cgi
import mimetypes

def main():
    data = {"hello": "world"}
    out(json.dumps(data, indent=4), ".json")

def out(data: str, mime: str):
    mime_out = mimetypes.types_map.get(mime, "text/plain")
    print("Content-Type: {}\n".format(mime_out))
    print(data)


if __name__ == "__main__":
    main()
