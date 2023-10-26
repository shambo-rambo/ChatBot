import streamlit as st
from streamlit_chat import message
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

# setup streamlit page
st.set_page_config(
    page_title="Hamblin GPT",
    page_icon="🤖"
)

def main():
    chat = ChatOpenAI(
        temperature=0,
        model_name="gpt-4-0613"
    )
    
    if "messages" not in st.session_state:
       st.session_state.messages = [
    SystemMessage(content="""You are a helpful assistant aiding students in crafting an essay paragraph using the S.T.E.A.L structure. The structure is defined as:
        Statement (S): A concise topic sentence answering a segment of the essay question. 
        Topic Elaboration (T): Contextualize the statement historically.
        Example (E): Reference a pertinent historical event or evidence.
        Analysis (A): Illuminate the significance of the example.
        Link (L): Round off by linking back to the essay prompt.
        
        Dynamic Evaluation: Post user input, the system should assess its quality. Praise precise inputs and offer constructive feedback on vague or off-topic ones.
        Grammar & Syntax: Highlight spelling, word choice, and grammatical inaccuracies.
        Relevance Check: Ensure user inputs align with the S.T.E.A.L structure and are contextually relevant.
        Independent Thinking: While the API provides guidance, users should be nudged to think critically and not rely solely on feedback.
        Conciseness Enforcer: Encourage inputs to be succinct, ideally below 250 words.
        Do NOT provide direct example sentences. 
        Immediately evaluate the student's input after each response: if it's excellent, acknowledge it; if not, offer 2-3 items of feedback and guidance in the form of             questions or pointers to help them improve.
        Provide feedback at every stage of the S.T.E.A.L structure and ask them to resubmit their sentence until an excellent level is achieved.
        Finally after the Link sentence how been finished print out the paragraph and them tell the student how I can further improve."""),
           
    AIMessage(content="Hello! I'm here to assist you in crafting a STEAL paragraph for your essay. I'm here to guide you, not to write for you.\n\n To begin, please share your essay question.\n\n Let's work together to make your writing shine!")
]
    st.header("Hamblin GPT 🤖")
        
    # sidebar with user input
    with st.sidebar:
        if "user_input" not in st.session_state:
            st.session_state.user_input = ""
    
        user_input = st.text_area("Your message: ", value=st.session_state.user_input, key="user_input_sidebar")
        submit_button = st.button("Submit")

        if submit_button:
            if user_input:
                st.session_state.messages.append(HumanMessage(content=user_input))
                with st.spinner("Thinking..."):
                    response = chat(st.session_state.messages)
                st.session_state.messages.append(AIMessage(content=response.content))
                st.session_state.user_input = ""  # Reset the user input in the session state

    # Moved this block out of the sidebar (corrected indentation)
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):  # start from index 1 to skip the SystemMessage
        if isinstance(msg, HumanMessage):
            message(msg.content, is_user=True, key=str(i) + '_user')
        elif isinstance(msg, AIMessage):
            message(msg.content, is_user=False, key=str(i) + '_ai')
    
    if st.button("Download Chat"):
        chat_history = ""
        for msg in st.session_state.messages:
            if isinstance(msg, HumanMessage):
                chat_history += f"User: {msg.content}\n"
            elif isinstance(msg, AIMessage):
                chat_history += f"AI: {msg.content}\n"
    
        st.download_button(
            label="Download Chat History",
            data=chat_history,
            file_name="chat_history.txt",
            mime="text/plain"
        )
            
if __name__ == '__main__':
    main()
