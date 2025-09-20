# 🎙️ Live Caption Generator (Vosk + PyAudio + WASAPI)

This project is a **Python** application that captures the computer's audio (via **WASAPI loopback** on Windows) and automatically generates a **SRT subtitle file** in real-time using **Vosk Speech Recognition**.

---

## 🚀 Features
- Captures the **audio playing on your speakers** (music, videos, meetings, etc.).
- Real-time transcription using **Vosk ASR**.
- Automatically segments text into **readable subtitle blocks**:
  - Max. 2 lines per subtitle.
  - Up to 42 characters per line.
  - Minimum duration: 1.5s | Maximum duration: 6s.
- Exports to **`.srt`** file, compatible with any video player.

---

## 📦 Requirements
- Python **3.9+**
- Python libraries:
  ```bash
  pip install vosk pyaudiowpatch numpy
  ```
- Vosk speech recognition model (English or Portuguese).  
  Download at: [Vosk Models](https://alphacephei.com/vosk/models)
  You can choose for any model at your preference

  Examples:
  - English: `vosk-model-small-en-us-0.15`
  - Portuguese: `vosk-model-small-pt-0.3`

---

## 📂 Project Structure
```
.
├── legenda.py       # Main script
├── README.md        # This file
└── models/
    └── vosk-model-small-pt-0.3/   # Downloaded model folder
```

---

## ▶️ How to use

1. **Clone the repository** or copy the files.
   ```bash
   git clone https://github.com/codefull425/audio-transcription.git
   cd audio-transcription
   ```

2. **Install dependencies**
   ```bash
   pip install vosk pyaudiowpatch numpy
   ```

3. **Download a Vosk model** and place it inside the `models/` folder.
   - Adjust the model path in the code (`MODEL_PATH`).

4. **Run the script**
   ```bash
   python legenda.py
   ```

5. The program:
   - Detects the loopback audio device.
   - Transcribes the audio in real time.
   - Automatically saves it into **`legenda.srt`**.

6. To stop, press **Ctrl + C**.  
   The `.srt` file will be ready in the project directory.

---

## 📑 Example output (`legenda.srt`)
```
1
00:00:01,000 --> 00:00:03,500
this is a sample subtitle

2
00:00:04,000 --> 00:00:06,000
generated automatically
```

---

## ⚠️ Notes
- Works only on **Windows** (uses WASAPI loopback).  
- If the audio is in Portuguese, configure:
  ```python
  MODEL_PATH = "models/vosk-model-small-pt-0.3"
  ```
- Quality depends on the chosen model:  
  - "small" models → faster, less accurate.  
  - "large" models → heavier, more accurate.

---

## 🛠️ Technologies
- [Python](https://www.python.org/)
- [Vosk API](https://alphacephei.com/vosk/)
- [PyAudioWpatch](https://github.com/intxcc/pyaudio_portaudio)

---

## 📜 License
This project is open-source and can be freely used for educational and research purposes.

---

# 🎙️ Gerador de Legendas em Tempo Real (Vosk + PyAudio + WASAPI)

Este projeto é uma aplicação em **Python** que captura o áudio do computador (via **WASAPI loopback** no Windows) e gera automaticamente um arquivo de legendas no formato **SRT** em tempo real, utilizando o **Vosk Speech Recognition**.

---

## 🚀 Funcionalidades
- Captura o **áudio que toca nos alto-falantes** do PC (músicas, vídeos, reuniões, etc.).
- Transcreve em tempo real utilizando **Vosk ASR**.
- Segmenta automaticamente o texto em **blocos de legenda legíveis**:
  - Máx. 2 linhas por legenda.
  - Até 42 caracteres por linha.
  - Duração mínima: 1,5s | máxima: 6s.
- Exporta para arquivo **`.srt`** compatível com qualquer player de vídeo.

---

## 📦 Requisitos
- Python **3.9+**
- Bibliotecas Python:
  ```bash
  pip install vosk pyaudiowpatch numpy
  ```
- Modelo Vosk de reconhecimento de voz (ex. inglês ou português).  
  Baixe em: [Modelos Vosk](https://alphacephei.com/vosk/models)
  Voce pode escolher o modelo da sua preferencia

  Exemplos:
  - Inglês: `vosk-model-small-en-us-0.15`
  - Português: `vosk-model-small-pt-0.3`

---

## 📂 Estrutura do Projeto
```
.
├── legenda.py       # Script principal
├── README.md        # Este arquivo
└── models/
    └── vosk-model-small-pt-0.3/   # Pasta com modelo baixado
```

---

## ▶️ Como usar

1. **Clone o repositório** ou copie os arquivos.
   ```bash
   git clone https://github.com/codefull425/audio-transcription.git
   cd audio-transcription
   ```

2. **Instale as dependências**
   ```bash
   pip install vosk pyaudiowpatch numpy
   ```

3. **Baixe um modelo do Vosk** e coloque na pasta `models/`.
   - Ajuste o caminho do modelo no código (`MODEL_PATH`).

4. **Execute o script**
   ```bash
   python legenda.py
   ```

5. O programa:
   - Detecta o dispositivo de áudio loopback.
   - Transcreve o áudio em tempo real.
   - Salva automaticamente em **`legenda.srt`**.

6. Para parar, pressione **Ctrl + C**.  
   O arquivo `.srt` estará pronto no diretório do projeto.

---

## 📑 Exemplo de saída (`legenda.srt`)
```
1
00:00:01,000 --> 00:00:03,500
este é um exemplo de legenda

2
00:00:04,000 --> 00:00:06,000
gerada automaticamente
```

---

## ⚠️ Observações
- Funciona apenas no **Windows** (usa WASAPI loopback).  
- Se o áudio for em português, configure:
  ```python
  MODEL_PATH = "models/vosk-model-small-pt-0.3"
  ```
- A qualidade depende do modelo escolhido:  
  - Modelos "small" → mais rápidos, menos precisos.  
  - Modelos "large" → mais pesados, maior acurácia.

---

## 🛠️ Tecnologias
- [Python](https://www.python.org/)
- [Vosk API](https://alphacephei.com/vosk/)
- [PyAudioWpatch](https://github.com/intxcc/pyaudio_portaudio)

---

## 📜 Licença
Este projeto é open-source e pode ser usado livremente para fins educacionais e de pesquisa.
