# AL_DSA5
# Action Learning

This Repository contains all the necessary information about the LSTM model Development for the Model Defense

## Structure

* dataset : Contains training and test data in txt format
* modules: contains the modules used in the notebooks
* notebooks: models developped and data exploration
* items: files saved such as models, scalers etc.. for later use.


## Setting Up the Database

1. **Install PostgreSQL**: Follow the instructions on the [official website](https://www.postgresql.org/download/) to install PostgreSQL.

2. **Clone the Repository**: Clone this repository to your local machine.

    ```sh
    git clone https://github.com/your-repo.git
    cd your-repo
    ```

3. **Create a Conda Environment**: Create and activate a Conda environment for the project.

    ```sh
    conda create -n ml_project python=3.11.9
    conda activate ml_project
    ```

4. **Install Dependencies**: Install the required dependencies.

    ```sh
    pip install -r requirements.txt
    ```

5. **Set Up the Database**: Run the setup script to create the database, user, and import the schema and sample data.

    ```sh
    ./setup_db.sh
    ```

6. **Run the FastAPI Server**: Start the FastAPI server.

    ```sh
    uvicorn main:app --reload
    ```

7. **Run the Streamlit App**: Start the Streamlit app.

    ```sh
    streamlit run streamlit_app.py
    ```

8. **Access the Database**: You can access the database using any PostgreSQL client with the following credentials:
    - **Database**: rul_db
    - **User**: rul_user
    - **Password**: yourpassword
    - **Host**: localhost
    - **Port**: 5432
