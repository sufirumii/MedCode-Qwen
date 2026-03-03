
import re, sqlite3, torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

DB_PATH  = "/kaggle/working/clinical_coding_agent/data/medconcepts.db"
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"

print("⏳ Loading Qwen2.5-7B-Instruct (4-bit quantised)…")
_bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
_tok = AutoTokenizer.from_pretrained(MODEL_ID)
_mdl = AutoModelForCausalLM.from_pretrained(MODEL_ID, quantization_config=_bnb, device_map="auto")
print("✅ Model ready")

def _db(): return sqlite3.connect(DB_PATH)

def _lookup(query: str) -> list:
    con = _db(); cur = con.cursor(); rows = []
    
    # 1. Try matching question column directly (catches full question strings)
    cur.execute(
        "SELECT question, answer, vocab, level FROM codes WHERE question LIKE ? LIMIT 5",
        (f"%{query[:60]}%",)
    )
    rows = cur.fetchall()
    if rows:
        con.close(); return rows

    # 2. Extract any code-like tokens and search
    tokens = re.findall(r"[A-Z][0-9]{2,}[A-Z0-9]*|[0-9]{2,3}\.[0-9]+|[A-Z][0-9]{2}[A-Z]{2}[0-9]{2}", query.upper())
    for t in tokens[:4]:
        cur.execute(
            "SELECT question, answer, vocab, level FROM codes WHERE question LIKE ? LIMIT 5",
            (f"%{t}%",)
        )
        rows += cur.fetchall()
    if rows:
        con.close(); return rows[:5]

    # 3. Keyword fallback on answer column
    words = [w for w in query.split() if len(w) > 4][:4]
    for w in words:
        cur.execute(
            "SELECT question, answer, vocab, level FROM codes WHERE answer LIKE ? LIMIT 3",
            (f"%{w}%",)
        )
        rows += cur.fetchall()

    con.close()
    return rows[:5]

def _generate(prompt: str, max_new: int = 350) -> str:
    inputs = _tok.apply_chat_template(
        [{"role": "user", "content": prompt}],
        add_generation_prompt=True, tokenize=True,
        return_dict=True, return_tensors="pt"
    ).to(_mdl.device)
    with torch.no_grad():
        out = _mdl.generate(**inputs, max_new_tokens=max_new, temperature=0.2, do_sample=True)
    return _tok.decode(out[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True).strip()

def answer(user_query: str) -> dict:
    hits = _lookup(user_query)
    if hits:
        ctx = "\n".join(f"[{r[2]}|{r[3]}] Q: {r[0]}\nA: {r[1]}" for r in hits)
        prompt = (
            f"You are a clinical coding expert.\n"
            f"Retrieved records:\n{ctx}\n\n"
            f"User question: {user_query}\n\n"
            f"The answer is directly in the retrieved records above. State it clearly and concisely."
        )
        source = "Corrective-RAG + Qwen2.5-7B"
    else:
        prompt = (
            f"You are a clinical coding expert in ICD-10-CM, ICD-9-CM, "
            f"ICD-10-PROC, ICD-9-PROC and ATC drug codes.\n"
            f"Answer accurately: {user_query}"
        )
        source = "Qwen2.5-7B (no DB match)"

    return {
        "answer": _generate(prompt),
        "source": source,
        "hits": [{"question":r[0],"answer":r[1],"vocab":r[2],"level":r[3]} for r in hits]
    }
