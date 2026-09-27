#!/usr/bin/env python3
"""
Tiny dependency-free RAG over Yetim Vakfi / COP31 knowledge.

- Retrieval: pure-Python TF-IDF + cosine similarity (no downloads, no token).
- Optional generation: HuggingFace Inference API if HF_TOKEN env var is set.

Usage:
    python rag.py "What is the sponsorship fee?"
    python rag.py "sponsorluk ücreti ne kadar?" --lang tr
    python rag.py "هزینه حمایت چقدر است؟" --lang fa
"""
import json
import math
import os
import re
from collections import Counter
from pathlib import Path

KB_PATH = Path(__file__).resolve().parent / "knowledge.json"

def tokenize(text):
    return re.findall(r"\w+", text.lower(), flags=re.UNICODE)

class Retriever:
    def __init__(self, docs):
        self.docs = docs
        df = Counter()
        self.tf = []
        for d in docs:
            toks = tokenize(d["title"] + " " + d["text"])
            c = Counter(toks)
            self.tf.append(c)
            for t in c:
                df[t] += 1
        n = len(docs)
        self.idf = {t: math.log((1 + n) / (1 + f)) + 1 for t, f in df.items()}

    def _vec(self, counter):
        return {t: c * self.idf.get(t, 0) for t, c in counter.items()}

    @staticmethod
    def _cos(a, b):
        dot = sum(a.get(t, 0) * b.get(t, 0) for t in set(a) | set(b))
        na = math.sqrt(sum(v * v for v in a.values())) or 1
        nb = math.sqrt(sum(v * v for v in b.values())) or 1
        return dot / (na * nb)

    def search(self, query, lang=None, top_k=1):
        qv = self._vec(Counter(tokenize(query)))
        scored = []
        for i, d in enumerate(self.docs):
            if lang and d.get("lang") != lang:
                continue
            s = self._cos(qv, self._vec(self.tf[i]))
            scored.append((s, d))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:top_k]

def load_kb():
    return json.loads(KB_PATH.read_text(encoding="utf-8"))

_RETRIEVER = None
def retriever():
    global _RETRIEVER
    if _RETRIEVER is None:
        _RETRIEVER = Retriever(load_kb())
    return _RETRIEVER

def ask(question, lang=None, top_k=1):
    """Return {'answer','title','score','id'} for the best match."""
    results = retriever().search(question, lang=lang, top_k=top_k)
    if not results:
        return {"answer": "", "title": "", "score": 0.0, "id": ""}
    s, d = results[0]
    return {"answer": d["text"], "title": d["title"], "score": round(s, 3), "id": d["id"]}

def generate(prompt, max_tokens=200):
    """Optional generative answer via HuggingFace Inference API. None if unavailable."""
    tok = os.environ.get("HF_TOKEN", "").strip()
    if not tok:
        return None
    try:
        from huggingface_hub import InferenceClient
    except ImportError:
        return "[huggingface_hub not installed: pip install huggingface_hub]"
    try:
        client = InferenceClient(token=tok)
        return client.text_generation(prompt, model="HuggingFaceH4/zephyr-7b-beta",
                                      max_new_tokens=max_tokens)
    except Exception as e:
        return f"[HF inference error: {e}]"

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("question")
    ap.add_argument("--lang", default=None)
    ap.add_argument("--generate", action="store_true")
    args = ap.parse_args()
    r = ask(args.question, lang=args.lang)
    print(f"[{r['id']}] {r['title']} (score {r['score']})")
    print(r["answer"])
    if args.generate:
        print("\n--- generative ---")
        print(generate(f"Answer briefly: {args.question}\nContext: {r['answer']}") or "[HF_TOKEN not set]")
