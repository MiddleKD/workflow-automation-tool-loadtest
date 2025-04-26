import json
import sys


def decode_korean_text(json_obj, field_path):
    """
    json_obj: loaded json object
    field_path: list of keys, e.g., ["data", "outputs", "text"]
    """
    val = json_obj
    for key in field_path:
        val = val[key]
    return val


if __name__ == "__main__":
    data = json.load(sys.stdin)
    print(decode_korean_text(data, ["data", "outputs", "text"]))
