from common import data

dog1 = data.Subject('Dog', 1)

i = 0
for segment in dog1.hour_segments('preictal'):
    i += 1

print i