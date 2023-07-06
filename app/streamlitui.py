import openai
import os
import streamlit as st
import requests
import uuid
import os
from streamlit_chat import message
from dotenv import load_dotenv
from supabase import create_client, Client

def get_telugu_poetry(query) -> str:
    query_to_extract_info = f"""Based on the main topic mentioned in the input delimited by ++++, generate a telugu poem and provide a translation. 
    The poem can be descriptive, colorful and filled with allegories.
    +++
    {query}
    """ 
    messages = [{ "role": "system", "content": "You are a creative telugu poetry generator bot that provides a translation for every poem."}]
    messages.append( {"role": "user", "content": query_to_extract_info} )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
    )
    response_text = (response.choices[0].message["content"])
    return response_text

def process_input():
    try:
        if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
            user_text = st.session_state["user_input"].strip()
            url = ""
            with st.session_state["thinking_spinner"], st.spinner(f"Generating Poetry"):
                telugu_poetry = get_telugu_poetry(user_text)
                poetry = telugu_poetry.split("Translation")[0]
                options = { 
                    'headers': { 'Accept': 'application/octet-stream', 'Content-Type': 'text/plain', 'x-api-key': os.getenv('NARKEET_API_KEY'), },
                    'data': poetry.encode('utf8')
                }
                url = f'https://api.narakeet.com/text-to-speech/m4a?voice=ramakrishna'
                file_data = requests.post(url, **options).content
                file_name = str(uuid.uuid4()) + ".m4a"
                supabase = st.session_state["supabase_client"]
                res = supabase.storage.from_('poems').upload(file_name, file_data)
                url = supabase.storage.from_('poems').get_public_url(file_name)

            st.session_state["messages"].append((user_text, True))
            st.session_state["messages"].append((telugu_poetry, False))
            st.session_state["messages"].append((f'<audio controls src="{url}"></audio>', False))
    except Exception as ex:
        print(ex)
        st.session_state["messages"].append((f"Request failed: {ex}", False))
    
def display_messages() -> None:
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        avatar_style = 'initials/svg?seed=OM'
        if is_user:
            avatar_style = 'initials/svg?seed=User' 
        message(msg, is_user=is_user, key = f"{i}.{msg}", allow_html = True, avatar_style = avatar_style)
    st.session_state["thinking_spinner"] = st.empty() 

def run() -> None:
    if len(st.session_state) == 0:
        load_dotenv()
        st.session_state["messages"] = [("Chat with me for topics to generate telugu poetry for. తెలుగు కవిత్వాన్ని రూపొందించడానికి అంశాల కోసం నాతో చాట్ చేయండి", False)]
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        supabase: Client = create_client(url, key)
        st.session_state["supabase_client"] = supabase 
        st.session_state["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") 
        openai.api_key = os.getenv("OPENAI_API_KEY") 
    
    display_messages()
    st.text_input("Enter a message for which telugu poetry is to be generated for.", key="user_input", on_change=process_input, label_visibility='visible')

    st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True )
    st.divider()
    st.text("Made by Moko.")

if __name__ == '__main__':
    run()