from datetime import datetime
import streamlit as st
import uuid
import app_components as components 
from pymongo import MongoClient
from pymongo.server_api import ServerApi 
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(layout="wide", page_title="StartupGPT") 

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("./styles.css")

if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

print(st.session_state['user_id'])

@st.cache_resource
def init_connection():
    return MongoClient(st.secrets.mongo.uri, server_api=ServerApi('1'))

client = init_connection()

#### MAIN PAGE ####
st.title("Welcome to StartupGPT")

def gather_feedback():
  return {
    "stage": st.session_state['stage'],
    "year_of_business":st.session_state['year'],
    "size": st.session_state['size'],
    "industry": st.session_state['industry'],
    #"revenue": st.session_state['revenue'],
    "location": st.session_state['location'],
    "role": st.session_state['role'],
    "birth_year": st.session_state['birth_year'],
    "ChatGPT_experience":st.session_state['gpt_experience'],
  }

def write_data(mydict):
    db = client.usertests #establish connection to the 'test_db' db
    backup_db = client.usertests_backup
    items = db.cycle_3 # return all result from the 'test_chats' collection
    items_backup = backup_db.cycle_3
    items.insert_one(mydict)
    items_backup.insert_one(mydict)

def get_user_feedback(feedback):
    user_feedback = {"Task-1":{"id": st.session_state['user_id'], "time": datetime.now(), "Chatbot_versions": "C1: dem+prompt+rag, C2: dem+rag, C3: dem", "Demographic": feedback}}
    return user_feedback

def update_chat_db(feedback):
    db = client.usertests 
    backup_db = client.usertests_backup
    user_feedback = get_user_feedback(feedback)

    print("form:", user_feedback)
    print("userid:", st.session_state['user_id'])

    print(len(list(db.cycle_3.find({"Task-1.id": st.session_state['user_id']}))))

    if len(list(db.cycle_3.find({"Task-1.id": st.session_state['user_id']}))) > 0:
        print("opdaterte chatobjekt")
        db.cycle_3.update_one({"Task-1.id": st.session_state['user_id']}, {"$set": {"Task-1.time": datetime.now(), "Task-1.Demographic": feedback}})
        backup_db.cycle_3.update_one({"Task-1.id": st.session_state['user_id']}, {"$set": {"Task-1.time": datetime.now(), "Task-1.Demographic": feedback}})

    else:
        write_data(user_feedback)
        print("lagret ny chatobjekt")


def get_selectbox_index(option_list, session_state_key):
    # """Returns the index of the current session state value in the options list, or None if not found."""
    try:
        return option_list.index(st.session_state[session_state_key])
    except (ValueError, KeyError):
        return None  # Return None to use the placeholder


