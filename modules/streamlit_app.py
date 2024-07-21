import streamlit as st
import requests
import pandas as pd

st.title("CSV helloz File Uploader and Viewer")

# Upload your input CSV file
uploaded_file = st.file_uploader("Upload your input CSV file", type=["csv"])

if uploaded_file is not None:
    # Display the CSV file contents
    st.write("Uploaded CSV File:")
    df = pd.read_csv(uploaded_file, header=None)
    st.dataframe(df)

    # Select the number of rows (window size)
    window_size = st.selectbox("Select the number of rows (window size)", [1, 5, 10, 15, 30])

    # Button to preprocess the data
    if st.button("Preprocess Data"):
        # Send the file and window size to the FastAPI server for preprocessing
        files = {"file": uploaded_file.getvalue()}
        response = requests.post("http://127.0.0.1:8000/preprocess/", files=files, data={"window_size": window_size})

        if response.status_code == 200:
            response_data = response.json()
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                st.write("Preprocessed Data Shape:", response_data["data_shape"])
                st.write("Preprocessed Data:")
                preprocessed_df = pd.DataFrame(response_data["data"])
                st.dataframe(preprocessed_df)
        else:
            st.error("Error occurred during preprocessing.")
