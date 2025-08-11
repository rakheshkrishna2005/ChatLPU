import streamlit as st
import json
import os
from groq import Groq
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
import time
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="ChatLPU",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

AVAILABLE_MODELS = {
    "OpenAI GPT-OSS 120B": "openai/gpt-oss-120b",
    "Llama 3.3 70B Versatile": "llama-3.3-70b-versatile", 
    "DeepSeek R1 Distill 70B": "deepseek-r1-distill-llama-70b",
    "Kimi K2 Instruct": "moonshotai/kimi-k2-instruct",
    "Qwen3 32B": "qwen/qwen3-32b"
}

# Configuration file path
CONFIG_FILE = "chatbot_config.json"

def load_config():
    """Load configuration from file"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {
        "selected_models": list(AVAILABLE_MODELS.keys()),
        "custom_instructions": ""
    }

def save_config(config):
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving configuration: {str(e)}")
        return False

def initialize_groq_client(api_key):
    """Initialize Groq client"""
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing Groq client: {str(e)}")
        return None

def get_model_response(model_id: str, messages: List, api_key: str, custom_instructions: str) -> str:
    """Get response from a specific model"""
    try:
        # Create ChatGroq instance
        llm = ChatGroq(
            groq_api_key=api_key,
            model_name=model_id,
            temperature=0.7,
            max_tokens=1024,
            timeout=60,
            max_retries=2
        )
        
        # Prepare messages with custom instructions
        system_message = SystemMessage(content=custom_instructions)
        human_message = HumanMessage(content=messages[-1])
        
        # Get response
        response = llm([system_message, human_message])
        return response.content
        
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.markdown("<h1 style='text-align: center'>⚡ ChatLPU</h1>", unsafe_allow_html=True)
    
    # Load configuration
    config = load_config()
    
    # Get API key from environment
    api_key = os.getenv("GROQ_API_KEY")
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        st.markdown("---")
        
        # Model selection with better styling
        st.markdown("#### ⚡ Models Available")
        selected_models = []
        
        for model_name in AVAILABLE_MODELS.keys():
            if st.checkbox(
                model_name, 
                value=model_name in config["selected_models"],
                key=f"model_{model_name}"
            ):
                selected_models.append(model_name)
        
        if not selected_models:
            st.warning("⚠️ Please select at least one model")
        
        st.markdown("---")
        
        # Custom instructions
        st.markdown("#### 📝 Custom Instructions")
        custom_instructions = st.text_area(
            "System Instructions (optional)",
            value=config["custom_instructions"],
            height=120,
            help="Add custom instructions for all models",
            placeholder="Custom instructions (optional)..."
        )
        
        st.markdown("---")
        
        # Action buttons with full width
        col1, col2 = st.columns(2)
        
        with col1:
            save_btn = st.button(
                "💾 Save Config", 
                type="primary", 
                use_container_width=True
            )
        
        with col2:
            clear_btn = st.button(
                "🗑️ Clear Chat", 
                use_container_width=True
            )
        
        if save_btn:
            new_config = {
                "selected_models": selected_models,
                "custom_instructions": custom_instructions
            }
            if save_config(new_config):
                st.success("✅ Configuration saved!")
                time.sleep(1)
                st.rerun()
        
        if clear_btn:
            if "messages" in st.session_state:
                del st.session_state.messages
            st.success("✅ Chat history cleared!")
            time.sleep(1)
            st.rerun()
    
    # Main chat interface
    if not api_key:
        st.error("🔑 **Groq API Key not found!**")
        st.info("Please create a `.env` file in your project directory with:")
        st.code("GROQ_API_KEY=your_actual_api_key_here", language="bash")
        st.info("Get your API key from: https://console.groq.com/keys")
        return
    
    if not selected_models:
        st.info("👈 **Please select at least one model in the sidebar**")
        return
    
    # Initialize chat history
    if "messages" in st.session_state:
        messages = st.session_state.messages
    else:
        messages = []
        st.session_state.messages = messages
    
    # Display chat history
    if messages:
        for message in messages:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    st.markdown(f"**You:** {message['content']}")
                else:
                    st.markdown("**Assistant:** Responses from selected models")
                    if "responses" in message:
                        for model_name, response in message["responses"].items():
                            with st.expander(f"🤖 {model_name}", expanded=len(message["responses"]) == 1):
                                st.markdown(response)
    
    # Chat input with better styling
    st.markdown("---")
    prompt = st.chat_input("💭 Ask a question...", key="chat_input")
    if prompt:
        # Add user message to chat history
        messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(f"**You:** {prompt}")
        
        # Generate responses from selected models
        with st.chat_message("assistant"):
            st.markdown("**Assistant:** Generating responses from selected models...")
            
            responses = {}
            
            # Generate responses with spinners
            for i, model_name in enumerate(selected_models):
                model_id = AVAILABLE_MODELS[model_name]
                
                with st.spinner(f"🔄 {model_name}..."):
                    # Get response from model
                    response = get_model_response(
                        model_id, 
                        [prompt], 
                        api_key, 
                        custom_instructions if custom_instructions.strip() else "You are a helpful AI assistant."
                    )
                    responses[model_name] = response
            
            # Display success message
            st.success(f"✅ Generated {len(responses)} responses!")
            
            # Display responses in expanders
            for model_name, response in responses.items():
                with st.expander(f"🤖 {model_name}", expanded=len(selected_models) == 1):
                    st.markdown(response)
        
        # Add assistant message to chat history
        messages.append({
            "role": "assistant", 
            "content": f"Responses generated from {len(selected_models)} models",
            "responses": responses
        })
        
        # Update session state
        st.session_state.messages = messages

if __name__ == "__main__":
    main()
