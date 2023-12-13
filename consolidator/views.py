import os
import time

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.shortcuts import HttpResponse, render

from consolidator.mixins import CSVReconsilitionMixin

fs = FileSystemStorage(location='temp')
# Create your views here.

def consolidator(request):

    context = {
        "show_results": False
    }

    if request.method == "POST":
        try:
            source_file = request.FILES["source_file"]
            target_file = request.FILES["target_file"]
            destination_file_name = request.POST.get("destination_file")

            source_file_extension = request.FILES['source_file'].name.split('.')[-1].lower()
            target_file_extension = request.FILES['target_file'].name.split('.')[-1].lower()

            if source_file_extension == "csv" and target_file_extension == "csv":
                source_file_content = source_file.read()
                source_file_content = ContentFile(source_file_content)
                source_file_name = fs.save(
                    "temp_source_file.csv", source_file_content
                )
                temp_source_file = fs.path(source_file_name)

                target_file_content = target_file.read()
                target_file_content = ContentFile(target_file_content)
                target_file_name = fs.save(
                    "temp_target_file.csv", target_file_content
                )
                target_source_file = fs.path(target_file_name)

                
                start_time = time.time()
                print(f"Execution Started At: {start_time}")

                csv_consolidator = CSVReconsilitionMixin(temp_source_file, target_source_file, f"{destination_file_name}.csv")
                csv_consolidator.run()
                stats = csv_consolidator.get_consolidation_stats()

                context["missing_in_target"] = stats["Records missing in target: "]
                context["missing_in_source"] = stats["Records missing in source: "]
                context["discrepancies"] = stats["Records with field discrepancies: "]
                context["destination_file"] = f"{destination_file_name}.csv"
                context["show_results"] = True

                end_time = time.time()
                elapsed_time = end_time - start_time

                print(f"Execution Ended At: {end_time}")
                print(f"Execution Time: {elapsed_time}")

            else:
                return HttpResponse({"Please upload only .csv files!"})
                
        except Exception as e:
            raise e

    return render(request, "consolidator.html", context)