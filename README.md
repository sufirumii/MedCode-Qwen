# MedCode-Qwen

Retrieval-augmented clinical coding agent over 819,832 ICD and ATC medical records, powered by Qwen/Qwen2.5-7B-Instruct.

---

### Demo

<img width="1920" height="900" alt="Screenshot 2026-03-04 at 2 03 40 AM" src="https://github.com/user-attachments/assets/0ab0ed1d-7cca-471a-b813-fa4bf963592c" />

<img width="1920" height="988" alt="Screenshot 2026-03-04 at 2 03 59 AM" src="https://github.com/user-attachments/assets/9a359b7c-edd4-418c-9e66-76de201c3797" />

---

### What It Does

MedCode-Qwen is a Corrective-RAG system that answers questions about medical codes across five major clinical vocabularies. Given a code or a natural language query, it retrieves the exact matching record from a local SQLite index and passes it to a large language model to produce a precise, clinically-grounded answer.

It covers diagnoses, procedures, and drug classifications — making it useful for clinical coders, medical informatics researchers, and healthcare developers who need fast, accurate lookups without relying on external APIs.

---

### Covered Vocabularies

| System | Category | Records |
|---|---|---|
| ICD-10-CM | Diagnosis | 220,000 |
| ICD-9-CM | Diagnosis | 195,000 |
| ICD-10-PROC | Procedure | 198,000 |
| ICD-9-PROC | Procedure | 112,000 |
| ATC | Drug Classification | 95,000 |

Total indexed records: 819,832

---

### Architecture

The system follows a three-step Corrective-RAG pipeline:

1. The user submits a query containing a medical code or plain language description.
2. A SQLite index is queried using regex-based code extraction and keyword fallback. This takes milliseconds and requires no embeddings or vector store.
3. The top retrieved records are passed as context to Qwen/Qwen2.5-7B-Instruct, which produces a concise, accurate answer grounded in the retrieved data. If no records are found, the model falls back to its own medical knowledge.

---

### Project Structure

```
MedCode-Qwen/
├── app.py               Gradio interface — launch this
├── build_db.py          One-time dataset indexer
├── requirements.txt     Python dependencies
├── README.md
├── backend/
│   └── agent.py         Corrective-RAG logic and LLM inference
└── data/
    └── medconcepts.db   SQLite index (built by build_db.py, not in repo)
```

---

### Requirements

- Python 3.10 or higher
- CUDA GPU with at least 16 GB VRAM (tested on NVIDIA T4 x2)
- Internet access for model and dataset download on first run

---

### Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/sufirumii/MedCode-Qwen.git
cd MedCode-Qwen
pip install -r requirements.txt
```

---

### Running the System

**Step 1 — Build the database index (run once)**

This streams the MedConceptsQA dataset from Hugging Face and indexes it into a local SQLite database. Takes approximately two minutes.

```bash
python build_db.py
```

**Step 2 — Launch the interface**

```bash
python app.py
```

The terminal will print a local URL and a public Gradio share link valid for one week. Open either in your browser to use the interface.

---

### Running on Kaggle

This project was built and tested on Kaggle with two T4 GPUs. To run it there:

```python
# Install dependencies
!pip install transformers datasets gradio bitsandbytes accelerate

# Build the index
!python /kaggle/working/MedCode-Qwen/build_db.py

# Launch
!python /kaggle/working/MedCode-Qwen/app.py
```

The model is loaded in 4-bit quantisation via BitsAndBytes, fitting comfortably within a single T4's 16 GB VRAM.

---

### Dataset

The system is built on MedConceptsQA, an open-source benchmark published in:

> Ofir Ben Shoham and Nadav Rappoport. "MedConceptsQA: Open Source Medical Concepts QA Benchmark." Computers in Biology and Medicine, 2024.

Dataset: https://huggingface.co/datasets/ofir408/MedConceptsQA

---

### Model

Qwen/Qwen2.5-7B-Instruct by Alibaba Cloud, loaded in 4-bit quantisation.

Model: https://huggingface.co/Qwen/Qwen2.5-7B-Instruct

---

### License

Apache 2.0
