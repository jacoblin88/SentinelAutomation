import json
import csv


data_source = []

with open('query_data.csv', 'r') as f:
    reader = csv.reader(f)
    list_row = list(reader)
    list_row = list_row[1:]
    for row in list_row:
        data_source.append(row[0])


Rule_Name_list = []
Query_list = []
Rule_List = []

with open("template.json") as json_file:
    data = json.load(json_file)
    for rule in data:
        flag = 1
        if "RequiredDataConnectors" in rule:
            if rule['RequiredDataConnectors'] is not None:
                for connector_dtype_tupple in rule['RequiredDataConnectors']:
                    if connector_dtype_tupple['DataTypes'][0] not in data_source:
                        flag=0
                        #print(flag)
                        break
        if flag == 1:
            Rule_List.append(rule)

## Scheduled Fusion MicrosoftSecurityIncidentCreation


# Scheduled
# DisplayName,Severity,Query,QueryPeriod,TriggerThreshold
Scheduled_Rule_Array = []
header = ['DisplayName','Severity','Query','QueryFrequency','QueryPeriod','TriggerThreshold']

for rule in Rule_List:
    if rule['Kind'] == "Scheduled":
        tuple = [rule['DisplayName'],rule['Severity'],rule['Query'],int(rule['QueryFrequency']['TotalSeconds']),int(rule['QueryPeriod']['TotalSeconds']),rule['TriggerThreshold']]
        Scheduled_Rule_Array.append(tuple)

with open('Scheduled.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for tuple in Scheduled_Rule_Array:
        writer.writerow(tuple)