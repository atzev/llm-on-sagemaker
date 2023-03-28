Note: The code is based on https://towardsdatascience.com/create-your-own-large-language-model-playground-in-sagemaker-studio-1be5846c5089 

# Create your own streamlit app
1. In 3_streamlit_app/playground.py replace the <<YOUR ENDPOINT NAME>> with the name of your endpoint. Make sure you are in the right region where your endpoint is deployed. By default we are using eu-west-1
2. Open a new terminal window in SageMaker Studio
3. Run ``` pip install streamlit ```
4. Run ``` pip install boto3 ```
5. Navigate to the 3_streamlit_app directory ```cd 3_streamlit_app```
6. Start the streamlit application ```streamlit run playground.py --server.port 6006```
7. Use the following URL to navigate to the app https://<YOUR_STUDIO_ID>.studio.<YOUR_REGION>.sagemaker.aws/jupyter/default/proxy/6006/ 
