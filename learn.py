import sys
import csv
import estimate
import matplotlib.pyplot as plt
import statistics

t0, t1 = 0.0, 0.0
try:
    with open('model.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            t0 = float(row['theta0'])
            t1 = float(row['theta1'])
except (OSError, IOError):
    t0 = 0.0
    t1 = 0.0


dataSet = []
kms = []
plt.xlabel('mileage')
plt.ylabel('price')
plt.title('data')
try:
    with open('data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dataSet.append({'km':float(row['km']),'price':float(row['price'])})
            plt.plot([float(row['km'])], [float(row['price'])], 'ro')
            kms.append(float(row['km']))
except (OSError, IOError):
    print("failed to open data.csv")
    sys.exit()

kmstd = statistics.stdev(kms)
kmmean = float(sum(kms)) / max(len(kms), 1)

for i in range(0, len(dataSet)):
    dataSet[i]['km'] = (kms[i] - kmmean) / kmstd

learningRate = 0.1
iteration = 100
plt.figure(2)
plt.ylabel('prediction error')
plt.xlabel('iterations')
plt.title('gradient descent')
plots = []
for i in range(0, iteration):
    qt0, qt1 = 0.0, 0.0
    for data in dataSet:
        q = estimate.price(t0, t1, data['km']) - data['price']
        qt0 += q
        qt1 += q * data['km']
    tmpt0 = learningRate * (1.0 / float(len(dataSet))) * qt0
    tmpt1 = learningRate * (1.0 / float(len(dataSet))) * qt1
    t0 -= tmpt0
    t1 -= tmpt1
    plots.append(qt0)
plt.plot(plots)

plt.figure(1)
maxkm = max(kms)
minkm = min(kms)
sclmax = (maxkm - kmmean) / kmstd
sclmin = (minkm - kmmean) / kmstd
maxprc = estimate.price(t0, t1, sclmax)
minprc = estimate.price(t0, t1, sclmin)
plt.plot([maxkm, minkm], [maxprc, minprc])

try:
    with open('model.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|')
        writer.writerow(['theta0', 'theta1', 'kmstd', 'kmmean'])
        writer.writerow([t0, t1, kmstd, kmmean])
except Exception:
    print("failed to write model.csv")

plt.show()
