import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from st_pages import add_indentation,hide_pages
import extra_streamlit_components as stx
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page
import app_components as components 

st.set_page_config(layout = "wide", page_title="StartupGPT")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("./styles.css") 

@st.cache_resource
def init_connection():
    return MongoClient(st.secrets.mongo.uri, server_api=ServerApi('1'))

client = init_connection()

def init_cookies():
  states = ["c1_option_1", "c1_option_2", "c1_option_3", "c1_perfer", "c1_comment", 
            "c2_option_1", "c2_option_2", "c2_option_3", "c2_perfer", "c2_comment", 
            "c3_option_1", "c3_option_2", "c3_option_3", "c3_perfer", "c3_comment", 
            "c4_option_1", "c4_option_2", "c4_option_3", "c4_perfer", "c4_comment", 
            "final"]

  for state in states:
    if state not in st.session_state:
       st.session_state[state] = ''

init_cookies()

####### SIDEBAR #######
components.sidebar_nav(False)

### HEADER ###
components.sticky_header("Chatbot 3", "Feedback", "None")

#### MAIN CONTENT ####
if('user_id' not in st.session_state):
    st.write("You need to consent in the \"Home\" page to get access")
    switch_page("Chatbot")
    
def write_data(mydict):
    db = client.usertests #establish connection to the 'test_db' db
    backup_db = client.usertests_backup
    items = db.cycle_1 # return all result from the 'test_chats' collection
    items_backup = backup_db.cycle_1
    items.insert_one(mydict)
    items_backup.insert_one(mydict)

def get_user_feedback(feedback):
    user_feedback = {"Task-1":{"id": st.session_state['user_id'], "time": datetime.now(), "Feedback": feedback}}
    return user_feedback

def update_chat_db(feedback):
    db = client.usertests 
    user_feedback = get_user_feedback(feedback)
    backup_db = client.usertests_backup

    print("feedback:", user_feedback)
    print("userid:", st.session_state['user_id'])

    print(len(list(db.cycle_1.find({"Task-1.id": st.session_state['user_id']}))))

    if len(list(db.cycle_1.find({"Task-1.id": st.session_state['user_id']}))) > 0:
        print("opdaterte chatobjekt")
        db.cycle_1.update_one({"Task-1.id": st.session_state['user_id']}, {"$set": {"Task-1.time": datetime.now(), "Task-1.Feedback": feedback}})
        backup_db.cycle_1.update_one({"Task-1.id": st.session_state['user_id']}, {"$set": {"Task-1.time": datetime.now(), "Task-1.Feedback": feedback}})

    else:
        write_data(user_feedback)
        print("lagret ny chatobjekt")

def gather_feedback():
  return {
    "effective":{
      "chatbot_1":st.session_state['c1_option_1'],
      "chatbot_2":st.session_state['c1_option_2'],
      "chatbot_3":st.session_state['c1_option_3'],
      "comment": st.session_state['c1_comment'],
      "perferred_chatbot": st.session_state['c1_perfer']
    },

    "efficient":{
      "chatbot_1":st.session_state['c2_option_1'],
      "chatbot_2":st.session_state['c2_option_2'],
      "chatbot_3":st.session_state['c2_option_3'],
      "comment": st.session_state['c2_comment'],
      "perferred_chatbot": st.session_state['c2_perfer']
    },

    "reliable":{
     "chatbot_1":st.session_state['c3_option_1'],
      "chatbot_2":st.session_state['c3_option_2'],
      "chatbot_3":st.session_state['c3_option_3'],
      "comment": st.session_state['c3_comment'],
      "perferred_chatbot": st.session_state['c3_perfer']
    },

    "satifactory":{
      "chatbot_1":st.session_state['c4_option_1'],
      "chatbot_2":st.session_state['c4_option_2'],
      "chatbot_3":st.session_state['c4_option_3'],
      "comment": st.session_state['c4_comment'],
      "perferred_chatbot": st.session_state['c4_perfer']
    },

    "final_comment":st.session_state['final']
  }

if "disabled" not in st.session_state:
    st.session_state["disabled"] = False

def disable():
    st.session_state["disabled"] = True

#------------- Form ------------------------   

st.caption("Please rate your experience with the chat based on the following criteria:")

selectionbox_options = ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]
preferation_options = ["Chatbot 1", "Chatbot 2", "Chatbot 3", "No difference"]

def get_selected_option(selection_type, selected):
  value = st.session_state[selected]
  return None if value == '' or value == None else selection_type.index(value)

#Effectiveness
st.subheader("Effectiveness")
with st.expander(":bulb:  Effectiveness explenation", expanded=True): #Kan legge til ,True hvis den skal være åpen som default
  # st.write("Correctness indicates ..... .....")
  lst = ["To which degree does the chatbot provide you with answers that are accurate, precise and complete.", "Answers are correct and relevant, with no significant part lacking from the answer, and that all the users questions and subquestions are answered."]
  s = ''
  for i in lst:
      s += "- " + i + "\n"
  st.markdown(s)


