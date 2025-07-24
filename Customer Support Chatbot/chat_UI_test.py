import streamlit as st
from PIL import Image
import openai  # Optional for AI chatbot functionality
import os

# Configure the layout
st.set_page_config(layout="wide")

# Create two columns
col1, col2 = st.columns([1, 1])

# Image Display Section (Left Column)
with col1:
    st.header("Image Display")
    
    # Upload image functionality
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
    else:
        # Display a placeholder image
        st.image("https://via.placeholder.com/500x300?text=Upload+an+image", 
                caption="Placeholder Image", 
                use_column_width=True)

# Chatbot Section (Right Column)
with col2:
    st.header("Chat Assistant")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Accept user input
    if prompt := st.chat_input("What would you like to know about the image?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message in chat container
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response (placeholder - replace with actual AI integration)
        ai_response = f"I received your question about the image: {prompt}"
        
        # For actual OpenAI integration (uncomment and add your API key):
        # openai.api_key = os.getenv("OPENAI_API_KEY")
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=st.session_state.messages
        # )
        # ai_response = response.choices[0].message.content
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(ai_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

# Optional CSS styling
st.markdown("""
    <style>
        [data-testid="stHorizontalBlock"] {
            align-items: center;
        }
        .stChatFloatingInputContainer {
            bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)