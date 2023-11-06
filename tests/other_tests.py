from datetime import datetime
import re

#print(type(datetime.now()), datetime.now())

a = "     login password     "
words = re.findall(r"\b\S+\b", a)
print(words, type(words))