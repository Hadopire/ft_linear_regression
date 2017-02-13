import sys
import csv
import estimate

t0, t1, kmmean, kmstd = 0.0, 0.0, 0.0, 1.0
try:
    with open('model.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            t0 = float(row['theta0'])
            t1 = float(row['theta1'])
            kmmean = float(row['kmmean'])
            kmstd = float(row['kmstd'])
except (OSError, IOError):
    t0 = 0.0
    t1 = 0.0
    kmmean = 0.0
    kmstd = 1.0

try:
    mileage = float(input("Enter mileage: "))
    mileage = (mileage - kmmean) / kmstd
    print(estimate.price(t0, t1, mileage))
except Exception:
    print("Expected integer value")
