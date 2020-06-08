#!/home/ericoff/env/bin/python3

import json
import cgi
import cgitb
import mimetypes
import os

cgitb.enable()

def main():
    form = cgi.FieldStorage()
    name  = form.getfirst("name", "world")
    data = say_hello(name)

    method = os.getenv("REQUEST_METHOD")
    data["method"] = method
    out(json.dumps(data, indent=4), ".json")

def say_hello(name):
    data = {"hello": name}
    return data

def out(data: str, mime: str):
    mime_out = mimetypes.types_map.get(mime, "text/plain")
    print("Content-Type: {}\n".format(mime_out))
    print(data)


if __name__ == "__main__":
    main()
