USER='imagerecuser'
DB='imagerecDB'
DBP='convolutional'
HOST='imagerec.cxypyuuzuvjh.us-east-1.rds.amazonaws.com'


import pymysql
import numpy as np

create_command="CREATE TABLE features (id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,asin char(10),cluster int,fid int,fval double)"


conn = pymysql.connect(host=HOST, port=3306, user=USER, passwd=DBP, db=DB)
cur = conn.cursor()
## Table manage commands
#cur.execute(create_command)
#cur.execute("DROP TABLE features")
cur.execute("SHOW TABLES")
## Insertion commands
add_feat = "INSERT INTO features (asin,cluster,fid,fval) VALUES(%s,%s,%s,%s)"
cur.execute("SHOW fields from features")
print cur.fetchall()


### load features
f ='/Users/davidgreenfield/Downloads/features_csv_tmp.csv'
f ='/Users/davidgreenfield/Downloads/features_f500.csv'
cols=range(1,4097)
feats =np.loadtxt(open(f,"rb"),delimiter=",",skiprows=1,usecols=(cols))
asins = np.loadtxt(open(f,"rb"),delimiter=",",skiprows=1,usecols=([0]),dtype=str)
for i in range(0,len(asins)):
    for x in range(0,4096):
        if feats[i][x]>0:
            vals=[asins[i]]+[str(int(x/100))]+[str(x)]+[str(feats[i][x])]
            cur.execute(add_feat,vals)
conn.commit()
cur.execute("SELECT * from features")