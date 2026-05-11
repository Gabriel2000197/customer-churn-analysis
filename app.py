import streamlit as st
import pandas as pd 
import joblib

#load model, threshold and preprocessor
model= joblib.load('outputs/models/final_subscription_model.pkl')
threshold= joblib.load('outputs/models/best_threshold.pkl')
preprocessor= joblib.load('outputs/models/preprocessor.pkl')

st.title('Custome Subscription Prediction: Decision-Suppor tool')
st.write('Enter customer details - predict the likelihood of term deposit subscription - get a recommendation')

#input
col1, col2, col3= st.columns(3)

with col1:
    age= st.slider('Age', min_value=17, max_value=98, value=40, step=1)
    job= st.selectbox('Job', ['admin.', 'blue-collar', 'entrepreneur', 'housemaid', 'management', 'retired', 'self-employed', 'services', 'student', 'technician', 'unemployed', 'unknown'])
    marital= st.selectbox('Marital Status', ['single', 'married', 'divorced'])

with col2:
    education= st.selectbox('Education', ['basic.4y', 'basic.6y', 'basic.9y', 'high.school', 'professional.course', 'university.degree', 'unknown'])
    poutcome= st.selectbox('Previous Campaign Outcome', ['success', 'failure', 'nonexistent'])
    previously_contacted= st.selectbox('Previously Contacted', [0, 1])

with col3:  #deafault values are the median of the dataset
    euribor3m= st.slider('EURIBOR 3 Month Rate', min_value=0.63, max_value=5.045, value=4.8, step=0.1)
    nr_employed= st.slider('Number of Employees', min_value=4963.6, max_value=5228.1, value=5191.0, step=1.0)
    cons_conf_idx= st.slider('Consumer Confidence Index', min_value=-50.8, max_value=-26.9, value=-41.8, step=0.1)
    emp_var_rate= st.slider('Employment Variation Rate', min_value=-3.4, max_value=1.4, value=1.1, step=0.1)

#default values - columns imputed
campaign = 2
contact = 'cellular'
month = 'may'
day_of_week = 'thu'
housing = 'yes'
loan = 'no'
default = 'no'
cons_price_idx = 93.994
previous = 0
duration = 180

with st.expander("Advanced Settings (optional)"):
    campaign = st.slider("Number of Contacts - This Campaign", 1, 14, 2)
    contact = st.selectbox("Contact Type", ['cellular', 'telephone'])
    month = st.selectbox("Month", ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'])
    day_of_week = st.selectbox("Day of Week", ['mon','tue','wed','thu','fri'])
    housing = st.selectbox("Housing Loan", ['yes','no','unknown'])
    loan = st.selectbox("Personal Loan", ['yes','no','unknown'])
    previous = st.slider("Previous Campaign Contacts", 0, 7, 0)
    duration = st.slider("Call Duration (seconds)", 0, 1271, 180)
    cons_price_idx = st.slider("Consumer Price Index", 92.2, 94.8, 93.994, step=0.001)
    default = st.selectbox("Credit in Default", ['no','yes','unknown'])

st.divider()

#predict
if st.button('Predict Subscription', type='primary'):
    with st.spinner('Predicting subscription...'):
        #convert input to dataframe
        input_data= pd.DataFrame({
            'age': [age],
            'job': [job],
            'marital': [marital],
            'education': [education],
            'poutcome': [poutcome],
            'previously_contacted': [1 if previously_contacted == 'yes' else 0], #manual encoding done
            'euribor3m': [euribor3m],
            'nr_employed': [nr_employed],
            'cons.conf.idx': [cons_conf_idx],
            'emp.var.rate': [emp_var_rate],
            'nr.employed': [nr_employed],              
            'cons.price.idx': [cons_price_idx], 
            #expander
            'campaign': [campaign],
            'contact': [contact],
            'month': [month],
            'day_of_week': [day_of_week],
            'housing': [housing],
            'loan': [loan],
            'previous': [previous],
            'default': [default],
            'duration': [duration],
            'cons.price_idx': [cons_price_idx],
        })

        #preprocessor
        input_data_encoded= preprocessor.transform(input_data)

        #prediction
        prediction_prob= model.predict_proba(input_data_encoded)[0][1] #subscription probability
        prediction= (1 if prediction_prob >= threshold else 0)

        st.divider()
        st.subheader('Prediction Results')

        col1, col2, col3= st.columns(3)
        with col1:
            st.metric('Subscription Probability', f'{prediction_prob:.2%}')

        with col2:
            if prediction == 1:
                st.success('✅ Likely to subscribe')
            else:
                st.error('❌ Not likely to subscribe')
        
        with col3:
            if prediction == 1:
                st.info('📞 Prioritize calling this customer')
            else:
                st.info('🔍 Move to a better customer first')

        st.caption("A client is classified as 'yes' if probability exceeds optimized threshold.")