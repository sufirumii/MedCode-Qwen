import gradio as gr
import sys

sys.path.insert(0, "/kaggle/working/clinical_coding_agent")
from backend.agent import answer

# --- Professional CSS ---
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@900&family=DM+Sans:wght@300;400;500;700&family=DM+Mono&display=swap');

:root {
    --bg-near-black: #040d1a;
    --accent-teal: #0c9e91;
    --text-near-white: #e8f4f2;
    --text-muted: #5c7f8a;
    --border-subtle: #0c9e9120;
}

body {
    font-family: 'DM Sans', sans-serif;
    background: var(--bg-near-black);
    color: var(--text-near-white);
    line-height: 1.8;
}

.gradio-container {
    background: var(--bg-near-black) !important;
    font-size: 1.1rem;
}

.gr-box, .gr-form {
    background: var(--bg-near-black) !important;
    border: 1px solid var(--border-subtle) !important;
}

.gr-chatbot {
    background: transparent !important;
    border: none !important;
    font-size: 1.3rem !important;
    min-height: 70vh !important;
    margin: 0 auto !important;
    max-width: 90% !important;
}

.gr-chatbot .user-message {
    background: var(--accent-teal) !important;
    color: white !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.4rem !important;
    line-height: 2.0 !important;
    padding: 24px !important;
    border-radius: 16px 16px 4px 16px !important;
    margin: 12px 0 !important;
    box-shadow: 0 4px 12px rgba(12, 158, 145, 0.3) !important;
}

.gr-chatbot .bot-message {
    background: rgba(7, 15, 28, 0.8) !important;
    color: var(--text-near-white) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.35rem !important;
    line-height: 2.0 !important;
    padding: 28px !important;
    border-left: 3px solid var(--accent-teal) !important;
    border-radius: 0 !important;
    margin: 12px 0 !important;
}

.gr-textbox {
    background: rgba(7, 15, 28, 0.9) !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-near-white) !important;
    font-size: 1.2rem !important;
    padding: 18px !important;
    border-radius: 6px !important;
    margin: 12px 0 !important;
}

.gr-textbox:focus {
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(12, 158, 145, 0.2) !important;
}

.gr-button {
    background: var(--accent-teal) !important;
    color: var(--bg-near-black) !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    height: 56px !important;
    border-radius: 6px !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    width: 100% !important;
    margin: 12px 0 !important;
}
"""

# --- Chat Function ---
def chat(message, history):
    if not message.strip():
        return history, ""
    result = answer(message)
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": f"{result['answer']}\n\n— {result['source']}"})
    return history, ""

# --- Hero HTML (Professional Copy) ---
hero_html = """
<div style="
    text-align: center;
    padding: 96px 24px 64px;
    border-bottom: 1px solid #0c9e9120;
    margin-bottom: 48px;
    background: linear-gradient(180deg, rgba(4, 13, 26, 0.9) 0%, rgba(7, 15, 28, 0.9) 100%);
