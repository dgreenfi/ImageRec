import sklearn
import numpy as np
from sklearn import svm
import json

def top_labels(labels,probabilities,n):
    ind=range(0,probabilities.size)
    #sort by index
    order=np.array([x for (y,x) in sorted(zip(probabilities[0],ind),reverse=True)])
    #return labels where the index
    return labels[order[0:n]]



def load_train():
    filename='./data/labels.txt'
    jlist=[]
    with open(filename) as f:
        lines = f.read().splitlines()
    for line in lines:
        jlist.append(json.loads(line))
    return jlist

def main():
    ##load features
    f ='/Users/davidgreenfield/Downloads/features_csv_tmp.csv'
    #f ='/Users/davidgreenfield/Downloads/features_f500.csv'
    cols=range(1,4096)
    feats =np.loadtxt(open(f,"rb"),delimiter=",",skiprows=1,usecols=(cols))
    asins = np.loadtxt(open(f,"rb"),delimiter=",",skiprows=1,usecols=([0]),dtype=str)

    ##load labels
    t=load_train()
    sample=[{'B004U7FWZC':"black"},{'B009AG91KU':"brown"}]
    labels=t
    ## assemble training set
    Y=[]
    X=[]
    for litem in labels:
        for key in litem.keys():
            try:
                f=feats[np.where(asins==key)][0]
                X.append(f)
                Y.append(litem[key])
            except IndexError:
                pass
    print X
    print Y

    ##train classifier
    #http://scikit-learn.org/stable/modules/svm.html#multi-class-classification
    clf = svm.SVC(decision_function_shape='ovo')
    clf.fit(X, Y)
    #dec = clf.decision_function([[f[123]]])
    #dec.shape[1] # 4 classes: 4*3/2 = 6
    clf.decision_function_shape = "ovr"
    outfile=open('./data/pred_labels.txt','a')

    for x in range(10,100):
        dec = clf.decision_function([feats[x]])

        predicted= clf.predict([feats[x]])
        labels= clf.classes_
        outfile.write( asins[x]+ " ")
        outfile.write(",".join(top_labels(labels,dec,3))+'\n')
        print predicted
        print dec





    ##run on non-classified


    ##output classifications


if __name__ == '__main__':

   main()