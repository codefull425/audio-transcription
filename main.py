from collections import deque

import numpy as np
import time

import pyaudiowpatch as pyaudio

import json
from vosk import KaldiRecognizer, Model
from captioner import CaptionAssembler

MODEL_PATH = "models/vosk-model-small-en-us-0.15"
CHUNK_SIZE = 2048  # Tamanho do buffer
SAMPLE_FORMAT = pyaudio.paInt16
SAMPLE_WIDTH = 2  # 16-bit = 2 bytes
DURATION = 60  # tempo total de execução em segundos


""" ------------------------------------------------------------------ """

MAX_LINES = 2                   # 1–2 linhas
MAX_CHARS_PER_LINE = 42         # ~42 por linha
MIN_CAPTION_SEC = 1.5
MAX_CAPTION_SEC = 6.0
LINE_BREAK_TOKENS = {",", ".", "!", "?", ":", ";"}
caps = CaptionAssembler("legenda.srt")
def find_loopback_device():
    if 1:
        with pyaudio.PyAudio() as p:
            """
            Create PyAudio instance via context manager.

            """
            try:
                # Get default WASAPI info
                wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
            except OSError:
                print("Looks like WASAPI is not available on the system. Exiting...")

                exit()

            # Get default WASAPI speakers
            default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])

            if not default_speakers["isLoopbackDevice"]:
                for loopback in p.get_loopback_device_info_generator():
                    """
                    Try to find loopback device with same name(and [Loopback suffix]).
                    Unfortunately, this is the most adequate way at the moment.
                    """
                    if default_speakers["name"] in loopback["name"]:
                        default_speakers = loopback
                        break
                else:
                    print(
                        "Default loopback output device not found.\n\nRun `python -m pyaudiowpatch` to check available devices.\nExiting...\n")

                    exit()

            print(f"Recording from: ({default_speakers['index']}){default_speakers['name']}")
            return default_speakers

def to_mono_int16(raw, nch):
    arr = np.frombuffer(raw, dtype=np.int16)
    if nch > 1:
        frames = arr.size // nch
        tmp = arr[:frames*nch].reshape(frames, nch).astype(np.int32)
        arr = tmp.mean(axis=1).astype(np.int16)
    return arr.tobytes()

def stream_and_transcribe():
    print("[INFO] Carregando modelo Vosk...")
    step_ms = 30
    loopback = find_loopback_device()
    sample_rate = int(loopback["defaultSampleRate"])
    frames_per_buffer = int(sample_rate * (step_ms / 1000.0))
    model = Model(MODEL_PATH)
    
    recognizer = KaldiRecognizer(model, sample_rate)
    window_size = int( sample_rate * (300/1000.0)) #buffer 300ms
    step_size = int( sample_rate * (150/1000.0)) #overlap 150ms
    recognizer.SetWords(True)
    channels=loopback["maxInputChannels"]
                          # chunk de ~30ms
      # ← habilita timestamps por PALAVRA


    p = pyaudio.PyAudio()

    print(f"[INFO] Usando dispositivo: ({loopback['index']}) {loopback['name']}")
    stream = p.open(format=SAMPLE_FORMAT,
                    channels=loopback["maxInputChannels"],
                    rate=sample_rate,
                    input=True,
                    input_device_index=loopback["index"],
                    frames_per_buffer=frames_per_buffer)

    ring = deque(maxlen=window_size)

    print("[INFO] Iniciando transcrição ao vivo... (Ctrl+C para parar)")
    start_time = time.time()

    try:
        while True:
            data = stream.read(frames_per_buffer, exception_on_overflow=False)
            mono = to_mono_int16(data, channels)

            if recognizer.AcceptWaveform(mono):
                result = json.loads(recognizer.Result())
                words = result.get("result", [])
                if words:
                    caps.add_words(words)

                if result.get("text"):
                    print("[Transcrição]:", result["text"])

            else:
                partial = json.loads(recognizer.PartialResult()).get("partial")

                if partial:
                    print("[Parcial]:", partial)
                        

    except KeyboardInterrupt:
        print("\n[INFO] Parado pelo usuário.")
    finally:
        try:
            final = json.loads(recognizer.FinalResult())
            words = final.get("result", [])
            if words:
                caps.add_words(words)
            if final.get("text"):
                print("[Transcrição]:", final["text"])
        except Exception:
            pass
        caps.finalize()
        stream.stop_stream()
        stream.close()
        p.terminate()



if __name__ == "__main__":
    stream_and_transcribe()