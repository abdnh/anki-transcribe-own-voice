import os
import sys
from concurrent.futures import Future

from aqt import gui_hooks, mw
from aqt.qt import *

sys.path.append(os.path.join(os.path.dirname(__file__), "vendor"))

from aqt.utils import showText, showWarning

from .consts import consts
from .transcription import transcribe


def on_reviewer_will_replay_recording(path: str) -> str:
    if not path:
        return path

    cid = mw.reviewer.card.id

    def on_done(future: Future) -> None:
        if mw.reviewer.card.id != cid:
            return
        try:
            transcription = future.result()
            if transcription:
                showText(transcription, title=consts.name, copyBtn=True)
        except Exception as exc:
            showWarning(str(exc), title=consts.name)

    future = transcribe(mw, path, on_done)
    if not future:
        showWarning(
            "The <a href='https://ankiweb.net/shared/info/411601849'>Speech Recognition add-on</a> is required",
            title=consts.name,
            textFormat="rich",
        )
    return path


gui_hooks.reviewer_will_replay_recording.append(on_reviewer_will_replay_recording)
