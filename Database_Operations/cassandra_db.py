import os.path
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import csv
import pandas as pd

class Database:
    def __init__(self):
        self.client_id = "rNTkOuTYbvMPMhsRvFHvvGvx"
        self.client_secret = "L+rDktsHzbtwcFsb_vp+Xp.E80sRsvN_tXCEqATWTUKO,8g3yrNU6IaOHyu8eEO-lZq,RsMaO4oqjR,siwzpu264e9TDNapzuYC+uiHWYzJBxwUxubjtk91AwySozpRT"
        self.secure_bundle = ".\secure-connect-akshat (1).zip"

    def connect_db(self):
        try:
            cloud_config = {
                'secure_connect_bundle': self.secure_bundle
            }
            auth_provider = PlainTextAuthProvider(self.client_id, self.client_secret)
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            self.session = cluster.connect()

            row = self.session.execute("select release_version from system.local").one()
            if row:
                print(row[0])
            else:
                print("An error occurred.")
        except Exception as e:
            raise e

    def create_table(self, keyspace, table_name):
        try:
            self.connect_db()
            self.session.execute(f"create table {keyspace}.{table_name}(index_col int PRIMARY KEY, text text, class text);")
        except Exception as e:
            return e

    def insert_records(self, filename):
        try:
            self.connect_db()
            with open(filename, 'r') as data:
                next(data)
                data_csv = csv.reader(data, delimiter=',')
                for i in data_csv:
                    print(i)
                    self.session.execute("insert into spam_ham.data(index_col, text, class) values (%s,%s,%s);",
                                    [int(i[2]), i[1], i[0]])
        except Exception as e:
            return e

    def fetch_records(self, keyspace, table_name):
        try:
            self.connect_db()
            data = self.session.execute(f"select * from {keyspace}.{table_name};")
            return data
        except Exception as e:
            return e

    def database_to_csv(self, keyspace, table_name):
        try:
            data = self.fetch_records(keyspace, table_name)
            dest = "Database Files"
            index_list, text_list, class_list = [], [], []
            data_dict = {}
            for data_ in data:
                index_list.append(data_[0])
                text_list.append(data_[2])
                class_list.append(data_[1])
            data_dict['index'], data_dict['text'], data_dict['class'] = index_list, text_list, class_list
            database_df = pd.DataFrame(data_dict)
            database_df.to_csv('data.csv', index=False)
            src = os.getcwd()
            src = src + '\data.csv'
            shutil.move(src, dest)
            # database_df.to_csv(path, index=False)
        except Exception as e:
            raise e