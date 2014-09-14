from common import data

dog1 = data.Subject('Dog', 1)

print 'Methode hourSegments :'
for hourSegment in dog1.hourSegments('preictal'):
    print hourSegment

print '---'

print 'Methode subSegments :'
i = 0
hourSegments = dog1.hourSegments('preictal')
hourSegment = hourSegments.next()
segments = hourSegment.subSegments(10)
while i < 3:
    print segments.next()
    i += 1
