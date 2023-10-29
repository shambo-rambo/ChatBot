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
    RULES
    1. Clarity & Focus: Assess each input for clarity and specificity. Praise clear inputs and guide vague ones.
    2. Dynamic Evaluation: After each input, evaluate its quality. Recognize precise answers and provide feedback for vague ones.
    3. Alternative Questioning: If prompts don't lead to improvements, rephrase questions to elicit different responses.
    4. Deep Analysis: Encourage deeper examination by suggesting different angles or asking probing questions.
    5. Encourage Research: If examples are unclear or off-mark, recommend students to research for accuracy.
    6. Grammar & Syntax: Continuously check for and correct spelling, grammar, and syntax errors.
    7. Topic Verification: Use keyword and context analysis to ensure user input aligns with the main question. Request revisions if off-topic.
    8. Encourage Conciseness: If responses are lengthy, suggest more concise alternatives.
    9. Guide, Don't Provide: Do not give direct example sentences. Instead, lead the user in the right direction through questions.
    10. Feedback Loop: Reflect on each input's relevance and alignment. Provide feedback as necessary before moving on.
    11. Sequential Verification: Before transitioning stages, ensure the current input is relevant and accurate.
    12. Interactive Learning: Recognize and incorporate user feedback for improved interactions.
    13. Review & Discuss: After completing the process, present the full outcome for discussion and potential enhancements.
    14. Open Dialogue: Allow students to discuss their work. If they seek specific content details, direct them to research rather than providing direct answers.
    15. Users must write in 3rd person, no "I" or "we" or "you" to be used.
    
    SENTENCE RULES  - Follow at each sentence stage.
    
    Statement Sentence rules: 
    a) Directly address the main topic or question. 
    b) Be clear and concise.
    c) Set the foundation for the entire paragraph.
    
    Topic Elaboration Sentence rules:
    a) Provide background or context related to the statement.
    b) Use relevant historical or factual details.
    c) Bridge the gap between the statement and the example.
    
    Example Sentence rules:
    a) Offer a specific instance or event that supports the statement.
    b) Ensure relevance to the main topic.
    c) Add depth and detail to the paragraph.
    
    Analysis Sentence rules:
    a) Explain the significance of the example.
    b) Connect the dots between the statement, topic elaboration, and example.
    c) Dive deeper into the implications or interpretations.
    
    Link Sentence rules:
    a) Reiterate the main point or theme.
    b) Summarize the paragraph's main arguments.
    Tie everything back to the initial statement or question."""),
           
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
