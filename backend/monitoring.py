import great_expectations as ge
import os

def validate_data(file_path):
    context = ge.DataContext("/app/great_expectations")
    if not os.path.exists("/app/great_expectations/expectations/my_suite.json"):
        df = ge.dataset.PandasDataset({"file": [file_path]})
        df.expect_column_values_to_not_be_null("file")
        df.save_expectation_suite("/app/great_expectations/expectations/my_suite.json")
    df = ge.read_csv(file_path) if file_path.endswith(".csv") else ge.dataset.PandasDataset({"file": [file_path]})
    validation_result = df.validate(expectation_suite="my_suite.json")
    return validation_result.to_json_dict()