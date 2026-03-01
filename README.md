# 📘 PageIndex Vector-less Document Chat

A Streamlit-based intelligent document chatbot using **PageIndex Tree Retrieval** and **Google Gemini**.

This system performs structured document reasoning **without embeddings** (vector-less RAG).

---

## 🚀 Features

- 📄 Upload any PDF
- 🌳 Automatic hierarchical PageIndex tree generation
- 🔍 LLM-based node selection (structure-aware)
- 🧠 Context-aware answer generation
- 💬 Interactive chatbot interface
- 🌙 Dark themed modern UI
- 🪵 Logging enabled for debugging
- 🔐 Secure API key handling via `.env`

---

## 🧠 Architecture Overview

```
User Uploads PDF
        ↓
PageIndex Creates Tree Structure
        ↓
Gemini Selects Relevant Nodes
        ↓
Extract Text from Selected Nodes
        ↓
Gemini Generates Final Answer
        ↓
Streamlit Chat UI Displays Response
```

This is **Tree-based RAG (Structure-driven Retrieval)** instead of traditional embedding/vector search.

---

## 📁 Project Structure

```
pageindex-vectorless-chat/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
└── .streamlit/
      └── config.toml
```

---

# ⚙️ Installation Guide (Step-by-Step)

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/pageindex-vectorless-chat.git
cd pageindex-vectorless-chat
```

---

## 2️⃣ Create Virtual Environment (Windows PowerShell)

```powershell
python -m venv venv
```

Activate the environment:

```powershell
.\venv\Scripts\Activate
```

If you get execution policy error:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 3️⃣ Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 4️⃣ Create `.env` File

Inside the root folder create a file named:

```
.env
```

Add your API keys:

```
PAGEINDEX_API_KEY=your_pageindex_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

---

# 🔑 How To Get API Keys

## 🧠 PageIndex API Key

Create your API key here:

https://dash.pageindex.ai/api-keys

---

## 🤖 Google Gemini API Key

Create your Gemini API key here:

https://aistudio.google.com/app/apikey

---

# ▶️ Run the Application

```powershell
streamlit run app.py
```

Then open your browser:

```
http://localhost:8501
```

---

# 🔒 Security Notes

- `.env` file is ignored in git via `.gitignore`
- Never commit your API keys
- Keep production keys secure
- Rotate keys if accidentally exposed

---

# 🧪 How It Works (Detailed Flow)

1. User uploads a PDF.
2. The PDF is submitted to PageIndex.
3. PageIndex builds a hierarchical tree representation of the document.
4. Gemini analyzes the tree structure to identify relevant nodes.
5. Text is extracted only from those selected nodes.
6. Gemini generates an answer strictly based on extracted context.
7. The response is displayed in a Streamlit chat interface.

---

# 🛠 Tech Stack

- Python 3.10+
- Streamlit
- PageIndex
- Google Gemini (gemini-2.5-flash)
- dotenv
- Logging

---

# 🌙 Dark Theme Configuration

Inside `.streamlit/config.toml`

```toml
[theme]
base="dark"
primaryColor="#8B5CF6"
backgroundColor="#0E1117"
secondaryBackgroundColor="#1E1E2E"
textColor="#FFFFFF"
font="sans serif"
```

---

# 🚀 Future Improvements

- Streaming LLM responses
- Source citation display
- Multi-document upload
- Docker support
- Azure / AWS deployment
- Tree visualization UI
- Agent-based routing system
- Authentication layer

---

# 📜 License

MIT License

---

# 👨‍💻 Author

Built with ❤️ using structured document intelligence.

---

# ⭐ If You Like This Project

Give it a ⭐ on GitHub and share with others!
