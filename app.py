# Import the necessary libraries
from multiprocessing.sharedctypes import Value
import streamlit as st 
import requests
import pandas as pd

# Get the API key from the user
api_key = st.sidebar.text_input("Type One AI API Key and press Enter:", type="password")

st.sidebar.write("Made with ❤️ by [@Saboo_Shubham_](https://twitter.com/Saboo_Shubham_)")
st.sidebar.write("Powered by [One AI](https://studio.oneai.com/?utm_source=social&utm_medium=medium&utm_campaign=daniel&utm_term=saboo_pub-towardsai-net-scan-linkedin-posts-to-analyze-emotions-sentiments-and-trends-using-ai-7e9663d612d3)")

if api_key:
        
    # Set the title of the app
    st.title('📱 LinkedIn Posts Scanner ')

    # Set the subtitle of the app
    st.write('**_This application uses the One AI API to scan LinkedIn posts for useful insights._**')  

    st.image('cover.png', use_column_width=True)

    url = "https://api.oneai.com/api/v0/pipeline"

    # Set the headers
    headers = {
      "api-key": api_key, 
      "content-type": "application/json"
    }

    # Input the social media post link
    input_url = st.text_input('Drop the LinkedIn post link here 👇',  value ="LinkedIn post link goes here...")

    # Set the payload
    payload = {
            "input": input_url,
            "input_type": "article",
            "output_type": "json",
            "steps": [
                {
                "skill": "html-extract-article"
                }
            ],
        }
    # Make the request
    req1 = requests.post(url, json=payload, headers=headers)
    article_data = req1.json()
    if st.button("Get Text"):
        article_text = article_data['output'][0]['contents'][0]['utterance']
        st.markdown("##### **_Extracted Text_**")
        st.text(article_text)
        

    with st.expander("Scan for insights"):
        
        # Select the insights to be returned
        skills = [st.selectbox('Select an intelligence feature 🕹', ['emotions', 'sentiments', 'article-topics'])]
        article_text = article_data['output'][0]['contents'][0]['utterance']

        # create a button to call the API
        if st.button('Scan Post for Insights'):
            payload = {
                "input": article_text,
                "input_type": "article",
                "output_type": "json",
                "steps": [
                    {
                    "skill": skills[0]
                    }
                ],
            }
            r = requests.post(url, json=payload, headers=headers)
            data = r.json()
            print(data)


            if 'emotions' in skills:
                st.subheader("Emotion Detection")
                df = pd.DataFrame(columns=['skill', 'emotion', 'span_text'])

                for i in range(len(data['output'][0]['labels'])):
                    df.loc[i] = [data['output'][0]['labels'][i]['skill'], data['output'][0]['labels'][i]['name'], data['output'][0]['labels'][i]['span_text']]

                st.write(df[df["skill"]=="emotions"])

            if 'sentiments' in skills:
                st.subheader("Sentiments Analysis")
                df = pd.DataFrame(columns=['skill', 'sentiment', 'span_text'])

                for i in range(len(data['output'][0]['labels'])):
                    df.loc[i] = [data['output'][0]['labels'][i]['skill'], data['output'][0]['labels'][i]['value'], data['output'][0]['labels'][i]['span_text']]

                st.write(df)

            if 'article-topics' in skills:
                st.subheader("Topic Detection")
                df = pd.DataFrame(columns=['skill', 'topic'])

                for i in range(len(data['output'][0]['labels'])):
                    st.code("#"+data['output'][0]['labels'][i]['value'])

                
else:
    st.error("🔑 API Key Not Found!")
    st.info("💡 Copy paste your One AI API key that you can find in API Keys section once you log in to the [One AI Playground](https://studio.oneai.com/?utm_source=social&utm_medium=medium&utm_campaign=daniel&utm_term=saboo_pub-towardsai-net-detect-business-insights-from-customer-support-conversations-using-ai-b09759144c00)")
  
