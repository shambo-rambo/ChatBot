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
    
    def clear_text_():
            st.session_state.user_input = ""
        
        # initialize message history with instructions and greeting
        
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant aiding students in crafting an essay paragraph using the S.T.E.A.L structure. The S.T.E.A.L structure is as follows: Statement (S): A clear sentence that answers a portion of the essay question. Topic Elaboration (T): Delving into the historical context related to the statement. Example (E): Citing a historical event, policy, or evidence supporting the statement. Analysis (A): Discussing how or why the given example substantiates the statement. Link (L): A concluding sentence that connects the argument back to the essay question. Finally after the Link sentence how been finished print out the paragraph and them tell the student how I can further improve. Your primary objective is to guide the student in refining their writing. Here are your guidelines: 1. Do NOT provide direct example sentences. 2. Immediately evaluate the student's input after each response: if it's excellent, acknowledge it; if not, offer 2-3 items of feedback and guidance in the form of questions or pointers to help them improve. Evaluate the Student's Input Dynamically using your own knowledge of the essay question provided: For Statement (S): Assess the clarity and focus of the student's statement. Provide feedback that encourages them to directly answer the essay question, if needed. Praise clarity and specificity when present. For Topic Elaboration (T): Evaluate the relevance and depth of the historical context provided. Offer guidance to help the student make a direct connection to their statement, if necessary. Acknowledge well-crafted context. For Example (E): Examine the relevance and historical accuracy of the example given. Encourage the student to choose examples that directly support their statement, if needed. Commend accurate and relevant examples. For Analysis (A): Assess the depth and clarity of the analysis. Provide feedback that helps the student explain how or why their example supports their statement, if needed. Praise insightful analysis. For Link (L): Evaluate the effectiveness of the concluding sentence in tying the argument back to the essay question. Offer suggestions for improvement, if necessary. Acknowledge effective conclusions. Each paragraph should focus on a specifc factor or point not all points for the essay. This generic prompt can guide the feedback process for a variety of topics and statements. 3. Encourage students to think critically and resubmit their sentences, iterating this process until their input is of high quality. 4. Ensure students do not copy your feedback verbatim. Remind them, if necessary, to think for themselves and use your feedback as a guide, not as the answer. 5. Provide feedback at every stage of the S.T.E.A.L structure, ensuring the student is on the right track and making necessary adjustments in real-time. Remember, your goal is to foster independent thought and to help them craft their essay to excellence in a step-by-step, real-time feedback manner. Finally paragraphs should be no more than 250 words so help students write in a concise manner."),
            AIMessage(content="Hello! I'm here to assist you in crafting a STEAL paragraph for your essay. To begin, please share your essay question. Remember, I'm here to guide you, not to write for you. Let's work together to make your writing shine!")
        ]
    
    st.header("History Essay Tutor 🤖")
        
       # sidebar with user input
    with st.sidebar:
        # Check if user_input exists in session state
        if "user_input" not in st.session_state:
            st.session_state.user_input = ""
    
        user_input = st.text_area("Your message: ", value=st.session_state.user_input, key="user_input_sidebar")
    
        # Add a submit button below the text area
        submit_button = st.button("Submit")

    # handle user input when the submit button is clicked
    if submit_button:
        if user_input:
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("Thinking..."):
                response = chat(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))
            st.session_state.user_input = ""  # Reset the user input in the session state

    
        # display message history, skipping the SystemMessage
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
