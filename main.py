import numpy as np
import tekore as tk
import time
import sys

import pyaudiowpatch as pyaudio
import time
import wave

import json
from vosk import KaldiRecognizer, Model

MODEL_PATH = "models/vosk-model-small-en-us-0.15"
CHUNK_SIZE = 2048  # Tamanho do buffer
SAMPLE_FORMAT = pyaudio.paInt16
SAMPLE_WIDTH = 2  # 16-bit = 2 bytes
DURATION = 30  # tempo total de execução em segundos
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



def stream_and_transcribe():
    print("[INFO] Carregando modelo Vosk...")
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, 44100)

    p = pyaudio.PyAudio()
    loopback = find_loopback_device()

    print(f"[INFO] Usando dispositivo: ({loopback['index']}) {loopback['name']}")
    stream = p.open(format=SAMPLE_FORMAT,
                    channels=loopback["maxInputChannels"],
                    rate=int(loopback["defaultSampleRate"]),
                    input=True,
                    input_device_index=loopback["index"],
                    frames_per_buffer=CHUNK_SIZE)

    print("[INFO] Iniciando transcrição ao vivo... (Ctrl+C para parar)")
    start_time = time.time()

    try:
        while time.time() - start_time < DURATION:
            data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)

            # Converte para mono, se necessário
            if loopback["maxInputChannels"] > 1:
                audio_data = np.mean(audio_data.reshape(-1, loopback["maxInputChannels"]), axis=1).astype(np.int16)

            if recognizer.AcceptWaveform(audio_data.tobytes()):
                result = json.loads(recognizer.Result())
                if result.get("text"):
                    print("[Transcrição]:", result["text"])
            else:
                partial = json.loads(recognizer.PartialResult()).get("partial")
                if partial:
                    print("[Parcial]:", partial)

    except KeyboardInterrupt:
        print("\n[INFO] Parado pelo usuário.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    if __name__ == "__main__":
        find_loopback_device()
        stream_and_transcribe()