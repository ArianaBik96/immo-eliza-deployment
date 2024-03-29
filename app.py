import streamlit as st
import os
import json 
import pandas as pd
import base64
from streamlit import session_state as st_session
from predict_houses import predict_house_price 
from predict_apartments import predict_apartment_price 

st.set_page_config(page_title="Price prediction", page_icon=':house:', layout='wide')

class SessionState:
    def __init__(self):
        self.selected_property = None

# Function to get or create session state
def get_session_state():
    session = getattr(st, '_session_state', None)
    if session is None:
        session = st._session_state = SessionState()
    return session



def import_postalcode(folder,file):
    file_path = os.path.join(folder,file)

    # Load the data from the JSON file into the postcode_mapping dictionary
    with open(file_path, "r") as file:
        postcode_mapping = json.load(file)

    return postcode_mapping

# Function to auto-fill region, province, district, and locality based on postcode
def autofill_fields(postcode_mapping):
    if postcode in postcode_mapping:
        region = postcode_mapping[postcode]["region"]
        province = postcode_mapping[postcode]["province"]
        district = postcode_mapping[postcode]["district"]
        locality = postcode_mapping[postcode]["locality"]
        latitude_str = postcode_mapping[postcode]["latitude"]
        longitude_str = postcode_mapping[postcode]["longitude"]
        
        # Convert latitude and longitude to float if not None
        latitude = float(latitude_str) if latitude_str is not None else 0.0  # Set default value if None
        longitude = float(longitude_str) if longitude_str is not None else 0.0  # Set default value if None
    else:
        region = ""
        province = ""
        district = ""
        locality = ""
        latitude = 0.0
        longitude = 0.0

    return region, province, district, locality, latitude, longitude

def set_background_image(image_path):
    # Load image from file
    with open(image_path, "rb") as img_file:
        img_bytes = img_file.read()

    # Encode image to base64
    encoded_img = base64.b64encode(img_bytes).decode()

    # Define CSS for the background image and overlay
    page_bg_img = f"""
    <style>
        .background-container {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url('data:image/png;base64,{encoded_img}');
            background-size: cover;
        }}
        .overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.90);  
        }}
    </style>
    """

    # Render the background image and overlay
    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.write('<div class="background-container"></div>', unsafe_allow_html=True)
    st.write('<div class="overlay"></div>', unsafe_allow_html=True)


    
def get_property_buttons():
    session = get_session_state()

    col1, col2 = st.columns([1, 1])

    container_style = (
        "display: flex; justify-content: center; margin-bottom: 20px;"
    )

    # Start the container
    st.write(f"<div style='{container_style}'>", unsafe_allow_html=True)

    # Button for House type
    with col1:
        if st.button("🏠", key="house_button"):
            session.selected_property = "House"        

    # Button for Apartment type
    with col2:
        if st.button("🏢", key="apartment_button"):
            session.selected_property = "Apartment"

    # End the container
    st.write("</div>", unsafe_allow_html=True)

    # Display the selected type
    if session.selected_property is not None:
        st.write("You selected:", session.selected_property)

    # Custom CSS for the button style
    button_custom_css = """
    <style>
        button[data-testid="baseButton-secondary"] {
            padding: 20px 40px;
            font-size: 80px; /* Adjusted font size for the button */
            margin-bottom: 10px;
            color: white;
            border: none;
            border-radius: 5px;
            background-color: #2D2D2D;
            display: inline-block;
            margin-inline-start: 5px; /* Adjusted margin between buttons */
            margin-inline-end: 5px;
            margin-block-start: 0px; /* Override paragraph margin */
            margin-block-end: 0px;
        }
    </style>
    """
    # Inject custom CSS
    st.markdown(button_custom_css, unsafe_allow_html=True)
    
    return session.selected_property


def get_property_type():
    type_of_property = st.radio("Select property type:", ["House", "Apartment"])
    return type_of_property

def handle_prediction(data_new_property, type_of_property):

    if type_of_property == 'House':
        # Call the predict function with appropriate data
        predicted_price = predict_house_price(data_new_property)
    elif type_of_property == 'Apartment':
        predicted_price = predict_apartment_price(data_new_property)
    else:
        st.write("DIDN'T GET HOUSE OR APARTMENT")
    # Display the predicted price
    return predicted_price
        

white_text_css = """
    <style>
        p, h1, h2, h3, h4, h5, h6 {
            color: white !important;
        }
    </style>
"""

# Inject custom CSS to change text color to white
st.markdown(white_text_css, unsafe_allow_html=True)

# Path to your background image file
background_image_path = os.path.join(os.path.dirname(__file__), 'pics', 'city_2.png')
print(background_image_path)
# Set background image
set_background_image(background_image_path)