def display_form():
    # """Displays the form for both new and returning users."""
    st.subheader("Demographics and consent form")
    st.write("By submitting the form you are consenting to:")
    lst3= [
        "having received and understood information about the project", 
        "the participation in this research, including communicating with chatbots and answering the questionnaire", 
        "the collection of your data as described in on this page",
        "having had the opportunity to ask questions"
    ]
    s = ''
    for i in lst3:
        s += "- " + i + "\n"
    st.markdown(s) 
    

    st.caption("Business details (Information regarding business details will be used as context by the chatbots)")
    stage_options = [
        "Seed Stage: Small team working on the development of a business plan and product, with minimal or personal funding", 
        "Early Stage: Product is introduced to the market, continued innovation is necessary, focus on building a customer base", 
        "Growth Stage: Established presence in the market and a steady customer base, focus on increasing revenue and market share", 
        "Expansion Stage: Well-established and financially stable, focus on maintaining market position and exploring new opportunities"
    ]
    year_options = [
        "<1 year", 
        "1-5 years", 
        "5-10 years", 
        ">10 years"
    ]
    gpt_exp_options = [
        "No experience: I have never used ChatGPT or have only tried it once or twice", 
        "Beginner: I have used ChatGPT a few times, but I'm still learning the basics", 
        "Intermediate: I use ChatGPT regularly and am familiar with many of its features", 
        "Experienced: I have extensive experience with ChatGPT and use it proficiently for various tasks", 
        "Advanced: I deeply understand ChatGPTs capabilities and limitations, and have possibly used it in professional or advanced projects"
    ]
   
    # https://www.ilo.org/global/industries-and-sectors/lang--en/index.htm
    # industry = ["Agriculture; plantations;other rural sectors" ,"Basic Metal Production" ,"Chemical industries" ,"Commerce", "Construction", "Education", "Financial services; professional services", "Food; drink; tobacco", "Forestry; wood; pulp and paper", "Health services", "Hotels; tourism; catering", "Mining (coal; other mining)", "Mechanical and electrical engineering", "Media; culture; graphical", "Oil and gas production; oil refining", "Postal and telecommunications services", "Public service", "Shipping; ports; fisheries; inland waterways", "Textiles; clothing; leather; footwear", "Transport (including civil aviation; railways; road transport", "Transport equipment manufacturing","Utilities (water; gas; electricity)"] 
   
    # https://www.ssb.no/en/klass/klassifikasjoner/6 
    industry = [
        "Accommodation and Food Service Activities",
        "Administrative and Support Service Activities",
        "Agriculture, Forestry and Fishing",
        "Arts, Entertainment and Recreation",
        "Construction",
        "Education",
        "Electricity, Gas, Steam and Air Conditioning Supply",
        "Financial and Insurance Activities",
        "Human Health and Social Work Activities",
        "Information and Communication",
        "Manufacturing",
        "Mining and Quarrying",
        "Professional, Scientific and Technical Activities",
        "Public Administration and Defence; Compulsory Social Security",
        "Real Estate Activities",
        "Transportation and Storage",
        "Water Supply; Sewerage, Waste Management and Remediation Activities",
        "Wholesale and Retail Trade; Repair of Motor Vehicles and Motorcycles",
        "Other"
    ]
    st.session_state['stage'] = st.selectbox("Stage", options=stage_options, index=get_selectbox_index(stage_options, 'stage'), placeholder="Select an option")
    st.session_state['year'] = st.selectbox("Year of business", year_options, index=get_selectbox_index(year_options, 'year'), placeholder="Select an option")
    st.session_state['size'] = st.number_input("Size of business", step=1, min_value=0, value=st.session_state.get('size'), placeholder="Number of employees", )
    #st.session_state['industry'] = st.text_input("Industry", value=st.session_state.get('industry', ''), placeholder="Technology, healthcare, finance, etc.")
    st.session_state['industry'] = st.selectbox("Industry", industry, index=get_selectbox_index(industry, 'industry'), placeholder="Select an option")
    # Uncomment the following line if needed
    # st.session_state['revenue'] = st.selectbox("Revenue Range", ["No revenue", "<1M NOK", "1M-10M NOK", ">10M NOK"], placeholder="Select an option") 
    st.session_state['location'] = st.text_input("Location", value=st.session_state.get('location', ''), placeholder="City, Country")

    st.caption("Personal details")
    st.session_state['role'] = st.text_input("Company Role", value=st.session_state.get('role', ''), placeholder="CEO, CTO, backend developer, UI/UX designer, etc.")
    st.session_state['birth_year'] = st.number_input("Year of birth", step=1, min_value=0, value=st.session_state.get('birth_year'), placeholder="YYYY", )
    st.session_state['gpt_experience'] = st.selectbox("Level of experience with ChatGPT", gpt_exp_options, index=get_selectbox_index(gpt_exp_options, 'gpt_experience'), placeholder="Select an option")

def handle_submit(is_new_user, submit_text):
    # """Handles the form submission for new and returning users."""
    if is_new_user:
        st.session_state['user_id'] = str(uuid.uuid4())

    st.toast("Thank you for submitting. You can still update the information and submit again")
    
    if submit_text != "Click to update form information":
        button_container.form_submit_button("Click to update form information")
        st.info("You can now access the tasks in the sidebar")
    all_feedback = gather_feedback()
    update_chat_db(all_feedback)

with st.form("test_form"):
    is_new_user = st.session_state.get('user_id') is None
    display_form()

    submit_text = "Submit demographics and consent to continue" if is_new_user else "Click to update form information"
    button_container = st.empty()

    if button_container.form_submit_button(submit_text):
        handle_submit(is_new_user, submit_text)


st.subheader("Information about the project")
st.write("This website serves as a prototype developed as part of a master thesis in Computer Science at the Norwegian University of Science and Technology (NTNU). The core objective of this project is to harness the potential of ChatGPT in empowering startups. While ChatGPT is becoming a widely used tool for businesses, tailoring it to fit the needs of different sectors can make it significantly more valuable for that particular sector. For startups this can be especially valuable due to high failure rates and lack of support. The use of AI tools such as ChatGPT as a virtual assistant can thereby help entrepreneurs save time, reduce costs, and improve productivity.")
st.write("Through this prototype we specifically aim to analyze and compare various versions of ChatGPT to identify models that best align with critical startup use cases. Obtaining real-world input is crucial in evaluating the efficacy of ChatGPT models in practical scenarios. Gaining the insights from potential users associated with startups is thereby a big help.")
st.write("The anticipated outcome of this research is a more effective use of AI tools like ChatGPT in startups. By customizing these tools to the specific needs startup companies, this project aspires to contribute to a future where more startups can thrive and succeed.")

