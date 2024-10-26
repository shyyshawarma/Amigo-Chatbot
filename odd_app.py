# import streamlit as st
# import requests

# def create_chat_session(api_key, external_user_id):
#     create_session_url = 'https://api.on-demand.io/chat/v1/sessions'
#     create_session_headers = {
#         'apikey': api_key
#     }
#     create_session_body = {
#         'pluginIds': [],
#         'externalUserId': external_user_id
#     }

#     response = requests.post(create_session_url, headers=create_session_headers, json=create_session_body)
#     response_data = response.json()
#     return response_data['data']['id']

# def submit_query(api_key, session_id, query):
#     submit_query_url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
#     submit_query_headers = {
#         'apikey': api_key
#     }
#     submit_query_body = {
#         'endpointId': 'predefined-openai-gpt4o',
#         'query': query,
#         'pluginIds': ['plugin-1713962163','plugin-1718189536'],
#         'responseMode': 'sync'
#     }

#     query_response = requests.post(submit_query_url, headers=submit_query_headers, json=submit_query_body)
#     return query_response.json()

# def main():
#     st.title("Amigo")
    

#     # Sidebar for API key and external user ID
#     st.sidebar.header("API Configuration")
#     api_key = st.sidebar.text_input("Enter API Key", type="password")
#     external_user_id = st.sidebar.text_input("Enter External User ID", type = "password")

#     if not api_key or not external_user_id:
#         st.warning("Please enter your API key and external user ID in the sidebar.")
#         return

#     # Create session button
#     if st.button("Create Chat Session"):
#         with st.spinner("Creating chat session..."):
#             try:
#                 session_id = create_chat_session(api_key, external_user_id)
#                 st.session_state['session_id'] = session_id
#                 st.success(f"Chat session created successfully. Session ID: {session_id}")
#             except Exception as e:
#                 st.error(f"Error creating chat session: {str(e)}")

#     # Query input and submit
#     if 'session_id' in st.session_state:
#         query = st.text_input("Enter your query")
#         if st.button("Submit Query"):
#             if query:
#                 with st.spinner("Submitting query..."):
#                     try:
#                         response = submit_query(api_key, st.session_state['session_id'], query)
#                         st.json(response)
#                     except Exception as e:
#                         st.error(f"Error submitting query: {str(e)}")
#             else:
#                 st.warning("Please enter a query.")
#     else:
#         st.info("Create a chat session first before submitting queries.")

# if __name__ == "__main__":
#     main()

import streamlit as st
import requests

# --- Styling to match the Amigo chatbot interface ---
st.set_page_config(page_title="Amigo Chatbot", layout="centered")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-color: #000000;
        color: #B9F44D;
        font-family: 'Arial', sans-serif;
        text-align: center;
    }
    .header {
        font-size: 36px;
        margin-top: 30px;
        margin-bottom: 20px;
    }
    .card {
        background-color: #1E1E1E;
        padding: 20px;
        margin: 10px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .button-container {
        margin-top: 10px;
    }
    .input {
        width: 100%;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Main Title ---
st.markdown("<div class='header'>Welcome to Amigo, your personal AI chatbot</div>", unsafe_allow_html=True)

# --- Cards for options ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='card'><h4>Suggest API</h4><p>Describe your needed task. We will provide the best API and agents available on our platform.</p></div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'><h4>Error Debugging</h4><p>Enter your current error code or problems. Get precise solutions and tutorials for help needed.</p></div>", unsafe_allow_html=True)

# --- Sidebar for API key and User ID ---
st.sidebar.header("API Configuration")
api_key = st.sidebar.text_input("Enter API Key", type="password")
external_user_id = st.sidebar.text_input("Enter External User ID", type="password")

# --- Chat session creation button ---
if not api_key or not external_user_id:
    st.warning("Please enter your API key and external user ID.")
else:
    if st.button("Create Chat Session"):
        with st.spinner("Creating chat session..."):
            try:
                # Function to create chat session
                def create_chat_session(api_key, external_user_id):
                    url = 'https://api.on-demand.io/chat/v1/sessions'
                    headers = {'apikey': api_key}
                    body = {'pluginIds': [], 'externalUserId': external_user_id}
                    response = requests.post(url, headers=headers, json=body)
                    response.raise_for_status()
                    data = response.json()
                    return data['data']['id']
                
                session_id = create_chat_session(api_key, external_user_id)
                st.session_state['session_id'] = session_id
                st.success(f"Chat session created successfully! Session ID: {session_id}")
            except Exception as e:
                st.error(f"Error: {e}")

# --- Query input area ---
if 'session_id' in st.session_state:
    st.markdown("<div class='card'><h4>Chat with Amigo</h4></div>", unsafe_allow_html=True)

    query = st.text_input("Enter your query", placeholder="Type your message here...")
    if st.button("Submit Query"):
        if query:
            with st.spinner("Submitting your query..."):
                try:
                    # Function to submit a query
                    def submit_query(api_key, session_id, query):
                        url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
                        headers = {'apikey': api_key}
                        body = {
                            'endpointId': 'predefined-openai-gpt4o',
                            'query': query,
                            'pluginIds': ['plugin-1713962163', 'plugin-1718189536'],
                            'responseMode': 'sync'
                        }
                        response = requests.post(url, headers=headers, json=body)
                        response.raise_for_status()
                        return response.json()
                    
                    response = submit_query(api_key, st.session_state['session_id'], query)
                    st.json(response)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a query.")
else:
    st.info("Please create a chat session to start querying.")

