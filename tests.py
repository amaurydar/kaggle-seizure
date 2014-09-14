from common import data

dog1 = data.Subject('Dog', 1)

i = 0
for segment in dog1.hour_segments('preictal'):
    i += 1
print 'Nombre de segments d\'une heure pour Dog_1 : %s' % i

print '---'

for segment in dog1.hour_segments('preictal'):
    print 'Premier segment d\'une heure de Dog_1 :'
    print 'Data (matrice de taille %s) :' % str(segment.data.shape)
    print segment.data
    print 'Duree : %s secondes' % segment.length
    print 'Temps entre le debut du segment et la seizure : %s secondes' % segment.time_to_seizure
    break