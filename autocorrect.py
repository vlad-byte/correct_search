import time
from init import Speller

start = time.time()
spell = Speller()
print(spell(input("Введите ваш запрос: ")))
end = time.time()
print("The time of execution of above program is :",
      (end-start) * 10**3, "ms")
