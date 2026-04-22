import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
import os

st.set_page_config(page_title="LangChain: Chat with SQL DB")
st.title("Chat with SQL DB")

LOCALDB="USE_LOCALDB"
radio_opt=["Use SQLite 3 Datbase Student.db"]

selected_opt=st.sidebar.radio(label="Choose the DB which you want to chat",options=radio_opt)

if radio_opt.index(selected_opt)==0:
    db_name = "student.db"   # simple input or variable
    db_uri = f"file:{db_name}"

from dotenv import load_dotenv
load_dotenv()

os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")
groq_api_key=os.getenv("GROQ_API_KEY")

llm=ChatGroq(groq_api_key=groq_api_key,model_name="llama-3.1-8b-instant",streaming=True)

@st.cache_resource(ttl="2h")
def configure_db():
    dbfilepath=(Path(__file__).parent/"student.db").absolute()
    return SQLDatabase(create_engine(f"sqlite:///{dbfilepath}"))

db=configure_db()

toolkit=SQLDatabaseToolkit(db=db,llm=llm)
from langchain.prompts import PromptTemplate

prefix = """
You are an expert SQL assistant.
- Use the table schema carefully
- Do not call tools repeatedly
- Generate final SQL query quickly
"""
agent=create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    prefix=prefix,
)

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"]=[{"role":"assistant","content":"How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query=st.chat_input(placeholder="Ask anything from the database")

if user_query:
    st.session_state.messages.append({"role":"user","content":user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback=StreamlitCallbackHandler(st.container())
        response = agent.invoke(
    {"input": user_query},
    {"callbacks": [streamlit_callback]}
)
        st.session_state.messages.append({"role":"assistant","content":response["output"]})
        st.write(response["output"])
    