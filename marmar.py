import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Using the OPENAI_API_KEY environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')


def check_drug_interactions(medications, age="", weight="", height=""):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a knowledgeable assistant trained to provide information on drug interactions, but first classify the risk of interaction only into (severe, mild, moderate) and offer tailored health advice."
                },
                {
                    "role": "user",
                    "content": f"Provide a detailed explanation of the potential risks and interactions among these medications: {medications}. "
                               f"Focus on any increased risks, specific side effects such as increased intracranial pressure, and the mechanism by which "
                               f"these interactions might occur. Include any relevant studies or findings that have implicated these drugs in such conditions. "
                               f"Ensure the explanation is comprehensive, covering the pharmacological aspects and clinical implications for patients. "
                               f"Then, based on age: {age}, weight: {weight}, and height: {height}, offer tailored advice."
                }
            ],
            max_tokens=400,  # Limiting the output to 350 tokens
        
        )
        # Response will be structured appropriately
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit app interface 
st.title('Marmar: We are making every Dose Safer.')
st.write('Welcome to Marmar. Check potential drug interactions and get tailored advice.')

# Compulsory field for medications
medications = st.text_area('Enter the names of the medications you are currently taking, separated by commas:', help='This field is compulsory.')


# Optional fields for personalized advice
age = st.text_input('Enter your age (Optional):', '')
weight = st.text_input('Enter your weight in kg (Optional):', '')
height = st.text_input('Enter your height in cm (Optional):', '')

# Button to initiate the drug interaction check
if st.button('Check Interactions'):
    if medications:
        response = check_drug_interactions(medications, age, weight, height)
        
        #split the response into severity and explanation
        parts = response.split('\n', 1)  # Splitting by newline, adjust if AI uses a different format
        
        if len(parts) == 2:
            severity, explanation = parts
            st.write('**Interaction Severity:**', severity)
            st.write('**Explanation:**', explanation)
        else:
            # If the response doesn't follow the expected format, display it as is
            st.write('**Response:**', response)
    else:
        st.warning('Please enter the required information for medications.')

# Reminder for users to consult with a healthcare provider for professional advice
st.write('We appreciate you choosing MarMar for your medication management needs. Please note, MarMar is designed to support, not substitute, the guidance of healthcare professionals. For advice specific to your health concerns, make sure to consult with your doctor or healthcare provider.')



# Footer
footer="""<style>
a:link , a:visited{
color: #ffffff;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: white;
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
