import csv
import json

# Read CSV data from file
csv_file_path = "Modified_File.csv"  # Replace with the actual path to your CSV file
json_file_path = "Json_File.json"  # Replace with the desired path for the output JSON file

data = []
with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data.append(row)

# Convert data to JSON
json_data = json.dumps({"projects": data}, indent=2)

# Write JSON data to file
with open(json_file_path, mode='w', encoding='utf-8') as json_file:
    json_file.write(json_data)

print(f"Conversion successful. JSON data written to {json_file_path}")
