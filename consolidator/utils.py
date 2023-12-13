import csv
import json


def csv_to_json(csv_path):
    # Open the CSV file
    with open(csv_path, "r") as csv_file:
        # Read the CSV data
        csv_data = csv.DictReader(csv_file)

        # Create an empty list to store the CSV rows
        rows = []

        # Loop through each row of the CSV data
        for row in csv_data:
            # Add the row to the list
            rows.append(row)

    # Convert the list of rows to a JSON object
    json_data = json.dumps(rows)

    # Return the JSON object
    return json.loads(json_data)


def compare_csv_data_lists(source, target):
    discrepancies = []

    # Create sets of IDs for quick lookup
    source_ids = set(d['ID'] for d in source)
    target_ids = set(d['ID'] for d in target)

    # Check for records missing in target
    for source_record in source:
        if source_record['ID'] not in target_ids:
            missing_record = {
                "Type": "Record missing in Target",
                "Record Identifier": source_record['ID'],
                "Field": "",
                "Source Value": "",
                "Target Value": ""
            }
            discrepancies.append(missing_record)

    # Check for records missing in source
    for target_record in target:
        if target_record['ID'] not in source_ids:
            missing_record = {
                "Type": "Record missing in Source",
                "Record Identifier": target_record['ID'],
                "Field": "",
                "Source Value": "",
                "Target Value": ""
            }
            discrepancies.append(missing_record)

    return discrepancies



def compare_csv_data_dictionaries(source_list, target_list):
    discrepancies = []

    # Loop through each dictionary in the source list
    for i, source_dict in enumerate(source_list):
        # Find the corresponding dictionary in the target list with the same ID
        target_dict = next(
            (d for d in target_list if d["ID"] == source_dict["ID"]), None)

        # Check if corresponding dictionary is found
        if target_dict:
            # Compare each field value
            for field, source_value in source_dict.items():
                target_value = target_dict.get(field)

                # Check for mismatches and add them to the discrepancies list
                if source_value != target_value:
                    discrepancies.append({
                        "Type": "Field Discrepancy",
                        "Record Identifier": source_dict["ID"],
                        "Field": field,
                        "Source Value": source_value,
                        "Target Value": target_value,
                    })

    return discrepancies
