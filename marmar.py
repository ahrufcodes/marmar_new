import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Using the OPENAI_API_KEY environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')


# UI configurations
st.set_page_config(page_title="Marmar", page_icon="💊")
custom_css = """
<style>
    /* editing title */
    h1 {
        font-size: 24px;
        color: #033F3C;
        padding: 0px 0px 40px 0px;
    }
    .stButton > button {
        background-color: #033F3C;
        color: #ffffff;
    }
    .stButton > button:hover {
        background-color: white;
        color: #033F3C;
    }
</style>
"""
# Inject custom CSS with markdown
st.markdown(custom_css, unsafe_allow_html=True)

# Display an Image Banner
st.image('img/banner.png', use_column_width=True)

# Streamlit app interface 
st.title('Marmar: Empowering you with the knowledge and tools to safely manage your medications.')
st.write('Welcome to Marmar. Check potential drug interactions and get tailored advice. Please provide the details below to get started.')

# Compulsory field for medications
medications = st.text_area('Enter the names of the medications you are currently taking, separated by commas:', help='Please enter the names of the medications you are currently taking, separated by commas.')
health_history = st.text_area('Enter your health history or describe any ailments:', help='Please include any chronic conditions, recent illnesses, or relevant health issues.')


# Optional fields for personalized advice
options = ['Male', 'Female']
gender = st.selectbox('Choose your gender:', options)
age = st.text_input('Enter your age (Optional):', '')
weight = st.text_input('Enter your weight in kg (Optional):', '')
height = st.text_input('Enter your height in cm (Optional):', '')

# # Reminder for users to consult with a healthcare provider for professional advice
# text_reduced_opacity = "We appreciate you choosing MarMar for your medication management needs. Please note, MarMar is designed to support, not substitute, the guidance of healthcare professionals. For advice specific to your health concerns, make sure to consult with your doctor or healthcare provider."
# #custom opacity for reducing the text opacity
# st.markdown(f'<span style="opacity: 0.5;">{text_reduced_opacity}</span>', unsafe_allow_html=True)

# Function to check drug interactions
def check_drug_interactions(medications, health_history, gender="", age="", weight="", height=""):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a knowledgeable assistant trained to provide information on drug interactions, but first classify the risk of interaction only into (Severe, Mild, Moderate) and then offer tailored health advice taking into account the patient's health history and personal details."
                },
                {
                    "role": "user",
                    "content": #f"Provide a detailed explanation of the potential risks and interactions among these medications: {medications}. then take the patient's {health_history} into account."
                               f"Given the health history: {health_history}, provide a detailed explanation of the potential risks and interactions among these medications: {medications}."
                               f"Focus on any increased risks, specific side effects, and the mechanism by which"
                               f"these interactions might occur, also considering the health history. Include any relevant studies or findings that have implicated these drugs in such conditions. "
                               f"Ensure the explanation is comprehensive, covering the pharmacological aspects and clinical implications for patients. "
                               f"Then, based on gender: {gender}, age: {age}, weight: {weight}, height: {height}, and health history{health_history}, offer tailored advice."
                }
            ],
            max_tokens=1000,  # Limiting the output to 1000 tokens
        
        )
        # Response will be structured appropriately(it's just  to get a cleaned up response)
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Button to initiate the drug interaction check
if st.button('Check Interactions'):
    warning_users = "<p style='color: #BABABA; opacity:.7;'>  We appreciate you choosing MarMar for your medication management needs. Please note, MarMar is designed to support, not substitute, the guidance of healthcare professionals. For advice specific to your health concerns, make sure to consult with your doctor or healthcare provider.'  </p>" 
    st.markdown(warning_users, unsafe_allow_html=True)
    if medications and health_history:
        response = check_drug_interactions(medications, health_history, gender, age, weight, height)
        
        #split the response 
        parts = response.split('\n', 1)  # Splitting by newline, adjust if AI uses a different format
        
        if len(parts) == 2:
            severity, explanation = parts
            st.write('**Interaction Severity:**', severity)
            st.write('**Explanation:**', explanation)
        else:
            # If the response doesn't follow the expected format, display it as is
            st.write('**Response:**', response)
    else:
        st.warning('Please enter the required information to continue.')



# Footer
footer="""<style>
a:link , a:visited{
color: #BADEDC;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: #033F3C;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: transparent;
color: #64928F;
text-align: center;
}
</style>
<div class="footer">
<p> Developed with ❤️ by <a href="https://github.com/ahrufcodes" target="_blank">ahruf</a> <a style='display: block; text-align: center;' href="https://ahruf.notion.site/About-Marmar-6e1c9dc286e84884bd7a62e6ec76cca4?pvs=4" target="_blank">About marmar</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)