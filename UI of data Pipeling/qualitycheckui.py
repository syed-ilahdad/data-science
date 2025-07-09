import streamlit as st
import json

st.set_page_config(page_title="Data Quality Checks Configuration", page_icon=":clipboard:", layout="wide")

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