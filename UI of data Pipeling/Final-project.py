import streamlit as st
from datetime import date,datetime
from streamlit_option_menu import option_menu
import json


st.set_page_config(page_title="U-I Interface", page_icon=":gear:", layout="wide")


with st.sidebar:
    selected=option_menu(
        menu_title="Main menu",
        options=["pipeline parameters", "sensor parameters", "qualitycheck"]
    )
# selecting pipline sidebar
if selected=="pipeline parameters":
    st.title(f"welcome to {selected}")
    # form creation of parameters entered
    default_date = date.today()
    months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"]
    days = list(range(1, 31))


    with st.form('parameters'):
        st.header("Pipeline Information")
        pipeline_id = st.text_input("Pipeline ID:", value="dqfw_dataset_certification_score", placeholder="Enter pipeline ID")
        pipeline_status = st.toggle("status", value=False)

        st.header("Default Arguments")

        owner = st.text_input("Owner Email:", value="smunna@ext.uber.com", placeholder="Enter owner email",  help="Enter a valid email address") #Added help text
        owner_ldap_groups = st.text_area("Owner LDAP Groups (comma-separated):", value="cloudlake_metrics", placeholder="Enter comma-separated groups", help="Enter a comma-separated list of LDAP groups") #Text area for potentially long lists
        email = st.text_area("Email Recipients (comma-separated):", value="cloudlake-insights-group@uber.com", placeholder="Enter comma-separated emails", help="Enter a comma-separated list of email addresses") #Text area for potentially long lists
        email_on_failure = st.checkbox("Email on Failure", value=True)

        schedule_interval = st.date_input("Schedule Interval ", value=default_date) #Help text for cron

        col1, col2, col3 = st.columns(3) #Columns for date inputs
        with col1:
           
            # start_date_year = st.number_input("Start Date Year:", value=2023, min_value=2000, max_value=2100, step=1)
            current_year = datetime.now().year
            years = list(range( current_year,2040))  # Years from 1900 to current year

            # Selectbox for year selection
            start_date_year = st.selectbox("Start date Year:", years, index=years.index(current_year))

            st.write(f"You selected: {start_date_year}")        
        with col2:
            # start_date_month = st.number_input("Start Date Month:", value=10, min_value=1, max_value=12, step=1)
            start_date_month = st.selectbox("start a Month:", months)
            st.write(f"You selected: {start_date_month}")
        with col3:
            # start_date_day = st.number_input("Start Date Day:", value=16, min_value=1, max_value=31, step=1)
            start_date_day = st.selectbox("start a Day (1-30):", days)

            st.write(f"📅 You selected: {start_date_day}")

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
    

