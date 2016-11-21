from .utils import record_audio

@app.task
def record_linein():
    record_audio()
