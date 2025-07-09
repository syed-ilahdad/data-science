import streamlit as st
from streamlit_scroll_navigation import scroll_navbar
from datetime import date, datetime
import json

# Anchor IDs
anchor_ids = ["pipeline_parameters", "sensor_parameters", "qualitycheck"]

# Sidebar navigation
with st.sidebar:
    st.subheader("Navigation")
    scroll_navbar(anchor_ids, anchor_labels=None)

st.subheader(anchor_ids[0], anchor=anchor_ids[0])
st.title(f"Welcome to {anchor_ids[0]}")
default_date = date.today()

# Initialize session state variables
if "pipeline_parameters" not in st.session_state:
    st.session_state.pipeline_parameters = None
if "sensor_parameters" not in st.session_state:
    st.session_state.sensor_parameters = None
if "data_quality_checks" not in st.session_state:
    st.session_state.data_quality_checks = []

# Pipeline Parameters Form
with st.form("parameters"):
    st.header("Pipeline Information")
    pipeline_id = st.text_input("Pipeline ID:", value="dqfw_dataset_certification_score")
    pipeline_status = st.toggle("Pipeline Status", value=False)

    st.header("Default Arguments")
    owner = st.text_input("Owner Email:", value="smunna@ext.uber.com")
    owner_ldap_groups = st.text_area("Owner LDAP Groups (comma-separated):", value="cloudlake_metrics")
    email = st.text_area("Email Recipients (comma-separated):", value="cloudlake-insights-group@uber.com")
    email_on_failure = st.checkbox("Email on Failure", value=True)
    schedule_interval = st.date_input("Schedule Interval", value=default_date)

    retries = st.number_input("Retries:", value=0, min_value=0, step=1)
    partition_delta = st.number_input("Partition Delta (in days):", value=-1)

    pipeline_submitted = st.form_submit_button("Submit Pipeline Parameters")

if pipeline_submitted:
    st.session_state.pipeline_parameters = {
        "pipeline_id": pipeline_id,
        "pipeline_status": pipeline_status,
        "default_args": {
            "owner": owner,
            "owner_ldap_groups": [group.strip() for group in owner_ldap_groups.split(",")],
            "email": [em.strip() for em in email.split(",")],
            "email_on_failure": email_on_failure,
            "schedule_interval": str(schedule_interval),
            "retries": retries,
            "partition_delta": partition_delta,
        },
    }
    st.success("Pipeline Parameters Submitted!")

# Sensor Parameters Form
st.subheader(anchor_ids[1], anchor=anchor_ids[1])
st.title(f"Welcome to {anchor_ids[1]}")

with st.form("sensor_form"):
    st.header("Sensor Arguments")
    sensor_flag = st.toggle("Sensor Enabled", value=True)
    owner = st.text_input("Sensor Owner Email:", value="smunna@ext.uber.com")
    email = st.text_area("Sensor Email Recipients (comma-separated):", value="cloudlake-insights-group@uber.com")
    retries = st.number_input("Sensor Retries:", value=10, min_value=0, step=1)

    sensor_submitted = st.form_submit_button("Submit Sensor Parameters")

if sensor_submitted:
    st.session_state.sensor_parameters = {
        "sensor_flag": sensor_flag,
        "owner": owner,
        "email": [em.strip() for em in email.split(",")],
        "retries": retries,
    }
    st.success("Sensor Parameters Submitted!")

# Data Quality Checks Form
st.subheader(anchor_ids[2], anchor=anchor_ids[2])
st.title("Data Quality Checks Configuration")

num_checks_to_add = st.number_input("Number of Data Quality Checks to Add:", min_value=0, value=0, step=1)

if st.button("Add Data Quality Checks"):
    st.session_state.num_checks = num_checks_to_add
    st.rerun()

if st.session_state.num_checks > 0:
    with st.form("dq_checks_form"):
        data_quality_checks = []
        for i in range(st.session_state.num_checks):
            st.header(f"Data Quality Check {i + 1}")

            col1, col2 = st.columns(2)
            with col1:
                table_name_with_namespace = st.text_input(f"Table Name {i+1}:", value="cloudlake_metrics.dataset_certification_score")
                primary_key = st.text_input(f"Primary Key {i+1}:", value="None")
                partition_key = st.text_input(f"Partition Key {i+1}:", value="datestr")

            with col2:
                alert_poc_str = st.text_area(f"Alert POCs (comma-separated) {i+1}:", value="cloudlake-insights-group@uber.com")
                cc_list_str = st.text_area(f"CC List (comma-separated) {i+1}:", value="vganga5@ext.uber.com")

            st.subheader("Multi-Attribute Duplicates Validation")
            col3, col4 = st.columns(2)

            with col3:
                col_list_str = st.text_area(f"Column List (comma-separated) {i+1}:", value="dataset_name,execution_date,datestr,test_category")
                partition_condition_json = st.text_area(f"Partition Condition (JSON) {i+1}:", value='[{"datestr": []}]')
                alert_criticality_multi = st.selectbox(f"Alert Criticality (Multi) {i+1}:", options=["Low", "Medium", "High"], index=0)

            with col4:
                threshold_check_type_multi = st.selectbox(f"Threshold Check Type (Multi) {i+1}:", options=["==", "!=", ">", "<", ">=", "<="], index=0)
                threshold_value_multi = st.number_input(f"Threshold Value (Multi) {i+1}:", value=0.00)

            validations = {}
            for validation_type in ["failure_score", "health_score"]:
                st.subheader(f"{validation_type.capitalize()} Validation")
                col5, col6 = st.columns(2)

                with col5:
                    lower_range = st.number_input(f"Lower Range ({validation_type}) {i+1}:", value=0.00)
                    upper_range = st.number_input(f"Upper Range ({validation_type}) {i+1}:", value=10.00)
                    partition_condition_json_val = st.text_area(f"Partition Condition (JSON) ({validation_type}) {i+1}:", value='[{"datestr": []}]')
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

            data_quality_checks.append({
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
            })

        dq_submitted = st.form_submit_button("Submit Data Quality Checks")

    if dq_submitted:
        st.session_state.data_quality_checks = data_quality_checks
        st.success("Data Quality Checks Submitted!")

# Final Submit Button
if st.button("Final Submit"):
    final_submission = {
        "Pipeline Parameters": st.session_state.pipeline_parameters,
        "Sensor Parameters": st.session_state.sensor_parameters,
        "Data Quality Checks": st.session_state.data_quality_checks,
    }
    st.subheader("Final Submitted Data")
    st.json(final_submission)
