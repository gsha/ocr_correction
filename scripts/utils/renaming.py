import os

path = r'C:\Progs\solr-5.0.0\solr-5.0.0\server\data\images\Al-Hayat\9'
for file in os.listdir(path):
    os.rename(os.path.join(path, file), os.path.join(path, file[2:]))