if selected=="sensor parameters":
     st.title(f"welcome to {selected}")

    # Custom CSS for a more visually appealing layout (optional)
     st.markdown(
        """
        <style>
        .main .block-container {
            max-width: 90%; /* Adjust as needed */
        }
        .st-expander {
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .st-expander-header {
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

     st.title("Sensor Parameters Configuration")

     with st.form("sensor_form"):
        st.header("Sensor Arguments")

        col1, col2 = st.columns(2)  # Two columns for better organization

        with col1:
            sensor_flag = st.toggle("Sensor Enabled", value=True)
            owner = st.text_input("Owner Email:", value="smunna@ext.uber.com", placeholder="Enter owner email", help="Enter a valid email address")
            email = st.text_area("Email Recipients (comma-separated):", value="cloudlake-insights-group@uber.com", placeholder="Enter comma-separated emails", help="Enter a comma-separated list of email addresses")
            owner_ldap_groups = st.text_area("Owner LDAP Groups (comma-separated):", value="cloudlake_metrics", placeholder="Enter comma-separated groups", help="Enter a comma-separated list of LDAP groups")
            depends_on_past = st.checkbox("Depends on Past", value=False)
            email_on_retry = st.checkbox("Email on Retry", value=False)
            email_on_failure = st.checkbox("Email on Failure", value=True)
            auto_backfill = st.checkbox("Auto Backfill", value=False)

        with col2:
            st.header("additional configs")
            exception_timeout = st.number_input("Exception Timeout (seconds):", value=10800, min_value=0, step=1)
            retry_delay = st.number_input("Retry Delay (seconds):", value=300, min_value=0, step=1)
            retries = st.number_input("Retries:", value=10, min_value=0, step=1)



        st.header("Task Details")

        col3, col4 = st.columns(2)

        with col3:
            task_id = st.text_input("Task ID:", value="wait_for_hive_etl_table", placeholder="Enter task ID")
            external_pipeline_id = st.text_input("External Pipeline ID:", value="0a6079f0-7336-11ee-b997-1c34da4d8ae0", placeholder="Enter external pipeline ID")

        with col4:
            external_task_id = st.text_input("External Task ID:", value="QB_PRESTO_TO_TABLE", placeholder="Enter external task ID")
            execution_delta = st.number_input("Execution Delta (hours):", value=0)


        submitted = st.form_submit_button("Submit")

     if submitted:
        sensor_parameters = {
            "sensor_args": {
                "sensor_flag": sensor_flag,
                "owner": owner,
                "email": [em.strip() for em in email.split(",")],
                "owner_ldap_groups": [group.strip() for group in owner_ldap_groups.split(",")],
                "depends_on_past": depends_on_past,
                "email_on_retry": email_on_retry,
                "email_on_failure": email_on_failure,
                "auto_backfill": auto_backfill,
                "exception_timeout": exception_timeout,
                "retry_delay": retry_delay,
                "retries": retries,
            },
            "task_details": {
                "task_id": task_id,
                "external_pipeline_id": external_pipeline_id,
                "external_task_id": external_task_id,
                "execution_delta": execution_delta,
            },
        }

        st.write("Submitted Parameters:")
        st.write(sensor_parameters)

        # ... Your backend integration code here ...


if selected=="qualitycheck":
        
    st.title("Data Quality Checks Configuration")

    # ... (CSS styling from previous examples)

    if "num_checks" not in st.session_state:
        st.session_state.num_checks = 0

    num_checks_to_add = st.number_input("Number of Data Quality Checks to Add:", min_value=0, value=0, step=1)

    if st.button("Add Data Quality Checks"):
        st.session_state.num_checks += num_checks_to_add
        st.rerun()  # Force page refresh

    if st.session_state.num_checks > 0:
        with st.form("dq_checks_form"):
            data_quality_checks = []
            for i in range(st.session_state.num_checks):
                st.header(f"Data Quality Check {i + 1}")

                # ... (Data quality check input fields - same as before)
                col1, col2 = st.columns(2)
                with col1:
                    table_name_with_namespace = st.text_input(f"Table Name with Namespace {i+1}:", value="cloudlake_metrics.dataset_certification_score")
                    primary_key = st.text_input(f"Primary Key {i+1}:", value="None", placeholder="e.g., id, user_id, or None")
                    partition_key = st.text_input(f"Partition Key {i+1}:", value="datestr", placeholder="e.g., date, partition_date")

                with col2:
                    alert_poc_str = st.text_area(f"Alert POCs (comma-separated) {i+1}:", value="cloudlake-insights-group@uber.com,data-cloudlake-core-leads-group@uber.com", placeholder="Enter comma-separated emails")
                    cc_list_str = st.text_area(f"CC List (comma-separated) {i+1}:", value="vganga5@ext.uber.com", placeholder="Enter comma-separated emails")

                st.subheader("Multi-Attribute Duplicates Validation")
                col3, col4 = st.columns(2)

                with col3:
                    col_list_str = st.text_area(f"Column List (comma-separated) {i+1}:", value="dataset_name,execution_date,datestr,test_category", placeholder="Enter comma-separated columns")
                    partition_condition_json = st.text_area(f"Partition Condition (JSON) {i+1}:", value='[{"datestr": []}]', placeholder='e.g., [{"datestr": []}]', height=75)
                    alert_criticality_multi = st.selectbox(f"Alert Criticality (Multi) {i+1}:", options=["Low", "Medium", "High"], index=0)

                with col4:
                    threshold_check_type_multi = st.selectbox(f"Threshold Check Type (Multi) {i+1}:", options=["==", "!=", ">", "<", ">=", "<="], index=0)
                    threshold_value_multi = st.number_input(f"Threshold Value (Multi) {i+1}:", value=0.00)

                st.subheader("Validations")

                validations = {}
                for validation_type in ["failure_score", "health_score"]:
                    st.subheader(f"{validation_type.capitalize()} Validation")
                    col5, col6 = st.columns(2)

                    with col5:
                        lower_range = st.number_input(f"Lower Range ({validation_type}) {i+1}:", value=0.00)
                        upper_range = st.number_input(f"Upper Range ({validation_type}) {i+1}:", value=10.00)
                        partition_condition_json_val = st.text_area(f"Partition Condition (JSON) ({validation_type}) {i+1}:", value='[{"datestr": []}]', placeholder='e.g., [{"datestr": []}]', height=75)
                        alert_criticality_val = st.selectbox(f"Alert Criticality ({validation_type}) {i+1}:", options=["Low", "Medium", "High"], index=2)

                    with col6:
                        threshold_check_type_val = st.selectbox(f"Threshold Check Type ({validation_type}) {i+1}:", options=["==", "!=", ">", "<", ">=", "<="], index=0)
                        threshold_value_val = st.number_input(f"Threshold Value ({validation_type}) {i+1}:", value=0.00)

                    validations[validation_type] = {
                        "num_range_check": {
                            "lower_range": lower_range,
                            "upper_range": upper_range,
                            "partition_condition": json.loads(partition_condition_json_val),
                            "alert_criticality": alert_criticality_val,
                            "threshold_check_type": threshold_check_type_val,
                            "threshold_value": threshold_value_val,
                        }
                    }

                data_quality_checks.append(
                    {
                        "table_name_with_namespace": table_name_with_namespace,
                        "primary_key": primary_key,
                        "partition_key": partition_key,
                        "validations_multi_attribute": {
                            "multi_attribute_duplicates": {
                                "col_list": [col.strip() for col in col_list_str.split(",")],
                                "partition_condition": json.loads(partition_condition_json),
                                "alert_criticality": alert_criticality_multi,
                                "threshold_check_type": threshold_check_type_multi,
                                "threshold_value": threshold_value_multi,
                            }
                        },
                        "validations": validations,
                        "alert_poc": [poc.strip() for poc in alert_poc_str.split(",")],
                        "cc_list": [cc.strip() for cc in cc_list_str.split(",")],
                    }
                )

            submitted = st.form_submit_button("Submit Data Quality Checks")

        if submitted:
            st.write("Submitted Data Quality Checks:")
            st.write(data_quality_checks)

            # ... Your backend integration code here ...


if st.sidebar.button("submit"):
    st.sidebar.write()