import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# --- 1. Page Configuration ---
st.set_page_config(page_title="Health Assistant AI", layout="wide", page_icon="🧑‍⚕️")

# --- 2. Custom CSS for Look & Feel ---
st.markdown("""
    <style>
    .main-header { font-size: 45px; font-weight: bold; color: blue; margin-bottom: 10px; }
    .sub-text { font-size: 18px; color: #555; margin-bottom: 25px; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #f8f9fa; color: #666; text-align: center; padding: 10px; border-top: 1px solid #ddd; z-index: 100; }
    div.stButton > button:first-child { background-color: #2E86C1; color: white; border-radius: 10px ; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Loading Saved Models ---
working_dir = os.path.dirname(os.path.abspath(__file__))

try:
    diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))
    heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))
    parkinsons_model = pickle.load(open(f'{working_dir}/saved_models/parkinsons_model.sav', 'rb'))
except Exception as e:
    st.error(f"Error loading models: {e}. Please check the 'saved_models' folder.")

# --- 4. Header Section ---
st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 15px 5%; background-color: #2E86C1; color: white; border-radius: 10px; margin-bottom: 30px;">
        <div style="font-size: 30px; font-weight: bold; cursor: pointer;">🩺 HealthShield AI</div>
        <div style="font-size: 20px;">
            <span style="margin-left: 20px;">Book Your Appointment</span>
            <span style="margin-left: 20px;">About</span>
            <span style="margin-left: 20px;">Contact</span>
            <span style="margin-left: 20px;">SignUp</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    

# --- 5. Navigation Logic (Session State) ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def change_page(page_name):
    st.session_state.page = page_name


# --- 6. PAGE LOGIC ---

if st.session_state.page == 'home':
    # LANDING PAGE
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("<div class='main-header'>AI-Powered Early Detection, Better Health Tomorrow</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-text'>Advanced machine learning to accurately forecast chronic conditions, helping you take proactive control of your well-being</div>", unsafe_allow_html=True)
        if st.button("Start Disease Prediction 🚀", use_container_width=True):
            change_page('predict')
            st.rerun()

    with col2:
        # Placeholder imag
        st.image(r"image/medical landing image.avif", use_container_width=True)

    st.divider()
    st.subheader("Available Services")
    c1, c2, c3 = st.columns(3)
    c1.info("✔️ **Diabetes Prediction**")
    c2.info("✔️ **Heart Disease Check**")
    c3.info("✔️ **Parkinson's Analysis**")

else:
    # PREDICTION PAGE
    if st.button("⬅ Back to Home"):
        change_page('home')
        st.rerun()

    with st.sidebar:
        selected = option_menu('Prediction Menu',
                               ['Diabetes Prediction', 'Heart Disease Prediction', 'Parkinsons Prediction'],
                               icons=['activity', 'heart', 'person'], 
                               menu_icon='hospital-fill', 
                               default_index=0)

    # --- Diabetes Prediction Logic ---
    if selected == 'Diabetes Prediction':
        st.title('Diabetes Prediction using ML')
        col1, col2, col3 = st.columns(3)
        with col1: Pregnancies = st.text_input('Number of Pregnancies')
        with col2: Glucose = st.text_input('Glucose Level')
        with col3: BloodPressure = st.text_input('Blood Pressure value')
        with col1: SkinThickness = st.text_input('Skin Thickness value')
        with col2: Insulin = st.text_input('Insulin Level')
        with col3: BMI = st.text_input('BMI value')
        with col1: DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')
        with col2: Age = st.text_input('Age of the Person')

        diab_diagnosis = ''
        if st.button('Diabetes Test Result'):
            try:
                user_input = [float(x) for x in [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]]
                diab_prediction = diabetes_model.predict([user_input])
                diab_diagnosis = "Person's Diabetes disease status is: Positive" if diab_prediction[0] == 1 else "Person's Diabetes disease status is: Negative"
                st.success(diab_diagnosis)
            except: st.error("Please enter valid numeric values")

    # --- Heart Disease Prediction Logic ---
    if selected == 'Heart Disease Prediction':
        st.title('Heart Disease Prediction using ML')
        col1, col2, col3 = st.columns(3)
        with col1: age = st.text_input('Age')
        with col2:
           sex_option = st.selectbox(
            'Select Gender',
            ['Male', 'Female'],
            help="Choose your gender"
        )
           sex = 1 if sex_option == 'Male' else 0
        with col3: cp = st.text_input('Chest Pain types')
        with col1: trestbps = st.text_input('Resting Blood Pressure')
        with col2: chol = st.text_input('Serum Cholestoral in mg/dl')
        with col3: fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')
        with col1: restecg = st.text_input('Resting Electrocardiographic results')
        with col2: thalach = st.text_input('Maximum Heart Rate achieved')
        with col3: exang = st.text_input('Exercise Induced Angina')
        with col1: oldpeak = st.text_input('ST depression induced by exercise')
        with col2: slope = st.text_input('Slope of the peak exercise ST segment')
        with col3: ca = st.text_input('Major vessels colored by flourosopy')
        with col1: thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

        heart_diagnosis = ''
        if st.button('Heart Disease Test Result'):
            try:
                user_input = [float(x) for x in [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]]
                heart_prediction = heart_disease_model.predict([user_input])
                heart_diagnosis = "Person's Heart disease status is: Positive" if heart_prediction[0] == 1 else "Person's Heart disease status is: Negative"
                st.success(heart_diagnosis)
            except: st.error("Please enter valid numeric values")

    # --- Parkinson's Prediction Logic ---
    if selected == "Parkinsons Prediction":
        st.title("Parkinson's Disease Prediction using ML")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1: fo = st.text_input('MDVP:Fo(Hz)')
        with col2: fhi = st.text_input('MDVP:Fhi(Hz)')
        with col3: flo = st.text_input('MDVP:Flo(Hz)')
        with col4: Jitter_percent = st.text_input('MDVP:Jitter(%)')
        with col5: Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')
        with col1: RAP = st.text_input('MDVP:RAP')
        with col2: PPQ = st.text_input('MDVP:PPQ')
        with col3: DDP = st.text_input('Jitter:DDP')
        with col4: Shimmer = st.text_input('MDVP:Shimmer')
        with col5: Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')
        with col1: APQ3 = st.text_input('Shimmer:APQ3')
        with col2: APQ5 = st.text_input('Shimmer:APQ5')
        with col3: APQ = st.text_input('MDVP:APQ')
        with col4: DDA = st.text_input('Shimmer:DDA')
        with col5: NHR = st.text_input('NHR')
        with col1: HNR = st.text_input('HNR')
        with col2: RPDE = st.text_input('RPDE')
        with col3: DFA = st.text_input('DFA')
        with col4: spread1 = st.text_input('spread1')
        with col5: spread2 = st.text_input('spread2')
        with col1: D2 = st.text_input('D2')
        with col2: PPE = st.text_input('PPE')

        parkinsons_diagnosis = ''
        if st.button("Parkinson's Test Result"):
            try:
                user_input = [float(x) for x in [fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]]
                parkinsons_prediction = parkinsons_model.predict([user_input])
                parkinsons_diagnosis = "Person's Parkinson's disease status is: Positive" if parkinsons_prediction[0] == 1 else "Person's Parkinson's disease status is: Negative"
                st.success(parkinsons_diagnosis)
            except: st.error("Please enter valid numeric values")
            
            # --- APPOINTMENT BOOKING LANDING SECTION ---
st.divider() 

  
acol1, acol2 = st.columns([1, 1])

with acol1: 
    
      st.image(r"image/medical appointment image.avif", use_container_width=True)

with acol2:
       # tagline
      st.markdown("<div class='main-header'>Consult with Our Specialized Doctors</div>", unsafe_allow_html=True)
      st.markdown("<div class='sub-text'>After your prediction, get expert medical advice instantly. Book a slot with top-rated professionals for a detailed consultation.</div>", unsafe_allow_html=True)
      
      # web link
      appointment_link = "https://appointment-booking-app-frontend-x2al.onrender.com"
      
      
      #st.link_button("Book Your Appointment 📅", appointment_link, use_container_width=True)
      #
appointment_link = "https://appointment-booking-app-frontend-x2al.onrender.com"

st.markdown(f"""
<style>
.button {{
    display: inline-block;
    width: 40%;
    margin-left: 55%;
    position: absolute;
    bottom:50px;
    padding: 12px;
    text-align: center;
    border-radius: 10px;
    background: linear-gradient(90deg, #4f46e5, #9333ea, #ec4899);
    color: white !important;
    font-size: 18px;
    font-weight: bold;
    text-decoration: none;
    transition: 0.3s ease;
}}
.button:hover {{
    transform: scale(1.05);
    box-shadow: 0 0 15px rgba(147, 51, 234, 0.6);
}}
</style>

<a href="{appointment_link}" target="_blank" class="button">
    Book Your Appointment 📅
</a>
""", unsafe_allow_html=True)
      #
      



st.divider()



# --- 7. Footer Section ---
st.markdown("""
    <div class="footer">
        <p>© 2026 Health Assistant AI | Created for Medical Awareness</p>
    </div>
    """, unsafe_allow_html=True)
