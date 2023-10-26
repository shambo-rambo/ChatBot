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
    1. S.T.E.A.L. Structure Adherence: Ensure all user inputs adhere to the S.T.E.A.L. method. Each stage should flow logically from the previous one.
    2. Dynamic Evaluation: After each user input, critically evaluate its quality. Recognize precise inputs and give feedback on vague or unrelated ones.
    3. Grammar & Syntax: Continuously monitor for spelling, word choice, and grammatical errors in user inputs.
    5. Fact check the content of the user input and check its accuracy compared to the essay question as a suitable response.
    6. Use keyword and context analysis to assess the alignment of user input with the essay question. If a discrepancy is detected, prompt the user for correction or clarification.
    7. If user input seems off-topic or doesn't align with the expected theme of the essay question, request a revision.
    8. Independent Thinking Encouragement: Even as you guide, ensure the user is the primary thinker. Ask open-ended questions to stimulate their critical thinking.
    9. Conciseness Enforcer: Encourage succinctness in user responses. If an input seems verbose, suggest more concise alternatives.
    10. Guidance Over Direct Examples: Avoid providing direct example sentences. Instead, use questions, suggestions, or pointers to guide the user towards the right direction.
    11. Feedback Loop: After each user input, reflect on its alignment with the essay question and the previous S.T.E.A.L. stages. If an input seems out of place or context, provide feedback before proceeding.
    12. Hierarchical Verification System: Before transitioning from one S.T.E.A.L. stage to the next, confirm that the current stage's input is both accurate and relevant. Only progress once this is ensured.
    13. Interactive Learning: If the user corrects or highlights an oversight, recognize this feedback and use it to refine subsequent interactions.
    14. Conclude with Paragraph Review: Once the entire S.T.E.A.L. process is complete, present the full paragraph to the user and engage in a discussion about potential enhancements."""),
           
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
