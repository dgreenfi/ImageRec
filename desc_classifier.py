import sklearn
import numpy as np
from sklearn import svm

def top_labels(labels,probabilities,n):
    ind=range(0,probabilities.size)
    #sort by index
    order=np.array([x for (y,x) in sorted(zip(probabilities[0],ind))])
    #return labels where the index
    return labels[np.where(order<n)]



def main():
    ##load features
    #f ='/Users/davidgreenfield/Downloads/features_csv_tmp.csv'
    f ='/Users/davidgreenfield/Downloads/features_f500.csv'
    cols=range(1,4096)
    feats =np.loadtxt(open(f,"rb"),delimiter=",",skiprows=1,usecols=(cols))
    asins = np.loadtxt(open(f,"rb"),delimiter=",",skiprows=1,usecols=([0]),dtype=str)

    ##load labels
    sample={'B004U7FWZC':["black","leather","shiny"],'B009AG91KU':["brown","high boot","leather","cowboy boot"]}
    labels=sample
    ## assemble training set
    Y=[]
    X=[]
    for key in labels.keys():
        f=feats[np.where(asins==key)[0][0]]
        for label in sample[key]:
            X.append(f)
            Y.append(label)

    ##train classifier
    #http://scikit-learn.org/stable/modules/svm.html#multi-class-classification
    clf = svm.SVC(decision_function_shape='ovo')
    clf.fit(X, Y)
    #dec = clf.decision_function([[f[123]]])
    #dec.shape[1] # 4 classes: 4*3/2 = 6
    clf.decision_function_shape = "ovr"
    dec = clf.decision_function([feats[123]])

    predicted= clf.predict([feats[123]])
    labels= clf.classes_
    print  top_labels(labels,dec,3)


    ##run on non-classified


    ##output classifications


if __name__ == '__main__':

   main()