">
    <div style="
        font-size: 0.8rem;
        letter-spacing: 0.3em;
        text-transform: uppercase;
        color: #0c9e91;
        margin-bottom: 24px;
        font-family: 'DM Sans', sans-serif;
        font-weight: 700;
    ">
        CLINICAL CODING INTELLIGENCE
    </div>
    <div style="
        font-family: 'Cormorant Garamond', serif;
        font-size: clamp(4rem, 8vw, 7rem);
        font-weight: 900;
        line-height: 0.9;
        letter-spacing: -4px;
        color: #e8f4f2;
        margin-bottom: 32px;
        text-shadow: 2px 4px 12px rgba(12, 158, 145, 0.2);
    ">
        MEDCODE<br>INTELLIGENCE
    </div>
    <div style="
        font-size: 1.3rem;
        color: #5c7f8a;
        font-family: 'DM Sans', sans-serif;
        font-weight: 400;
        margin-bottom: 36px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.9;
    ">
        Precision coding across 819,832+ medical records, powered by Qwen2.5-7B-Instruct.
    </div>
    <div style="
        display: inline-block;
        font-size: 0.8rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #0c9e91;
        border: 1px solid #0c9e9140;
        border-radius: 4px;
        padding: 10px 24px;
        font-family: 'DM Sans', sans-serif;
        margin-bottom: 40px;
    ">
        QWEN2.5-7B-INSTRUCT · CORRECTIVE-RAG · 819,832+ CODES
    </div>
    <div style="
        display: flex;
        justify-content: center;
        gap: 2px;
        margin-top: 20px;
        border: 1px solid #0c9e9120;
        border-radius: 6px;
        overflow: hidden;
        max-width: 720px;
        margin-left: auto;
        margin-right: auto;
        background: rgba(7, 15, 28, 0.6);
    ">
        <div style="flex: 1; padding: 24px 12px; text-align: center; border-right: 1px solid #0c9e9120;">
            <div style="font-family: 'Cormorant Garamond', serif; font-size: 2rem; font-weight: 900; color: #0c9e91;">819K+</div>
            <div style="font-size: 0.7rem; letter-spacing: 0.15em; text-transform: uppercase; color: #5c7f8a; margin-top: 6px;">RECORDS</div>
        </div>
        <div style="flex: 1; padding: 24px 12px; text-align: center; border-right: 1px solid #0c9e9120;">
            <div style="font-family: 'Cormorant Garamond', serif; font-size: 2rem; font-weight: 900; color: #0c9e91;">5</div>
            <div style="font-size: 0.7rem; letter-spacing: 0.15em; text-transform: uppercase; color: #5c7f8a; margin-top: 6px;">VOCABULARIES</div>
        </div>
        <div style="flex: 1; padding: 24px 12px; text-align: center; border-right: 1px solid #0c9e9120;">
            <div style="font-family: 'Cormorant Garamond', serif; font-size: 1.8rem; font-weight: 900; color: #0c9e91;">ICD-10<br>ATC</div>
            <div style="font-size: 0.7rem; letter-spacing: 0.15em; text-transform: uppercase; color: #5c7f8a; margin-top: 6px;">STANDARDS</div>
        </div>
        <div style="flex: 1; padding: 24px 12px; text-align: center;">
            <div style="font-family: 'Cormorant Garamond', serif; font-size: 2rem; font-weight: 900; color: #0c9e91;">7B</div>
            <div style="font-size: 0.7rem; letter-spacing: 0.15em; text-transform: uppercase; color: #5c7f8a; margin-top: 6px;">PARAMETERS</div>
        </div>
    </div>
</div>
"""

# --- Footer HTML ---
footer_html = """
<div style="
    text-align: center;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #1a3040;
    border-top: 1px solid #0c9e9112;
    padding: 40px 0 24px;
    margin-top: 64px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
">
    MEDCODE INTELLIGENCE · CORRECTIVE-RAG · QWEN2.5-7B-INSTRUCT · 819,832+ MEDICAL CODES
</div>
"""

# --- Build the Interface ---
with gr.Blocks(css=custom_css) as demo:
    # Hero
    gr.HTML(hero_html)

    # Section Heading
    gr.HTML(
        "<div style='font-family: \"DM Sans\", sans-serif; font-size: 0.9rem; letter-spacing: 0.25em; text-transform: uppercase; color: #0c9e91; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #0c9e9120;'>ASK THE AGENT</div>"
    )

    # Chatbot (Professional, No Examples)
    chatbot = gr.Chatbot(
        type="messages",
        height=800,
        show_label=False,
        allow_tags=True
    )

    # Input Area
    with gr.Row():
        msg = gr.Textbox(
            placeholder="Enter your clinical coding query...",
            container=False,
            scale=8,
            lines=2
        )
        submit_btn = gr.Button("SUBMIT", scale=1)

    # Event Handlers
    msg.submit(chat, [msg, chatbot], [chatbot, msg])
    submit_btn.click(chat, [msg, chatbot], [chatbot, msg])

    # Footer
    gr.HTML(footer_html)

# --- Launch ---
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True
    )
