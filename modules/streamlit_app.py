import streamlit as st
import requests
import pandas as pd

# Column renaming dictionary
RENAMING_DICT = {
    0: "engine_num", 1: "cycle_num", 2: "oper_set_1", 3: "oper_set_2", 4: "oper_set_3", 5: "temp_fan_inlet",
    6: "temp_lpc_outlet", 7: "temp_hpc_outlet", 8: "temp_lpt_outlet", 9: "px_fan_inlet", 10: "px_by_duct",
    11: "px_hpc_outlet", 12: "phys_fan_speed", 13: "phys_core_speed", 14: "engine_px_ratio",
    15: "stat_px_hpc_out", 16: "fuel_flow_ratio", 17: "corr_fan_speed", 18: "corr_core_speed",
    19: "bypass_ratio", 20: "fuel_air_ratio", 21: "bleed_enthalpy", 22: "demanded_fan_speed",
    23: "demanded_corr_fan_speed", 24: "hpt_coolant_bleed", 25: "lpt_coolant_bleed"
}

st.title("Predictive Maintenance Webapp")

# Upload your input CSV file
uploaded_file = st.file_uploader("Upload your input CSV file", type=["csv"])

if uploaded_file is not None:
    # Display the CSV file contents with renamed columns
    st.write("Uploaded CSV File:")
    df = pd.read_csv(uploaded_file, header=None)
    df.rename(columns=RENAMING_DICT, inplace=True)
    st.dataframe(df)

    # Select the number of rows (window size)
    window_size = st.selectbox("Select the number of rows (window size)", [1, 5, 10, 15, 30])

    # Button to preprocess the data
    if st.button("Preprocess & Predict "):
        # Send the file and window size to the FastAPI server for preprocessing
        files = {"file": uploaded_file.getvalue()}
        response = requests.post("http://127.0.0.1:8000/preprocess/", files=files, data={"window_size": window_size})

        if response.status_code == 200:
            response_data = response.json()
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                st.write("Preprocessed Data Shape:", response_data["data_shape"])
                #st.write("Preprocessed Data:")
                #preprocessed_df = pd.DataFrame(response_data["data"])
                #st.dataframe(preprocessed_df)
                st.write("Predicted RUL:")
                # Display the first prediction as a single number
                predicted_rul = response_data["predictions"][0][0]
                st.write(predicted_rul)
        else:
            st.error("Error occurred during preprocessing.")
