import csv
import json

def load_data(path):
    lookup_dict={}
    with open(path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            lookup_dict[row[4]]={"url":row[6]}
    return lookup_dict

def main():
    file='/Users/davidgreenfield/Downloads/reviews_Clothing_Shoes_and_Jewelry.json'
    f=open(file,'r')
    data=f.readlines()

    fo=open('./data/reviews_boots.json','w')
    ids=load_data('./data/boots_aws.csv')
    id_keys=ids.keys()
    for line in data:
        rec= json.loads(line)
        if rec['asin'] in id_keys:
            fo.write(line)
    print data[0]


if __name__ == '__main__':
    main()