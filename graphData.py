import matplotlib.pyplot as plt
import csv

csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    quoting = csv.QUOTE_MINIMAL
    )

mostPopularAllKeys = []
mostPopularAllValues = []
with open('mostPopular.csv', 'r', encoding="ascii") as mycsvfile:
    thedata = csv.reader(mycsvfile, dialect='mydialect')
    print(thedata)
    for row in thedata:
        mostPopularAllKeys.append(row[0])
        mostPopularAllValues.append(int(row[1]))

plt.xticks(rotation=90)
plt.bar(range(len(mostPopularAllValues)), mostPopularAllValues, align='center')
plt.xticks(range(len(mostPopularAllValues)), mostPopularAllKeys, size='small')
plt.show()
