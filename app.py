import streamlit as st
import os
import tempfile
import ollama
import random
import json
from rag_system import PurePythonRAG

# Cache buster: 2025-11-17-22-03
st.set_page_config(
    page_title="My Provon - Pure Python",
    page_icon="🧠",
    layout="wide"
)

# Fun loading messages while AI thinks
LOADING_MESSAGES = [
    "Madam ji, bas thoda sa wait kr lo, result bas aane hi wala hai.",
    "Ethu sa aur wait lo madam ji, system process kar raha hai.",
    "Jyada mat socho, output bas nikalne hi wala hai.",
    "Dude, bas 2 sec, AI ka dimaag ghoom raha hai abhi.",
    "Madam ji, bas thoda patience rakh lo, result loading mein hai.",
    "Ettu sa wait karo na, result abhi-abhi aa jayega.",
    "Relax madam ji, AI ka kaam chal raha h… final result incoming.",
    "Bas ek chhota sa second aur… result landing.",
    "Thoda sa aur ruk jao madam ji, output processing ho raha hai.",
    "Dude, AI ko bus ek sip chai peene do, result ready ho jayega.",
    "Madam ji, tension mat lo, result bilkul pass hi hai.",
    "Bus ekdum last step chal raha hai, thoda sa aur wait karo.",
    "Ettu sa bhi wait nahi kar sakti kya? Result aa raha haiaa.",
    "AI is thinking madam ji… bas thoda sa aur time.",
    "Madam ji, patience ka phal sweet hota hai, result abhi abi."
]

# Initialize RAG system
@st.cache_resource
def load_rag_system():
    return PurePythonRAG()

rag_system = load_rag_system()

# Function to generate diagram/flowchart
def generate_diagram(answer, question):
    """Generate a diagram or flowchart based on the answer"""
    try:
        diagram_prompt = f"""You MUST create an ASCII diagram. This is mandatory.

Question: {question}
Answer: {answer}

Create a visual ASCII diagram that shows:
1. Main topic/concept at the top or center
2. Sub-concepts branching out
3. Relationships shown with arrows (-->, <--, <-->)
4. Hierarchy shown with | and -

Example format:
        Main Concept
           |
      _____|_____
     |           |
   Sub1        Sub2
     |           |
   Detail    Detail

Now create the diagram for the above Q&A. Make it clear and structured."""
        
        diagram_response = ollama.generate(model='llama2:latest', prompt=diagram_prompt)
        return diagram_response['response']
    except Exception as e:
        return f"Could not generate diagram: {str(e)}"

# Sidebar
st.sidebar.title("📚 My Documents")
st.sidebar.write("Upload your documents to build your knowledge base")

uploaded_files = st.sidebar.file_uploader(
    "Choose files (PDF, TXT, DOCX)",
    type=['pdf', 'txt', 'docx'],
    accept_multiple_files=True
)

if uploaded_files:
    if st.sidebar.button("🚀 Add to Knowledge Base"):
        with st.spinner("Processing documents..."):
            file_paths = []
            for uploaded_file in uploaded_files:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    file_paths.append(tmp_file.name)
            
            try:
                # Add documents to knowledge base
                chunk_count = rag_system.add_documents(file_paths)
                if chunk_count > 0:
                    st.sidebar.success(f"✅ Added {chunk_count} knowledge chunks!")
                else:
                    st.sidebar.warning("⚠️ No content extracted from files")
            except Exception as e:
                st.sidebar.error(f"❌ Error: {str(e)}")
            finally:
                # Clean up temporary files
                for file_path in file_paths:
                    try:
                        os.unlink(file_path)
                    except:
                        pass

# Knowledge base info
st.sidebar.markdown("---")
st.sidebar.info(rag_system.get_collection_info())

# Main interface
st.title("🧠 My Provon - Pure Python")
st.write("**priiii**, how can i help you")

# Chat interface
if not st.session_state.get("messages"):
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.get("messages", []):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        # Show random loading message
        loading_msg = random.choice(LOADING_MESSAGES)
        with st.spinner(loading_msg):
            response = rag_system.query(prompt)
            
            # Display answer with priiii prefix
            st.markdown("### 📝 Answer")
            st.markdown(f"**priiii** {response['answer']}")
            
            # Display sources
            if response["sources"]:
                st.markdown("### 🔍 Sources")
                for i, source in enumerate(response["sources"]):
                    score = response["scores"][i] if i < len(response["scores"]) else "N/A"
                    st.write(f"• **{source}** (relevance: {score:.2f})")
            
            # Add diagram/flowchart button
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                generate_diagram_btn = st.button("📊 Generate Diagram", use_container_width=True)
            
            if generate_diagram_btn:
                with st.spinner("🎨 Creating diagram..."):
                    diagram = generate_diagram(response['answer'], prompt)
                    st.markdown("### 📈 Diagram/Flowchart")
                    st.markdown(f"```\n{diagram}\n```")

    # Add assistant response to chat history
    st.session_state.messages.append({
        "role": "assistant", 
        "content": f"**priiii** {response['answer']}\n\n**Sources:** {', '.join(response['sources']) if response['sources'] else 'None'}"
    })


# Clear chat button
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.sidebar.success("Chat history cleared!")