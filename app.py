import streamlit as st
import os
from groq import Groq
import random

from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import SystemMessagePromptTemplate, PromptTemplate, HumanMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate 



         
 

client = Groq(
    api_key= "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" )


chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of low latency LLMs",
        }
    ],
    model="mixtral-8x7b-32768",
)

print(chat_completion.choices[0].message.content)