epc_values = ['A++', 'A+','A', 'B', 'C', 'D', 'E', 'F', 'G']
condition_values = ['AS_NEW','JUST_RENOVATED','GOOD','TO_BE_DONE_UP', 'TO_RESTORE', 'TO_RENOVATE']
type_values = ["House", "Apartment"]
type_of_kitchen = ['','INSTALLED', 'HYPER_EQUIPPED','SEMI_EQUIPPED', 'NOT_INSTALLED']
type_floodzone = ['','NON_FLOOD_ZONE' ,'RECOGNIZED_FLOOD_ZONE' ,'POSSIBLE_FLOOD_ZONE','POSSIBLE_N_CIRCUMSCRIBED_FLOOD_ZONE', 'CIRCUMSCRIBED_WATERSIDE_ZONE','RECOGNIZED_N_CIRCUMSCRIBED_FLOOD_ZONE' 'CIRCUMSCRIBED_FLOOD_ZONE', 'RECOGNIZED_N_CIRCUMSCRIBED_WATERSIDE_FLOOD_ZONE', 'POSSIBLE_N_CIRCUMSCRIBED_WATERSIDE_ZONE']


st.title("Predict the price of your property :moneybag:")

type_of_property = get_property_buttons()

# Define CSS for the expander containers
expander_css = """
    <style>
        div[data-testid="stExpander"]{
            background-color: #2D2D2D !important;
            border: 1px solid #FFFFFF !important;
            border-radius: 5px !important;
            padding: 10px !important;
        }
        div[data-testid="stExpander"]{
            background-color: #2D2D2D !important;
            padding: 10px !important;
        }
    </style>
"""
# Inject custom CSS for expander styling
st.markdown(expander_css, unsafe_allow_html=True)
# Create the expander for the address group
with st.expander("Address", expanded=False):
    postcode = st.text_input("Postcode: (!)")
    folder, file_name = "src", "postcode_mapping.json"
    all_postalcode = import_postalcode(folder, file_name)
    region, province, district, locality , latitude, longitude = autofill_fields(all_postalcode)

    # Input fields with autocomplete and grayed-out styling
    region= st.text_input("Region:", value=region, key="region", disabled=True, help="Autofilled based on postcode")
    province= st.text_input("Province:", value=province, key="province", disabled=True, help="Autofilled based on postcode")
    district= st.text_input("District:", value=district, key="district", disabled=True, help="Autofilled based on postcode")
    locality= st.text_input("City:", value=locality, key="locality", disabled=True, help="Autofilled based on postcode")

# Create the expander for the general group
with st.expander("General", expanded=False):
    condition=st.select_slider('State the condition for the property', condition_values)
    facade = st.number_input("Number of facades", value=1)

# Create the expander for the interior group
with st.expander("Interior", expanded=False):
    surface=st.text_input('Measurements of the surface in m² (!)')
    bedrooms=st.text_input('Number of bedrooms(!)')
    kitchen = st.selectbox('Type of kitchen', type_of_kitchen)
    fireplaceExists =st.checkbox("Is there a fireplace?")

# Create the expander for the energy group
with st.expander("Energy", expanded=False):
    epcScores=st.select_slider('EPC score',  epc_values)

# Create the expander for the Risks group
with st.expander("Town planning and risks", expanded=False):
    floodzone=st.selectbox('Is the property in a floodzone?',type_floodzone)

    
new_house_data = { 
    'postcode' : [postcode],
    'region' : [region],
    'province' : [province],
    'district': [district],
    'locality': [locality], 
    'latitude' : [latitude],
    'longitude' : [longitude],
    'subtype' : [type],
    'epcScores': [epcScores],
    'bedrooms': [bedrooms],
    'surface': [surface]
}

data_new_property = pd.DataFrame(new_house_data)

# Define mandatory input fields
mandatory_fields = ['postcode', 'epcScores', 'bedrooms', 'surface']

# Define button to trigger prediction
if st.button('Predict the price'):
    # Check if mandatory fields are filled
    mandatory_fields_filled = all([postcode, epcScores, bedrooms, surface])

    if mandatory_fields_filled:
        # Perform prediction
        predicted_price= handle_prediction(data_new_property, type_of_property)
        st.success(f"The predicted price is {predicted_price}")
    else:
        st.write("Please fill in:")
        # Change style of mandatory fields to red
        if not postcode:
            st.markdown('<style>div[data-baseweb="input"] input{border: 1px solid #FF0000;}</style>', unsafe_allow_html=True)
            st.write("postcode")
        if not epcScores:
            st.markdown('<style>div[data-baseweb="input"] input{border: 1px solid #FF0000;}</style>', unsafe_allow_html=True)
            st.write("EPC score")
        if not bedrooms:
            st.markdown('<style>div[data-baseweb="input"] input{border: 1px solid #FF0000;}</style>', unsafe_allow_html=True)
            st.write("Number of bedrooms")
        if not surface:
            st.markdown('<style>div[data-baseweb="input"] input{border: 1px solid #FF0000;}</style>', unsafe_allow_html=True)
            st.write("Measurements of the living surface")

# print(f'THE LONGITUDE IS {new_house_data['longitude']}')
# print(f'THE LATITUDE IS {new_house_data['latitude']}')

# # Define the latitude and longitude coordinates to focus on
# latitude = float(new_house_data['latitude'][0])
# longitude = float(new_house_data['longitude'][0])

# # Create a DataFrame with latitude and longitude columns
# data = pd.DataFrame({'LATITUDE': [latitude], 'LONGITUDE': [longitude]})

# # Create a Streamlit map centered on the provided latitude and longitude
# st.map(data, zoom=9)