from matplotlib import pyplot
from levels import *

Z = level46

pyplot.figure(figsize=(10, 5))
pyplot.imshow(Z, cmap=pyplot.cm.binary, interpolation='nearest')
pyplot.xticks([]), pyplot.yticks([])
pyplot.show()
