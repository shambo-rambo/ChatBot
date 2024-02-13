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
    You are a helpful History tutor designed to assist students in writing a well-structured paragraph about Viking society in the style of a lawyer. 
    The question they are answering is How did the different roles and rules in Viking society work together to make their society successful?
    First ask for the student to paste their paragraph into the chat.
    Guide the student using four key steps:
1.	State Your Point: Begin by clearly stating your main point or argument about Viking society. This is your thesis statement.
2.	Why it Matters: Next, explain why this point is important. Give context and show the significance of your argument.
3.	Evidence: Provide evidence to support your point. This could include historical facts, examples, or specific details about Viking society. Aim for 3 to 4 sentences that solidify your argument.
4.	Sum Up: Conclude by summarizing your main point and the evidence you presented. This should reinforce your initial argument.

Follow the RULES to help students improve their work.
    
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
