"""
Streamlit PageIndex + Gemini Chatbot (Vector-less Document QA)

Flow:
1. User uploads PDF
2. Backend creates PageIndex tree
3. Tree stored in session
4. User queries via chat interface
5. Relevant nodes selected via Gemini
6. Context extracted
7. Final answer generated
"""

import streamlit as st
import os
import json
import time
import logging
import re
import tempfile
from pageindex import PageIndexClient
import pageindex.utils as utils
import google.generativeai as genai


# =========================
# 🔐 CONFIGURATION
# =========================

PAGEINDEX_API_KEY = "e5af73db356c4ccba01a9865d28cc995"
GEMINI_API_KEY = "AIzaSyB9LicFqt0wK-zacYJ7Q6zautR2Cs9MePs"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Initialize PageIndex client
pi_client = PageIndexClient(api_key=PAGEINDEX_API_KEY)


# =========================
# 📜 LOGGING CONFIGURATION
# =========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# =========================
# 🤖 LLM CALL FUNCTION
# =========================
def call_llm(prompt: str, model: str = "gemini-2.5-flash", temperature: float = 0.0) -> str:
    """
    Calls Gemini model with deterministic config.
    Returns cleaned text response.
    """
    logging.info("Calling Gemini LLM...")
    model = genai.GenerativeModel(model)

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": temperature,
            "top_p": 1,
            "top_k": 1,
        }
    )

    logging.info("LLM response received.")
    return response.text.strip()


# =========================
# 📄 SUBMIT PDF TO PAGEINDEX
# =========================
def submit_pdf_to_pageindex(pdf_file):
    """
    Saves uploaded PDF temporarily and submits to PageIndex.
    Waits until retrieval is ready.
    Returns document tree.
    """
    logging.info("Saving uploaded PDF...")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_file.read())
        pdf_path = tmp.name

    logging.info("Submitting document to PageIndex...")
    doc_id = pi_client.submit_document(pdf_path)["doc_id"]

    st.info(f"📤 Document Submitted: {doc_id}")

    # Wait for indexing
    with st.spinner("⏳ Processing document..."):
        while not pi_client.is_retrieval_ready(doc_id):
            time.sleep(2)

    logging.info("Retrieval ready. Fetching tree...")

    tree = pi_client.get_tree(doc_id, node_summary=True)["result"]

    return tree


# =========================
# 🔍 FIND RELEVANT NODES
# =========================
def find_relevant_nodes(tree, query):
    """
    Uses Gemini to find relevant nodes from PageIndex tree.
    Returns node_list and reasoning.
    """

    tree_without_text = utils.remove_fields(tree.copy(), fields=["text"])

    search_prompt = f"""
    You are given a question and a tree structure of a document.
    Each node contains node_id, title and summary.

    Question: {query}

    Document Tree:
    {json.dumps(tree_without_text, indent=2)}

    Return JSON:
    {{
        "thinking": "...",
        "node_list": ["node_id1", "node_id2"]
    }}
    """

    result = call_llm(search_prompt)

    # Remove markdown wrapping
    result = re.sub(
        r"(?:^\s*```(?:json)?\s*)|(?:\s*```\s*$)",
        "",
        result,
        flags=re.DOTALL
    )

    return json.loads(result)


# =========================
# 📚 EXTRACT CONTEXT
# =========================
def extract_context(tree, node_list):
    """
    Extracts full text content from relevant nodes.
    """
    node_map = utils.create_node_mapping(tree)

    relevant_content = "\n\n".join(
        node_map[node_id]["text"] for node_id in node_list
    )

    return relevant_content


# =========================
# 🧠 GENERATE FINAL ANSWER
# =========================
def generate_answer(query, context):
    """
    Generates final answer strictly from retrieved context.
    """

    answer_prompt = f"""
    Answer the question based only on the context.

    Question:
    {query}

    Context:
    {context}

    Provide clear and concise answer.
    """

    return call_llm(answer_prompt)


# =========================
# 🎨 STREAMLIT UI
# =========================

st.set_page_config(
    page_title="📘 PageIndex Chat",
    layout="wide"
)

st.title("📘 PageIndex Document Chatbot")
st.markdown("### ⚡ Vector-less Intelligent Document QA")

# Sidebar upload
with st.sidebar:
    st.header("📄 Upload Document")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file:
        if st.button("🚀 Process Document"):
            tree = submit_pdf_to_pageindex(uploaded_file)
            st.session_state.tree = tree
            st.success("✅ Document Indexed Successfully!")

# Chat Interface
if "tree" in st.session_state:

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.divider()
    st.subheader("💬 Ask Questions")

    query = st.chat_input("Ask something about the document...")

    if query:
        st.session_state.chat_history.append(("user", query))

        with st.spinner("🔍 Searching relevant sections..."):
            search_result = find_relevant_nodes(st.session_state.tree, query)
            node_list = search_result["node_list"]

            context = extract_context(st.session_state.tree, node_list)

            answer = generate_answer(query, context)

        st.session_state.chat_history.append(("assistant", answer))

    # Render chat history
    for role, message in st.session_state.chat_history:
        if role == "user":
            with st.chat_message("user"):
                st.markdown(message)
        else:
            with st.chat_message("assistant"):
                st.markdown(message)

else:
    st.info("👈 Upload and process a PDF to start chatting.")