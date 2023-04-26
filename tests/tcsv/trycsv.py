import csv

reader = csv.DictReader(open('logs.csv', 'r', encoding='utf-8'))
print(reader.fieldnames)
writer = csv.DictWriter(open('logs.csv', 'a', encoding='utf-8'), reader.fieldnames, delimiter="|")

writer.writerow({
    'name': '程闽',
    'age': 19
})