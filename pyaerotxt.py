from pyqcm import XmlQCM
import sys

qcm = XmlQCM(sys.argv[1])

q = qcm.getRandom()

print q.display(True)
