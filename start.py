import src


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)
