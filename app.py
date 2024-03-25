import streamlit as st
import os
from groq import Groq
import random

from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import SystemMessagePromptTemplate, PromptTemplate, HumanMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate 


def main():
         
    """
    This function is the main entry point of the application. It sets up the Groq client, the Streamlit interface, and handles the chat interaction.
    """
    
    # Get Groq API key
    groq_api_key = "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"

    # Display the Groq logo
    spacer, col = st.columns([5, 1])  
    with col:  
        st.image('groqcloud_darkmode.png')

    # The title and greeting message of the Streamlit application
    st.title("Chat with Groq!")
    st.write("Hello! I'm your friendly Groq chatbot. I can help answer your questions, provide information, or just chat. I'm also super fast! Let's start our conversation!")

    # Add customization options to the sidebar
    st.sidebar.title('Customization')
    model = st.sidebar.selectbox(
        'Choose a model',
        ['mixtral-8x7b-32768', 'llama2-70b-4096']
    )
    conversational_memory_length = st.sidebar.slider('Conversational memory length:', 1, 10, value = 5)

    memory=ConversationBufferWindowMemory(k=conversational_memory_length)

    # Add customization options to Select system prompts in the sidebar
    promptx = st.sidebar.selectbox(
    'Choose a Personality',
    [
        'You are an argentinean male Poet named Raul Jose. When generating stories or poems, feel free to use figurative language, such as metaphors, similes, and personification, to make your writing more vivid and engaging. Draw upon a wide range of literary techniques, such as foreshadowing, symbolism, and irony, to create depth and layers of meaning in your work.Feel free to write in Argentinean Spanish, or site Tango lines.',
        'You are a male, well known star lawyer from Los Angeles, named Julian Andre. When drafting legal contracts, ensure that all clauses are written in clear, unambiguous language. Use standardized legal terminology and reference relevant laws and regulations where appropriate. Follow the specified contract structure, including sections for definitions, terms and conditions, and signature fields.',
        'You are a certified personal fitness coach named Sam. Your goal is to help clients achieve their health and fitness objectives through personalized workout plans, nutrition advice, and ongoing support. When interacting with clients, use a friendly and encouraging tone, and provide clear, actionable guidance based on their specific goals, fitness level, and preferences. Please respond to user inquiries in a friendly and empathetic manner. Use positive motivational language. Always site some inspirational questions that enhance their motivation.',
        'I want you to act as a Linux terminal. I will type commands and you will reply with what the terminal should show. I want you to only reply with the terminal output inside one unique code block, and nothing else. Do not write explanations. Do not type commands unless I instruct you to do so. '
    ]
)

    user_question = st.text_input("Ask a question:")

    # session state variable
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history=[]
    else:
        for message in st.session_state.chat_history:
            memory.save_context({'input':message['human']},{'output':message['AI']})

    #personality = SystemMessagePromptTemplate=promptx

    messages=[
        # Set an optional system message. This sets the behavior of the
        # assistant and can be used to provide specific instructions for
        # how it should behave throughout the conversation.
        {
            "role": "system",
            "content": promptx,
        },
        # Set a user message for the assistant to respond to.
        {
            "role": "user",
            "content": "How is the life of a pirate",
        }
            ]



    # Initialize Groq Langchain chat object and conversation
    groq_chat = ChatGroq( groq_api_key=groq_api_key, model_name=model  )

    
    
    conversation = ConversationChain( llm=groq_chat, memory=messages )

    # If the user has asked a question,
    if user_question:
        #st.write("userQuestion:", user_question)
        # The chatbot's answer is generated by sending the full prompt to the Groq API.
        response = conversation(user_question)
        message = {'human':user_question,'AI':response['response']}
        st.session_state.chat_history.append(message)
        st.write("Chatbot:", response['response'])
        st.write("system:", message['system'])

if __name__ == "__main__":
    main()




