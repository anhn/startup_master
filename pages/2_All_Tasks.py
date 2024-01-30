import streamlit as st
from st_pages import add_indentation, hide_pages
import extra_streamlit_components as stx


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("./styles.css")
####### SIDEBAR #######
# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
add_indentation()
hide_pages(["Chatbot_1", "Chatbot_2", "Feedback", "Task_Information"])
#show_pages_from_config()




@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()
cookie_manager.get_all()

# Fetch a specific cookie
user_consent_cookie = cookie_manager.get(cookie="kjeks")

with st.sidebar:
    st.write("Your tasks")
    with st.expander("Task 1", expanded=True):
        if user_consent_cookie:
            task_info = f"""
            <a href="Task_Information" target = "_self">
            <button class="not_clicked">
                Task information
            </button></a>
                """
            st.markdown(task_info, unsafe_allow_html=True)

            c1 = f"""
            <a href="Chatbot_1" target = "_self">
            <button class="not_clicked">
                Chatbot 1
            </button></a>
                """
            st.markdown(c1, unsafe_allow_html=True)

            c2 = f"""
            <a href="Chatbot_2" target = "_self">
            <button class="not_clicked">
                Chatbot 2
            </button></a>
                """
            st.markdown(c2, unsafe_allow_html=True)

            feedback = f"""
            <a href="Feedback" target = "_self">
            <button class="not_clicked">
                Feedback
            </button></a>
                """
            st.markdown(feedback, unsafe_allow_html=True)

        else:
            task_info = f"""
            <a href="Task_Information" target = "_self">
            <button type="button" class="not_clicked">
                Task information
            </button></a>
                """
            st.markdown(task_info, unsafe_allow_html=True)

            c1 = f"""
            <a href="Chatbot_1" target = "_self">
            <button type="button" class="disabeled" disabled>
                Chatbot 1
            </button></a>
                """
            st.markdown(c1, unsafe_allow_html=True)

            c2 = f"""
            <a href="Chatbot_2" target = "_self">
            <button type="button" class="disabeled" disabled>
                Chatbot 2
            </button></a>
                """
            st.markdown(c2, unsafe_allow_html=True)

            feedback = f"""
            <a href="Feedback" target = "_self">
            <button type="button" class="disabeled" disabled>
                Feedback
            </button></a>
                """
            st.markdown(feedback, unsafe_allow_html=True)