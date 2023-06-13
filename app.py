import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
st.set_option('deprecation.showPyplotGlobalUse', False)
import pickle
import warnings
warnings.filterwarnings('ignore')
import pymsteams



# --- section ML model -------------------------------------------

def main():

    # --- section 2.1 Predict Diabetes From Digital Medical Records -------------------------------------------
    st.title('High Potential Customer Propensity APP🏆🚀')
    st.sidebar.title('Machine learning for High Potential Customer🏆🚀')
    st.subheader('⭐️ Raw dataset')


    @st.cache_data(persist=True)
    def load_data():
        data = pd.read_csv('/app/streamlit_market_ad/sample.csv')
        return data
    
    @st.cache_data(persist=True)
    def split(df):
        y = df['label']
        x = df.drop(columns=['label'])
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3,random_state=12)
        return x_train, x_test, y_train, y_test
    
    def webhook_msg(WH_LINK, text):
        msg = pymsteams.connectorcard(WH_LINK)
        msg.text(str(text))
        msg.send()


    df = load_data()

    # (part1) ---- show raw data set and correlation -----------------------------------------------------
    if st.sidebar.checkbox('Show raw data', True):
        st.write(df.head(5))


    # (part2) train models
    x_train, x_test, y_train, y_test = split(df)


    # get input data from user
    st.subheader('⭐️ Customer prediction')

    # load model
    loaded_model = pickle.load(open('/app/streamlit_market_ad/trained_customer.sav','rb'))


    # Code for prediction
    submission = ''

    # creating a button for preidction
    if st.button('Make Prediction'):
        x_test = x_test.drop(['origin'], axis=1)

        prob = loaded_model.predict_proba(x_test)

        submission = pd.read_csv('/app/streamlit_market_ad/test_format1.csv')
        submission['prob'] = pd.Series(prob[:, 1])
        submission.sort_values("prob", inplace = True, ascending=False)

        st.subheader('Prediction of High Potential (Loyal) Customer:')
    
        st.write(submission.head(10))

        WH_LINK = 'https://cf.webhook.office.com/webhookb2/62b7c69e-13ea-4ce0-a097-d4b86a1f57c7@bdb74b30-9568-4856-bdbf-06759778fcbc/IncomingWebhook/de3b01af87e04023bd6fac04da0d8861/619ee140-680d-427c-b9ac-695de2f6cb69'
        
        text = []
        submission.reset_index(drop=True, inplace=True)
        for i in range(0, 5):
            texti = f'The top {i} customer is user_id {submission.user_id[i]}, prob is: {submission.prob[i]}'
            text+=[texti]
        st.write(text)

        webhook_msg(WH_LINK, text)
        st.success('Results has been sent to teams channel')
        st.balloons()


     

if __name__ == '__main__':
    main()



