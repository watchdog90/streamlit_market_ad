import streamlit as st
import pandas as pd
import numpy as np
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

    @st.cache_data(persist=True)
    def load_data():
        data = pd.read_csv('/app/streamlit_market_ad/sample.csv')
        return data
    
  
    
    def webhook_msg(WH_LINK, text):
        msg = pymsteams.connectorcard(WH_LINK)
        msg.text(str(text))
        msg.send()


    df = load_data()

    # (part1) ---- show raw data set and correlation -----------------------------------------------------
    st.subheader('⭐️ Raw dataset')
    if st.sidebar.checkbox('Show raw data', True):
        df_user_log = pd.read_csv('/app/streamlit_market_ad/user_log_sample.csv')
        df_user_info = pd.read_csv('/app/streamlit_market_ad/user_info_sample.csv')

        st.subheader('user log dataset')
        st.write('time_stamp: mmdd')
        st.write('action_type: 0= click, 1= shop bag, 2= purchase, 3= list')
        st.write(df_user_log.head(5))
        st.write(df_user_log.shape)


        st.subheader('user profile dataset')
        st.write('age: [0,18][18,24][25,29][30,34][35,39][40,49][>=50]')
        st.write('gender: 0= female, 1= male')
        st.write(df_user_info.head(5))
        st.write(df_user_info.shape)


    st.subheader('⭐️ Preprocessed dataset')
    if st.sidebar.checkbox('Show preprocessed data', False):
        st.write('interatvie features: user & item, sell & item')
        st.write('user buy/click, sell buy/click, diff age groups, diff genders, diff timestamps... ')
        st.write(df.head(5))
        st.write(df.shape)

    # get input data from user
    st.subheader('⭐️ Customer prediction')

    # Code for prediction
    submission = ''

    # creating a button for preidction
    if st.button('Make Prediction'):

        submission = pd.read_csv('/app/streamlit_market_ad/rank.csv')
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



