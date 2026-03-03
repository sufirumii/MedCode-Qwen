# MedCode-Qwen

Retrieval-augmented clinical coding agent over 819,832 ICD and ATC medical records, powered by Qwen/Qwen2.5-7B-Instruct.

---

### Demo

<img width="1920" height="900" alt="MedCode-Qwen Interface" src="https://github.com/user-attachments/assets/0ab0ed1d-7cca-471a-b813-fa4bf963592c" />

<img width="1920" height="988" alt="MedCode-Qwen Answer" src="https://github.com/user-attachments/assets/9a359b7c-edd4-418c-9e66-76de201c3797" />

---

### What It Does

MedCode-Qwen is a Corrective-RAG system that answers questions about medical codes across five major clinical vocabularies. Given a code or a natural language query, it retrieves the exact matching record from a local SQLite index and passes it to Qwen/Qwen2.5-7B-Instruct to produce a precise, clinically-grounded answer.

It covers diagnoses, procedures, and drug classifications — making it useful for clinical coders, medical informatics researchers, and healthcare developers who need fast, accurate lookups without relying on external APIs.

---

### The Model — Qwen/Qwen2.5-7B-Instruct

The language model powering this system is Qwen2.5-7B-Instruct, developed by Alibaba Cloud as part of the Qwen2.5 series.

Qwen2.5-7B-Instruct is a 7-billion parameter instruction-tuned model trained on over 18 trillion tokens. It performs strongly on knowledge-intensive tasks, long-context understanding, and structured reasoning — all of which are critical for clinical coding, where answers must be precise and grounded in specific records rather than general knowledge.

In this system the model is loaded in 4-bit quantisation using BitsAndBytes, reducing memory usage to approximately 5 GB, which fits comfortably within a single NVIDIA T4 GPU. Despite the quantisation, response quality remains high because the model is always provided with the exact retrieved record as context rather than being asked to recall codes from memory.

Key properties of the model used here:

- Parameters: 7 billion
- Quantisation: 4-bit (NF4) via BitsAndBytes
- Context window: 128,000 tokens
- Instruction format: ChatML
- License: Apache 2.0

Model page: https://huggingface.co/Qwen/Qwen2.5-7B-Instruct

---

### The Dataset — MedConceptsQA

The retrieval index is built from MedConceptsQA, an open-source medical coding benchmark containing 819,832 question-answer pairs across five clinical vocabularies at three difficulty levels.

| System | Category | Records |
|---|---|---|
| ICD-10-CM | Diagnosis | 220,000 |
| ICD-9-CM | Diagnosis | 195,000 |
| ICD-10-PROC | Procedure | 198,000 |
| ICD-9-PROC | Procedure | 112,000 |
| ATC | Drug Classification | 95,000 |

Only the question and answer columns are indexed — the multiple choice options are discarded. The index is stored in a SQLite database and queried at runtime using regex-based code extraction with a keyword fallback. No embeddings or vector store are required.

Dataset page: https://huggingface.co/datasets/ofir408/MedConceptsQA

Citation:
> Ofir Ben Shoham and Nadav Rappoport. "MedConceptsQA: Open Source Medical Concepts QA Benchmark." Computers in Biology and Medicine, 2024.

---

### Architecture

The system follows a three-step Corrective-RAG pipeline:

1. The user submits a query containing a medical code or plain language description.
2. The SQLite index is queried instantly using regex to extract code patterns and keyword search as fallback. Up to five matching records are retrieved.
3. The retrieved records are passed as context to Qwen2.5-7B-Instruct, which produces a grounded, clinically accurate answer. If no records are found, the model answers from its own parametric knowledge.

This design means the system never needs to generate codes from scratch — it always has the ground truth record available, and the model's role is explanation and reasoning rather than memorisation.

---

### Project Structure

```
MedCode-Qwen/
├── app.py               Gradio interface — launch this
├── build_db.py          One-time dataset indexer
├── requirements.txt     Python dependencies
├── README.md
└── backend/
    ├── __init__.py
    └── agent.py         Corrective-RAG logic and LLM inference
```

The `data/` folder containing `medconcepts.db` is not included in the repository. It is generated locally by running `build_db.py`.

---

### Requirements

- Python 3.10 or higher
- CUDA GPU with at least 16 GB VRAM (tested on NVIDIA T4 x2)
- Internet access for model and dataset download on first run

---

### Installation

```bash
git clone https://github.com/sufirumii/MedCode-Qwen.git
cd MedCode-Qwen
pip install -r requirements.txt
```

---

### Running the System

**Step 1 — Build the database index (run once, takes approximately 2 minutes)**

```bash
python build_db.py
```

**Step 2 — Launch the interface**

```bash
python app.py
```

The terminal will print a local URL and a public Gradio share link valid for one week.

---

### Running on Kaggle

This project was developed and tested on Kaggle with two T4 GPUs. To run it there:

```python
!pip install transformers datasets gradio bitsandbytes accelerate

!python /kaggle/working/MedCode-Qwen/build_db.py

!python /kaggle/working/MedCode-Qwen/app.py
```

---

### License

Apache 2.0
