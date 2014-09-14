from common import data

dog1 = data.Subject('Dog', 1)

print 'Methode hour_segments :'
i = 0
for segment in dog1.hour_segments('preictal'):
    i += 1
print 'Nombre de hour_segment pour Dog_1 : %s' % i

for segment in dog1.hour_segments('preictal'):
    hour_segment1 = segment
    break
print 'Premier segment d\'une heure de Dog_1 :'
print hour_segment1

print '---'
print 'Methode segments :'
i = 0
segments = dog1.segments('preictal', 10)
while i < 3:
    print segments.next()
    i += 1
