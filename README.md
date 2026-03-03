# 🏥 Clinical Coding AI Agent

Corrective-RAG over 800 k+ medical codes powered by **Qwen/Qwen2.5-7B-Instruct**.

## Folder structure
```
clinical_coding_agent/
├── setup.py           # run ONCE — writes all files
├── build_db.py        # run ONCE — indexes the dataset
├── app.py             # Gradio UI — launch this
├── requirements.txt
├── backend/
│   └── agent.py       # Corrective-RAG + LLM logic
├── data/
│   └── medconcepts.db # SQLite index (built by build_db.py)
└── frontend/
    └── index.html     # Standalone HTML UI
```

## Quickstart (Kaggle)
```bash
pip install -r requirements.txt
python build_db.py        # ~2 min, one-time
python app.py             # opens Gradio + public share URL
```

## How it works
1. User asks a question containing a medical code or keyword.
2. SQLite lookup retrieves exact/fuzzy matches instantly.
3. Qwen2.5-7B-Instruct reasons over the retrieved records and answers.
4. If no DB match, falls back to pure LLM knowledge.

## Covered vocabularies
| Code system | Category |
|---|---|
| ICD-10-CM | Diagnosis |
| ICD-9-CM  | Diagnosis |
| ICD-10-PROC | Procedure |
| ICD-9-PROC  | Procedure |
| ATC | Drugs |
