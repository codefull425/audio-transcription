def format_srt_time(t):
    h = int(t // 3600); 
    t -= h * 3600
    m = int(t // 60);   
    t -= m * 60
    s = int(t);         
    ms = int(round((t - s) * 1000))
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def wrap_lines(text, max_chars=42, max_lines=2):
    words = text.split()
    lines, cur = [], []
    for w in words:
        cur_len = sum(len(x) for x in cur) + max(0, len(cur) - 1)
        if cur and cur_len + 1 + len(w) > max_chars:
            lines.append(" ".join(cur)); cur = [w]
        else:
            cur.append(w)
    if cur: lines.append(" ".join(cur))
    while len(lines) > max_lines:
        last = lines.pop()
        lines[-1] = (lines[-1] + " " + last).strip()
    return "\n".join(lines)

class CaptionAssembler:
    def __init__(self, srt_path, max_lines=2, max_chars=42,
                 min_sec=1.5, max_sec=6.0,
                 break_tokens={",", ".", "!", "?", ":", ";"}):

        self.srt_path = srt_path
        self.max_lines = max_lines
        self.max_chars = max_chars
        self.min_sec = min_sec
        self.max_sec = max_sec
        self.break_tokens = break_tokens

        self.idx = 1
        self.sf = open(self.srt_path, "w", encoding="utf-8")
        self.reset()

    def reset(self):
        self.words = []   # lista de (word, start, end)
        self.start = None
        self.end = None

    def _flush(self):
        if not self.words: return
        text = " ".join(w for w, _, _ in self.words).strip()
        if not text: self.reset(); return

        body = wrap_lines(text, self.max_chars, self.max_lines)
        s, e = self.start, self.end

        # escreve no .srt
        self.sf.write(f"{self.idx}\n")
        self.sf.write(f"{format_srt_time(s)} --> {format_srt_time(e)}\n")
        self.sf.write(body + "\n\n")

        self.idx += 1
        self.reset()

    def add_words(self, vosk_words):
        for w in vosk_words:
            word = w.get("word", "").strip()
            ws = float(w.get("start", 0.0))
            we = float(w.get("end", ws))
            if not word: continue

            if self.start is None: self.start = ws
            self.end = we
            self.words.append((word, ws, we))

            dur = self.end - self.start
            txt = " ".join(x[0] for x in self.words)

            if dur >= self.max_sec:
                self._flush()
            elif dur >= self.min_sec and (word in self.break_tokens or len(txt) > self.max_lines * self.max_chars):
                self._flush()

    def finalize(self):
        self._flush()
        self.sf.flush(); self.sf.close()