st.subheader("Who is responsible for the research project?")
st.write("Department of Computer Science (Institutt for datateknologi og informatikk) at NTNU is responsible for the project")

st.subheader("Why are you asked to participate?")
st.write("Students and graduates in the early stages of startup development are asked to partake in this study to offer their perspectives on generative AI in startup development.")

st.subheader("What does your participation entail?")
st.write("Participation in this study includes interaction with three different chatbots, and answering the following questionnaire regarding your experiences. The time estimated for this study is about 20 minutes, 6 minutes per chatbot.")


st.subheader("Voluntary Participation")
st.write("Your participation in this study is entirely voluntary. You have the right to withdraw at any time without any negative consequences. If you wish to withdraw all the data obtained concerning you for this study is deleted immediately. You will not be able to recover your data after withdrawing. To withdraw from the study click the button below:")
withdraw_button_container = st.empty()
if st.session_state['user_id'] is None:
    withdraw_button_container.button("Click to withdraw from study", type="primary", disabled=True, help="You have not entered the study")
else:
    if withdraw_button_container.button("Click to withdraw from study", type="primary", disabled=False):
        
        print("witdrawn") ## Add modal when feature is released
        db = client.usertests
        backup_db = client.usertests_backup

        if len(list(db.cycle_3.find({"Task-1.id": st.session_state['user_id']}))) > 0:
            db.cycle_3.delete_one({"Task-1.id": st.session_state['user_id']})
            backup_db.cycle_3.delete_one({"Task-1.id": st.session_state['user_id']})

        for key in st.session_state.keys():
            del st.session_state[key]
        
        st.session_state['user_id'] = None  
        
        withdraw_button = withdraw_button_container.button("You have successfully withdrawn from the study. All data associated to you has been deleted", type="primary", disabled=True)   
        consent_button = button_container.form_submit_button('Submit and consent to data usage as described on this page')

        streamlit_js_eval(js_expressions="parent.window.location.reload()")


st.subheader("Confidentiality and Data Protection")
lst = [
    "We will only use your information for the purposes we have stated in this document.", 
    "All personal data collected during this study will be treated confidentially and in accordance with privacy regulations.", 
    "We will implement appropriate technical and organizational measures to ensure the security of your data.", 
    "Data will be anonymized", 
    "The data will be stored securely in a secure database and will only be accessible to the research team."
]
s = ''
for i in lst:
    s += "- " + i + "\n"
st.markdown(s)

st.subheader("What happens to your data when the research project is finished?")
st.write("The project is estimated to finish in the early summer of 2024. All data associated with you will be destroyed securely after this finish date.")

st.subheader("What gives us the right to handle data about you?")
st.write("We process information about you based on your consent.")
st.write("On behalf of NTNU, Sikt – The Knowledge Sector's Service Provider (Kunnskapssektorens tjenesteleverandør in Norwegian) has assessed that the processing of personal data in this project is in accordance with the data protection regulations.")

st.subheader("Rights of participants")
st.write("As long as you can be identified in the data material, you have the right to:")
lst2 = [
    "access information we process about you, and to receive a copy of the information",
    "have personal information about you deleted", 
    "send a complaint to the Norwegian Data Protection Authority (Datatilsynet) about the processing of your personal data"
]
s = ''
for i in lst2:
    s += "- " + i + "\n"
st.markdown(s)

st.subheader("Contact")
st.write("If you have any questions or feedback on the prototype, please don't hesitate to contact us!")
lst5 = [
    '<p>Researcher, Thea Lovise Ahlgren: <a href="mailto:thealah@stud.ntnu.no">thealah@stud.ntnu.no</a></p>', 
    '<p>Researcher, Helene Fønstelien Sunde: <a href="mailto:helenfs@stud.ntnu.no">helenfs@stud.ntnu.no</a></p>',
    '<p>Project supervisor, Anh Nguyen-Duc: <a href="mailto:angu@usn.no">angu@usn.no</a></p>' 
]
s = ''
for i in lst5:
    s += "- " + i + "\n"
st.markdown(s,unsafe_allow_html=True)

st.markdown("\n")
st.write("Our data protection officer:")
st.markdown('- Thomas Helgesen: <a href="mailto:thomas.helgesen@ntnu.no">thomas.helgesen@ntnu.no</a> \n', unsafe_allow_html=True)
st.write("If you have any questions related to the assessment made by the privacy services from Sikt, you can contact them via:")
st.markdown('<p>Epost: <a href="mailto:personverntjenester@sikt.no">personverntjenester@sikt.no</a> or phone: 73 98 40 40.</p>', unsafe_allow_html=True)

####### SIDEBAR #######
components.sidebar_nav(st.session_state['user_id'] is None)

