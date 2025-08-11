# ⚡ ChatLPU

**ChatLPU** is an interactive, multi-model technical chatbot built with **Streamlit** and powered by Groq-hosted large language models. It’s designed for **learning, research, and exploration of technical topics**, allowing you to query multiple AI models side-by-side for comparison.

## 🚀 Features

* **Multi-Model Support**
  Choose from multiple advanced models such as:

  * OpenAI GPT-OSS 120B
  * Llama 3.3 70B Versatile
  * DeepSeek R1 Distill 70B
  * Kimi K2 Instruct
  * Qwen3 32B

* **Custom System Instructions**
  Fine-tune responses by adding your own system-level prompts.

* **Persistent Configuration**
  Save and load your preferred model selections and instructions automatically via a JSON config file.

* **Interactive Chat Interface**

  * Real-time chat with multiple models
  * Expandable model-specific responses
  * Clear chat history with one click

* **Sidebar Controls**

  * Model selection checkboxes
  * Instruction editor
  * Save & clear buttons

## 🛠 Technology Stack

* **Python** — Core language
* **Streamlit** — UI framework
* **Groq** — API client for hosted models
* **LangChain** — Model interaction abstraction
* **dotenv** — Environment variable management


## 📂 Project Structure

```
app.py                # Main application script
chatbot_config.json   # Auto-generated user configuration file
.env                  # Environment variables (API keys)
```

## 🔑 Environment Variables

The app requires a **Groq API key** stored in a `.env` file:

```
GROQ_API_KEY=your_actual_api_key_here
```

You can obtain your key from:
[https://console.groq.com/keys](https://console.groq.com/keys)

## 💡 Usage Flow

1. **Select Models** from the sidebar.
2. **Add Custom Instructions** (optional).
3. **Ask a Question** in the chat input.
4. View **side-by-side AI responses** from your chosen models.
5. **Save Config** for future sessions or **Clear Chat** anytime.
