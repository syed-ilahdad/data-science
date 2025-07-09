import streamlit as st
from datetime import date


st.set_page_config(page_title="Pipeline Parameters", page_icon=":gear:", layout="wide")

st.title("Pipeline Configuration")
default_date = date(2024, 2, 1)
# selected_date = st.date_input("Pick a date:", value=default_date)

# st.write(f"You picked: {selected_date}")
with st.form("pipeline_form"):
    st.header("Pipeline Information")
    pipeline_id = st.text_input("Pipeline ID:", value="dqfw_dataset_certification_score", placeholder="Enter pipeline ID")
    # pipeline_status = st.selectbox("Pipeline Status:", options=["ON", "OFF"], index=0)  # Default "ON"
    pipeline_status = st.toggle("status", value=False)

    st.header("Default Arguments")

    owner = st.text_input("Owner Email:", value="smunna@ext.uber.com", placeholder="Enter owner email",  help="Enter a valid email address") #Added help text
    owner_ldap_groups = st.text_area("Owner LDAP Groups (comma-separated):", value="cloudlake_metrics", placeholder="Enter comma-separated groups", help="Enter a comma-separated list of LDAP groups") #Text area for potentially long lists
    email = st.text_area("Email Recipients (comma-separated):", value="cloudlake-insights-group@uber.com", placeholder="Enter comma-separated emails", help="Enter a comma-separated list of email addresses") #Text area for potentially long lists
    email_on_failure = st.checkbox("Email on Failure", value=True)

    schedule_interval = st.date_input("Schedule Interval ", value=default_date) #Help text for cron

    col1, col2, col3 = st.columns(3) #Columns for date inputs
    with col1:
      start_date_year = st.number_input("Start Date Year:", value=2023, min_value=2000, max_value=2100, step=1)
    with col2:
      start_date_month = st.number_input("Start Date Month:", value=10, min_value=1, max_value=12, step=1)
    with col3:
      start_date_day = st.number_input("Start Date Day:", value=16, min_value=1, max_value=31, step=1)

    retries = st.number_input("Retries:", value=0, min_value=0, step=1)
    partition_delta = st.number_input("Partition Delta (in days):", value=-1)


    submitted = st.form_submit_button("Submit")

if submitted:
    # Process the form data here
    pipeline_parameters = {
        "pipeline_id": pipeline_id,
        "pipeline_status": pipeline_status,
        "default_args": {
            "owner": owner,
            "owner_ldap_groups": [group.strip() for group in owner_ldap_groups.split(",")], #List conversion and whitespace removal
            "email": [em.strip() for em in email.split(",")], #List conversion and whitespace removal
            "email_on_failure": email_on_failure,
            "schedule_interval": schedule_interval,
            "start_date_year": start_date_year,
            "start_date_month": start_date_month,
            "start_date_day": start_date_day,
            "retries": retries,
            "partition_delta": partition_delta,
        },
    }

    st.write("Submitted Parameters:") #Display the submitted parameters
    st.write(pipeline_parameters)

    # You would typically send this data to your backend or perform other actions here.
    # Example:
    # try:
    #     response = requests.post("your_api_endpoint", json=pipeline_parameters)
    #     response.raise_for_status()  # Raise an exception for bad status codes
    #     st.success("Pipeline configuration updated successfully!")
    # except requests.exceptions.RequestException as e:
    #     st.error(f"Error updating pipeline configuration: {e}")