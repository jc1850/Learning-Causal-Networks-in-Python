import cProfile
import sys
sys.path.append('src')
import fci
from indepTests import chi
data = fci.FCIAlg.prepare_data('data/asia_1000.data', isLabeled = True)
PCA = fci.FCIAlg(data, chi, 0.05)
cProfile.run('PCA.learnGraph()', sort ='cumtime')