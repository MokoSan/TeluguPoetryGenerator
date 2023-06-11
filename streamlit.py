from dotenv import load_dotenv
import openai
import os
import streamlit as st
from streamlit_chat import message

#st.title("Enter Text To Generate a Short Telegu Poetry For. ఒక చిన్న తెలుగు కవితను రూపొందించడానికి వచనాన్ని నమోదు చేయండి.")

def get_telegu_poetry(query) -> str:
    query_to_extract_info = f"""Based on the main topic mentioned in the input delimited by ++++, generate a telegu poem and provide a translation. 
    The poem can be descriptive, colorful and filled with allegories. 
    +++
    {query}
    """ 
    messages = [{ "role": "system", "content": "You are a creative Telegu poetry generator bot that provides a translation for every poem"}]
    messages.append( {"role": "user", "content": query_to_extract_info} )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
    )
    response_text = (response.choices[0].message["content"])
    return response_text

def process_input():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        with st.session_state["thinking_spinner"], st.spinner(f"Generating Poetry"):
            telegu_poetry = get_telegu_poetry(user_text)

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((telegu_poetry, False))
    
def display_messages() -> None:
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key = f"{i}.{msg}")
    st.session_state["thinking_spinner"] = st.empty() 

def run() -> None:
    if len(st.session_state) == 0:
        load_dotenv()
        st.session_state["messages"] = [("Chat with me for topics to generate Telegu poetry for. తెలుగు కవిత్వాన్ని రూపొందించడానికి అంశాల కోసం నాతో చాట్ చేయండి", False)]
        st.session_state["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") 
        openai.api_key = os.getenv("OPENAI_API_KEY") 
    
    display_messages()
    st.text_input("Enter a message for which Telegu poetry is to be generated for.", key="user_input", on_change=process_input, label_visibility='visible')

    st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)
    st.divider()
    st.text("Made by Moko.")

if __name__ == '__main__':
    run()