st.markdown("**Chatbot 1**")
c1_option_1 = st.selectbox('​​To what degree did you feel the answers you received correspond with the **Effectiveness**-attribute for **Chatbot 1**',selectionbox_options,placeholder="Choose an option",index=get_selected_option(selectionbox_options, "c1_option_1"))
st.session_state['c1_option_1'] = c1_option_1

# c1_txt_1 = st.text_area(
# "Comment on **Effectiveness** for **Chatbot 1**",
# value=st.session_state['c1_txt_1'],placeholder="Comment"
# )
# st.session_state['c1_txt_1'] = c1_txt_1

st.markdown("**Chatbot 2**")
c1_option_2 = st.selectbox('​​To what degree did you feel the answers you received correspond with the **Effectiveness**-attribute for **Chatbot 2**',selectionbox_options,placeholder="Choose an option",index=get_selected_option(selectionbox_options, "c1_option_2"))
st.session_state['c1_option_2'] = c1_option_2

# c1_txt_2 = st.text_area(
# "Comment on **Effectiveness** for **Chatbot 2**",
# value=st.session_state['c1_txt_2'],placeholder="Comment"
# )
# st.session_state['c1_txt_2'] = c1_txt_2

st.markdown("**Chatbot 3**")
c1_option_3 = st.selectbox('​​To what degree did you feel the answers you received correspond with the **Effectiveness**-attribute for **Chatbot 3**',selectionbox_options,placeholder="Choose an option",index=get_selected_option(selectionbox_options, "c1_option_3"))
st.session_state['c1_option_3'] = c1_option_3

c1_prefer = st.selectbox(
   "**Which chatbot do you think gave the most effective answers?**",
   preferation_options,
   index=get_selected_option(preferation_options, "c1_perfer"),
   placeholder="Select chatbot",
)
st.session_state['c1_perfer'] = c1_prefer

c1_comment = st.text_area(
"Is there anything you want to claryfy regarding the **Effectiveness** of any of the chatbots?",
value=st.session_state['c1_comment'],placeholder="Comment"
)
st.session_state['c1_comment'] = c1_comment

#Efficiency
st.subheader("Efficiency")
with st.expander(":bulb:  Efficiency explenation", expanded=True):
  # st.write("Completeness indicates ..... .....")
  lst = ['The system should provide useful answers without the users needing to write too many prompts to specify what type of answer they are after.', 'How efficient the system is at catching what the users are after and providing a useful answer, with minimal user effort. ']
  s = ''
  for i in lst:
      s += "- " + i + "\n"
  st.markdown(s)

st.markdown("**Chatbot 1**")
c2_option_1 = st.selectbox('​​To what degree did you feel the answers you received correspond with the **Efficiency**-attribute for **Chatbot 1**',selectionbox_options,placeholder="Choose an option",index=get_selected_option(selectionbox_options, "c2_option_1"))
st.session_state['c2_option_1'] = c2_option_1
# c2_txt_1 = st.text_area(
# "Comment on **Efficiency** for **Chatbot 1**",
# value=st.session_state['c2_txt_1']
# )
# st.session_state['c2_txt_1'] = c2_txt_1

st.markdown("**Chatbot 2**")
c2_option_2 = st.selectbox('​​To what degree did you feel the answers you received correspond with the **Efficiency**-attribute for **Chatbot 2**',selectionbox_options,placeholder="Choose an option",index=get_selected_option(selectionbox_options, "c2_option_2"))
st.session_state['c2_option_2'] = c2_option_2
# c2_txt_2 = st.text_area(
# "Comment on  **Efficiency** for **Chatbot 2**",
# value=st.session_state['c2_txt_2'], placeholder="Comment"
# )
# st.session_state['c2_txt_2'] = c2_txt_2

st.markdown("**Chatbot 3**")
c2_option_3 = st.selectbox('​​To what degree did you feel the answers you received correspond with the **Efficiency**-attribute for **Chatbot 3**',selectionbox_options,placeholder="Choose an option",index=get_selected_option(selectionbox_options, "c2_option_3"))
st.session_state['c2_option_3'] = c2_option_3

c2_prefer = st.selectbox(
   "**Which chatbot do you think gave the most efficient answers**",
   preferation_options,
   index=get_selected_option(preferation_options, "c2_perfer"),
   placeholder="Select chatbot",
)
st.session_state['c2_perfer'] = c2_prefer

c2_comment = st.text_area(
"Is there anything you want to claryfy regarding the **Efficiency** of any of the chatbots?",
value=st.session_state['c2_comment'],placeholder="Comment"
)
st.session_state['c2_comment'] = c2_comment

#Reliability
st.subheader("Reliability")
with st.expander(":bulb:  Reliability explenation", expanded=True):
  #st.write("Consinstency indicates ..... .....")
  lst = ['The answers have no apparent errors, and the users trust the correctness of the answers.']
  s = ''
  for i in lst:
      s += "- " + i + "\n"
  st.markdown(s)

