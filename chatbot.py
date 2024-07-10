import streamlit as st
import openai

st.title("My Tiny little bot")
openai.api_key = " "#enter your apikey within the quotes

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.container():
        st.markdown(f"**{message['role'].capitalize()}:** {message['content']}")

prompt = st.text_input("What is up?")
if prompt:
    with st.container():
        st.markdown(f"**User:** {prompt}")
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.container():
        message_placeholder = st.empty()
        full_response = ""

        response = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        for chunk in response:
            full_response += chunk["choices"][0].get("delta", {}).get("content", "")
            message_placeholder.markdown(f"**Assistant:** {full_response}...")

        message_placeholder.markdown(f"**Assistant:** {full_response}")
    st.session_state.messages.append({"role": "assistant", "content": full_response})


