import json
import csv


for n in range(3, 21):
    for m in range(2, n):
        for p in range(1, 10):
            for i in range(100):
                try:
                    with open('Watts_Strogatz/n' + str(n) + 'm' + str(m) + 'p' + str(p/10) + '/nb' + str(i) + '/data.txt') as json_file:
                        data = json.load(json_file)
                    with open('Watts_Strogatz/n' + str(n) + 'm' + str(m) + 'p' + str(p/10) + '/nb' + str(i) + '/attributs.csv') as csvfile:
                        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                except:
                    print(n, m, p/10, i)