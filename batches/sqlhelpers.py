import numpy as np



import pymysql

create_command="CREATE TABLE features (id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,asin char(10),cluster int,fid int,fval double)"



def sql_to_matrix():
    USER='imagerecuser'
    DB='imagerecDB'
    DBP='convolutional'
    HOST='imagerec.cxypyuuzuvjh.us-east-1.rds.amazonaws.com'

    conn = pymysql.connect(host=HOST, port=3306, user=USER, passwd=DBP, db=DB)
    cur = conn.cursor()
    clustnum=0
    import time

    start = time.time()


    cur.execute("SELECT asin from features WHERE cluster="+str(clustnum)+" GROUP BY asin")
    clust= cur.fetchall()
    asins = [x[0] for x in clust]
    matr=np.zeros((len(asins),4097))
    #print asins
    #for asin in clust:
    cur.execute("SELECT * from features WHERE cluster="+str(clustnum))
    feats=cur.fetchall()
    for row in feats:
        #row (sqlid,asin,cluster,fid,fval)
        # (1, 'B009XSN76O', 0, 8, 1.96949994564)
        #set val
        matx=asins.index(row[1])
        matr[matx][row[3]]=row[4]
        #set cluster val
        matr[matx][1]=row[2]
    matr_fin=np.c_[np.transpose(np.matrix(asins)),matr]
    end = time.time()
    print(end - start)





if __name__!='main':
    sql_to_matrix()