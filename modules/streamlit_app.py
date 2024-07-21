import streamlit as st
import requests
import pandas as pd

st.title("CSV File Uploader and Viewer")

# Select the number of rows to display
window_size = st.number_input("Select the number of rows to view", min_value=1, value=5)

# Upload your input CSV file
uploaded_file = st.file_uploader("Upload your input CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file without headers
    df = pd.read_csv(uploaded_file, header=None)
    
    # Display the CSV file contents
    st.write("Uploaded CSV File:")
    st.dataframe(df)
    
    # Display the first few rows based on the selected window size
    st.write(f"First {window_size} rows of the CSV file:")
    st.dataframe(df.head(window_size))
    
    # Display the data summary
    st.write("Data Summary:")
    st.write(df.describe())
