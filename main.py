import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
from llama_index.llms import OpenAI
import openai
from utils import copy_md_files_from_to
import os

openai_key = os.environ["OPENAI_API_KEY"]

@st.cache_resource(show_spinner=False)
def load_data(model, system_promt):
    with st.spinner(text="Loading and indexing QBiz Docs... may take a few minutes"):
        reader = SimpleDirectoryReader(input_dir=r".\data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model=model,
                                                                  temperatur=0.7,
                                                                  system_prompt=system_promt,
                                                                  api_key=openai_key))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)

        st.write("Index Created")
        return index



def run_app():

    st.title("QBiz Wiki Chatbot")
    st.header("Chat with the QBiz Wiki page!")

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant",
             "content": "Ask Me Anything about QBiz Wiki!"}
        ]

    st.write('---')
    st.subheader("Prepare data for the chatbot:")
    st.write("##### 1. Copy all markdown files from the `source` folder to the `data` folder.")

    source = st.text_input("Source Directory", value=r"C:\Users\franc\Documents\Qbiz\Side Projects\qbiz-wiki")
    source = r"{source}".format(source=source)

    target = st.text_input("Target Directory", value=r"C:\Users\franc\Documents\Qbiz\Side Projects\QBiz_Chatbot\data")
    target = r"{target}".format(target=target)

    if source and target and st.button("Copy files"):
        copy_md_files_from_to(source, target)

    st.write("##### 2. Load and Index data.")

    st.write("###### 2.1 Set model parameters.")

    model = st.selectbox("Model", ["gpt-3.5-turbo"])

    system_prompt = "You are an expert on QBiz Wiki and your is to answer questions. " \
                    "Assume that all questions are related to the QBiz Wiki. " \
                    "Keep your answers technical and based on facts - do not hallucinate features."
    st.text_area("System Prompt", value=system_prompt)


    index = load_data(model=model,
                      system_promt=system_prompt)

    st.write(index)

    st.write("##### 3. Create the chat engine.")
    chat_engine = index.as_chat_engine(chat_mode='condense_question',
                                       verbose=True)
    st.write("Engine Created")

    if promt := st.chat_input("Your Question"):
        st.session_state.messages.append({"role": "user",
                                          "content": promt})
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_engine.chat(promt)
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message)  # Add response to message history



if __name__ == "__main__":
    run_app()

