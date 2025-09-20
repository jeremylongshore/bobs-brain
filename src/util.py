from flask import jsonify

def ok(data): return (jsonify(data), 200)
def bad(msg, code=400): return (jsonify({"error": msg}), code)