st.markdown("**Chatbot 1**")
c3_option_1 = st.selectbox('​To what degree did you feel the answers you received correspond with the **Reliability**-attribute for **Chatbot 1**',selectionbox_options,placeholder="Choose an option",index=get_selected_option(selectionbox_options, "c3_option_1"))
st.session_state['c3_option_1'] = c3_option_1
# c3_txt_1 = st.text_area(
# "Comment on **Reliability** for **Chatbot 1**",
# value=st.session_state['c3_txt_1'],placeholder="Comment"
# )
# st.session_state['c3_txt_1'] = c3_txt_1

st.markdown("**Chatbot 2**")
c3_option_2 = st.selectbox('​To what degree did you feel the answers you received correspond with the **Reliability**-attribute for **Chatbot 2**',selectionbox_options,placeholder="Choose an option",index=get_selected_option(selectionbox_options, "c3_option_2"))
st.session_state['c3_option_2'] = c3_option_2
# c3_txt_2 = st.text_area(
# "Comment on  **Reliability** for **Chatbot 2**",
# value=st.session_state['c3_txt_2'],placeholder="Comment"
# )
# st.session_state['c3_txt_2'] = c3_txt_2

st.markdown("**Chatbot 3**")
c3_option_3 = st.selectbox('​​To what degree did you feel the answers you received correspond with the **Reliability**-attribute for **Chatbot 3**',selectionbox_options,placeholder="Choose an option",index=get_selected_option(selectionbox_options, "c3_option_3"))
st.session_state['c3_option_3'] = c3_option_3

c3_prefer = st.selectbox(
   "**Which chatbot do you think gave the most reliable answers**",
   preferation_options,
   index=get_selected_option(preferation_options, "c3_perfer"),
   placeholder="Select chatbot",
)
st.session_state['c3_perfer'] = c3_prefer

c3_comment = st.text_area(
"Is there anything you want to claryfy regarding the **Reliability** of any of the chatbots?",
value=st.session_state['c3_comment'],placeholder="Comment"
)
st.session_state['c3_comment'] = c3_comment

#Satisfaction
st.subheader("Satisfaction")
with st.expander(":bulb:  Satisfaction explenation", expanded=True):
  #st.write("Consinstency indicates ..... .....")
  lst = ['How pleased the user is with the overall quality of the answers and that the answers are percieved as usefull and contextually correct.']
  s = ''
  for i in lst:
      s += "- " + i + "\n"
  st.markdown(s)

st.markdown("**Chatbot 1**")
c4_option_1 = st.selectbox('​To what degree did you feel the answers you received correspond with the **Satisfaction**-attribute for **Chatbot 1**',selectionbox_options,placeholder="Choose an option",index=get_selected_option(selectionbox_options, "c4_option_1"))
st.session_state['c4_option_1'] = c4_option_1

# c4_txt_1 = st.text_area(
# "Comment on **Satisfaction** for **Chatbot 1**",
# value=st.session_state['c4_txt_1'],placeholder="Comment"
# )
# st.session_state['c4_txt_1'] = c4_txt_1

st.markdown("**Chatbot 2**")
c4_option_2 = st.selectbox('​To what degree did you feel the answers you received correspond with the **Satisfaction**-attribute for **Chatbot 2**',selectionbox_options,placeholder="Choose an option",index=get_selected_option(selectionbox_options, "c4_option_2"))
st.session_state['c4_option_2'] = c4_option_2
# c4_txt_2 = st.text_area(
# "Comment on  **Satisfaction** for **Chatbot 2**",
# value=st.session_state['c4_txt_2'],placeholder="Comment"
# )
# st.session_state['c4_txt_2'] = c4_txt_2

st.markdown("**Chatbot 3**")
c4_option_3 = st.selectbox('​​To what degree did you feel the answers you received correspond with the **Satisfaction**-attribute for **Chatbot 3**',selectionbox_options,placeholder="Choose an option",index=get_selected_option(selectionbox_options, "c4_option_3"))
st.session_state['c4_option_3'] = c4_option_3

c4_prefer = st.selectbox(
   "**Which chatbot do you think gave the most satifactory answers**",
   preferation_options,
   index=get_selected_option(preferation_options, "c4_perfer"),
   placeholder="Select chatbot",
)
st.session_state['c4_perfer'] = c4_prefer

c4_comment = st.text_area(
"Is there anything you want to claryfy regarding the **Satisfaction** of any of the chatbots?",
value=st.session_state['c4_comment'],placeholder="Comment"
)
st.session_state['c4_comment'] = c4_comment

#Final comments
st.subheader("Final comments")
final_txt = st.text_area(
"Do you have any final comments that you would like us to know",
value=st.session_state['final'],placeholder="Comment"
)
st.session_state['final'] = final_txt
# Every form must have a submit button. Fix what happends on submit
submitted = st.button(
  "Submit", on_click=disable, disabled=st.session_state.disabled
)


if submitted:
  print("Form has been submitted")
  all_feedback = gather_feedback()
  update_chat_db(all_feedback)
  st.info("Thank you for giving us your feedback!")

   

   
   
