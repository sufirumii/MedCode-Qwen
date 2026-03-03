
import sqlite3
from datasets import load_dataset

DB = "/kaggle/working/clinical_coding_agent/data/medconcepts.db"

SUBSETS = [
    "icd10cm_easy","icd10cm_medium","icd10cm_hard",
    "icd9cm_easy","icd9cm_medium","icd9cm_hard",
    "icd10proc_easy","icd10proc_medium","icd10proc_hard",
    "icd9proc_easy","icd9proc_medium","icd9proc_hard",
    "atc_easy","atc_medium","atc_hard",
]

con = sqlite3.connect(DB)
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS codes")
cur.execute('''
    CREATE TABLE codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer   TEXT NOT NULL,
        vocab    TEXT,
        level    TEXT
    )
''')
cur.execute("CREATE INDEX IF NOT EXISTS idx_vocab ON codes(vocab)")
con.commit()

total = 0
for subset in SUBSETS:
    vocab, level = subset.rsplit("_", 1)
    for split in ["dev", "test"]:
        print(f"  → {subset}/{split}…", end=" ", flush=True)
        ds = load_dataset("ofir408/MedConceptsQA", subset, split=split, streaming=True)
        buf = []
        for row in ds:
            buf.append((row["question"], row["answer"], vocab.upper(), level))
            if len(buf) >= 2000:
                cur.executemany("INSERT INTO codes(question,answer,vocab,level) VALUES(?,?,?,?)", buf)
                con.commit(); total += len(buf); buf = []
        if buf:
            cur.executemany("INSERT INTO codes(question,answer,vocab,level) VALUES(?,?,?,?)", buf)
            con.commit(); total += len(buf)
        print("done")

con.close()
print(f"\n✅ {total:,} rows indexed → {DB}")
