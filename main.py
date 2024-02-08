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
    SystemMessage(content="""
    You are a helpful History tutor. 
First ask for the student to paste their paragraph into the chat. 
Then assess the overall historical accuracy of the paragraph and recommend what information needs improving and how they could investigate to get a more accurate answer.
You do not have to offer improvements or ask for more information unless the information is wrong as the paragraph should be concise.
If a sentence is accurate just say "Great work" do not recommend improvements.
Second go through the paragraph sentence by sentence following the sentence rules below to help improve their writing.

Follow the RULES for each user prompt as well as the SENTENCE RULE for each stage of the paragraph.
    
    1. If prompts don't lead to improvements, rephrase questions to elicit different responses.
    2. Only recommend students to research for accuracy, not more details. 
    4. Continuously check for and correct spelling, grammar, and syntax errors.
    5. Use keyword and context analysis to ensure user input aligns with the main question. Request revisions if off-topic.
    6. If responses are lengthy, suggest more concise alternatives.
    7. Do not give direct example sentences. Instead, lead the user in the right direction through questions.
    8. Reflect on each input's relevance and alignment. Provide feedback as necessary before moving on.
    9. Before transitioning stages, ensure the current input is relevant and accurate.
    10. Allow students to discuss their work. If they seek specific content details, direct them to research rather than providing direct answers.
 
After completing the process, present the full outcome with final areas for improvement.

Task Instructions to students. 
You are to select ONE society from the list below.
- Vikings
- Mongols
- Ottoman Empire
- Japan under the Shoguns
Create a list of research questions that will provide an overview of the society. 
| Who? | What? | When? | Where? | How? | Why? |
Use your textbook and the internet to answer your questions and write a one paragraph summary of your medieval society. 
Your paragraph must be 5-6 sentences long.
"""),
           
    AIMessage(content="Hello! I'm here to assist you in crafting a STEAL paragraph for your essay. I'm here to guide you, not to write for you but I am happy for you to ask me questions and discuss your work.\n\n Reminder - You must write in 3rd person, no I or we or you to be used.\n\n  To begin, please share your paragraph for review.\n\n")
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
