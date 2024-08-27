
import streamlit as st 
import pandas as pd
from joblib import load
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option("styler.render.max_elements", 282348)
st.set_page_config(
    page_title="FraudDetection",
    page_icon="",
)

# st.sidebar.success("Main page")
# Load the model
model = load('model.joblib')


def file():
 st.page_link("pages/📂_Upload Template.py", label="Check the upload Template",icon="❗")

 uploaded_file = st.file_uploader(type='csv',label= "Upload the client data ")
   
 if uploaded_file is not None :
        df=pd.read_csv(uploaded_file)
        df=df.drop(columns='Unnamed: 0')
        st.write(df.head())
        return df
    
def idclieent(data):
    client_ids=data['client_id']
    return client_ids
def regionclieent(data):
     regions=data['region']
     return regions
def disrictclieent(data):
     districts=data['disrict']
     return districts

def encoder(data):
    
     encoder = OneHotEncoder(sparse_output=False)
     encoded_datatest = encoder.fit_transform(data[['counter_type']])
     encoded_datatest = encoded_datatest.astype(int)
#création d'un DataFrame pour les colonnes encodées
     encoded_dftest = pd.DataFrame(encoded_datatest, columns=encoder.get_feature_names_out(['counter_type']))
     data.reset_index(drop=True, inplace=True)
# Concaténer les données encodées avec le DataFrame original
     data= pd.concat([data, encoded_dftest], axis=1).drop(columns=['counter_type'], errors='ignore')
     return data
     

def normaliser(data):
    scalertest=MinMaxScaler()
    data_normalized=scalertest.fit_transform(data)
    data=pd.DataFrame(data_normalized,columns=data.columns)
    return data


def preprocess(df):
     
     df=df.drop(columns='client_id')
     df=encoder(df)
     df=normaliser(df)
     df=df.drop(columns=['old_index','counter_type_ELEC','counter_type_GAZ','counter_code'])
     return df


def predict(data,clientid,regions,disricts):
    predictions=model.predict(data)
    mapping = {0: "Not Fraud", 1: "Fraud"}
    
    results = pd.DataFrame({
    'client_id': clientid,
    'predicted_class': predictions,
    'region':regions,
    'districts': disricts
    })
    resultspred=results.groupby('client_id').agg(lambda x : x.mode().iloc[0])
    resultspred = resultspred.reset_index()
    # Apply the mapping to the DataFrame
    resultspred['decoded_class'] = resultspred['predicted_class'].map(mapping)
    return resultspred

def highlight_fraud(val):
    color = 'red' if val == 'Fraud' else 'green'
    return f'color: {color}'

def printf(pred):
    #fraud_cases = pred[pred['decoded_class'] == 'Fraud']
    if not pred.empty:
        pred = pred.style.applymap(highlight_fraud, subset=['decoded_class'])
        st.dataframe(pred)
        
    
fraud_cases=None
notfraud_cases=None



# Display the pie chart in Streamlit


def main():
    global fraud_cases, notfraud_cases 
     # Display a warning message #721c24
    st.warning("🚨 Please note: Clients flagged as fraudulent require further verification. Additional steps are needed to confirm fraud.")
    # st.markdown(
    # """
    # <div style="background-color: yellow ; color: white; padding: 10px; border-radius: 5px;">
    #     🚨The clients predicted as fraudulent may not be definitively fraudulent. Additional steps are needed to confirm fraud.
    # </div>
    # """,
    # unsafe_allow_html=True
    # )
   
    resultspred=None
    checkbox_state=None
    checkbox_stateF=None
    red=None
    green=None
    st.title('Fraud Detection')
    st.logo('cropped-radem.png')
    data=file()
    if data is not None :
        
        button=st.button('Predict',type='primary')
        # Create an expander (collapsible section) to simulate a popover
        
        if button:
            client_ids = idclieent(data)
            regions=regionclieent(data)
            districts=disrictclieent(data)
            data = preprocess(data)
            st.session_state['resultspred']= predict(data, client_ids,regions,districts)
            # st.write(st.session_state['resultspred'].columns)

            selected_columns = st.session_state['resultspred'][['client_id', 'predicted_class', 'decoded_class']]

            st.session_state['fraud_cases'] =  selected_columns[selected_columns['decoded_class'] == 'Fraud']
            st.session_state['notfraud_cases'] = selected_columns [selected_columns['decoded_class'] == 'Not Fraud']
            
            st.success("Prediction complete!")
            # printf(selected_columns )
        if 'fraud_cases' in st.session_state or 'notfraud_cases' in st.session_state:
            with st.expander("Filter Items"):
                red = st.checkbox("Show fraudulent clients", value=False)
                green = st.checkbox("Show not fraudulent clients", value=False)
                
                st.session_state['pourcentage']= st.session_state['resultspred']['decoded_class'].value_counts(normalize=True)*100
            st.page_link("pages/📊_prediction_statistics.py", label="Check the prediction statistics",icon="📊")
               
            if red and 'fraud_cases' in st.session_state:
                    st.write("### Fraudulent Clients")
                    printf(st.session_state['fraud_cases'])

            if green and 'notfraud_cases' in st.session_state:
                    st.write("### Non-Fraudulent Clients")
                    printf(st.session_state['notfraud_cases'])
       
      
        
    
        


    
    


     


if __name__ == "__main__":
    main()












