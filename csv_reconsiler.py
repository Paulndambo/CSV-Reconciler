import csv
import time

from support_functions import (compare_csv_data_dictionaries,
                               compare_csv_data_lists, csv_to_json)

# Record the start time
start_time = time.time()


class CSVReconsilitionMixin(object):
    def __init__(self, source_file_path, target_file_path, destination_file_name):
        self.source_file_path = source_file_path
        self.target_file_path = target_file_path
        self.destination_file_path = destination_file_name
        self.report_list = []
        self.consolidation_stats = {}

    def run(self):
        self.__initialize_files_data()
        self.__generate_rows_missing_in_either_list()
        self.__compare_csv_rows_data()
        self.__write_results_report()

    def __initialize_files_data(self):
        source_file_data = csv_to_json(self.source_file_path)
        target_file_data = csv_to_json(self.target_file_path)

        return source_file_data, target_file_data

    def __generate_rows_missing_in_either_list(self):
        source_file_data, target_file_data = self.__initialize_files_data()
        [self.report_list.append(x) for x in compare_csv_data_lists(source_file_data, target_file_data)]
        

    def __compare_csv_rows_data(self):
        source_file_data, target_file_data = self.__initialize_files_data()
        results = [self.report_list.append(x) for x in compare_csv_data_dictionaries(source_file_data, target_file_data)]

        self.consolidation_stats["Records with field discrepancies: "] = len(results)

    def __write_results_report(self):
        with open(f"reports/{self.destination_file_path}", 'w', newline='') as csv_file:
            fieldnames = self.report_list[0].keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            # Write the header
            writer.writeheader()
            # Write the data
            writer.writerows(self.report_list)

            print(f"")
        

    def get_consolidation_stats(self):
        source_file_data, target_file_data = self.__initialize_files_data()
        source_data_ids = [x["ID"] for x in source_file_data]
        target_data_ids = [x["ID"] for x in target_file_data]

        self.consolidation_stats["Records missing in target: "] = len([x for x in source_data_ids if x not in target_data_ids])
        self.consolidation_stats["Records missing in source: "] = len([x for x in target_data_ids if x not in source_data_ids])
        
        print("******************Reconciliation Results******************")
        print("Reconciliation completed: ")
        for key, value in self.consolidation_stats.items():
            print(f"{key}: {value}")
        print(f"Report saved to: reports/{self.destination_file_path}")
        print("******************Reconciliation Results******************")
    

    

source_csv_file = input("Enter Source CSV File Location/Path: ")
target_csv_file = input("Enter Target CSV File Location/Path: ")
destination_file_name = input("Enter Name of Reconciliation Report File: ")

reconsiler = CSVReconsilitionMixin(source_csv_file, target_csv_file, destination_file_name)

print("******************Reconciliation Time****************")
print(f"Execution Started At: {start_time}")
reconsiler.run()
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Execution Ended At: {end_time}")
print(f"Execution Time: {elapsed_time}")

reconsiler.get_consolidation_stats()