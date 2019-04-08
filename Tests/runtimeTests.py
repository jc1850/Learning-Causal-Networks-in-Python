import cProfile
import sys
sys.path.append('src')
import pc
from indepTests import chi
data = pc.PCAlg.prepare_data('data/alarm_10000.dat', isLabeled = True)
PCA = pc.PCAlg(data, chi, 0.05)
cProfile.run('PCA.learnGraph()', sort ='cumtime')