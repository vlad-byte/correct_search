import csv
import time
from init import Speller


spell = Speller()
start = time.time()
p = spell(input("Введите ваш запрос: ")).lower().split()
with open("Database.csv", encoding='ANSI') as r_file:
    file_reader = csv.reader(r_file, delimiter=";")
    count = 0
    for row in file_reader:
        t = True
        for j in p:
            if j not in row[1].lower():
                t = False
        if t:
            print(f'    {row[0]} - {row[1]}')
            count += 1
    print(f'Всего {count} совпадений')
end = time.time()
print("The time of execution of above program is :",
      (end-start) * 10**3, "ms")
