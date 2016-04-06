import sklearn
import numpy as np
from sklearn import svm

def main():
    ##load features
    #f ='/Users/davidgreenfield/Downloads/features_csv_tmp.csv'
    f ='/Users/davidgreenfield/Downloads/features_f500.csv'
    cols=range(1,4096)
    feats =np.loadtxt(open(f,"rb"),delimiter=",",skiprows=1,usecols=(cols))
    asins = np.loadtxt(open(f,"rb"),delimiter=",",skiprows=1,usecols=([0]),dtype=str)

    ##load labels
    sample={'B0019JYU4I':["brown","leather","thick sole"],'B004016KRC':["black","high boot","leather"]}

    ## assemble training set

    ##train classifier
    #http://scikit-learn.org/stable/modules/svm.html#multi-class-classification
    X = [[0,1], [1,2], [2,3], [3,4]]
    Y = ["Small", "med", "large", "XL"]
    clf = svm.SVC(decision_function_shape='ovo')
    clf.fit(X, Y)
    dec = clf.decision_function([[1,2]])
    dec.shape[1] # 4 classes: 4*3/2 = 6
    clf.decision_function_shape = "ovr"
    dec = clf.decision_function([[1,2]])
    print dec.shape[1],dec # 4 classes
    print clf.predict([[1,2]])


    ##run on non-classified


    ##output classifications


if __name__ == '__main__':

   main()