import sqlite3
import os
import csv
from tkinter.filedialog import askdirectory


def read_csv(file_path):
    data = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data.append(
                row
            )
    return data


# expect data to be a list of lists that contain data to add to db
def insert_many(data, filename):
    # skip first line if necessary
    if data[0][0] == 'PT. #':
        data.pop(0)
    conn = sqlite3.connect('bridge.db')
    c = conn.cursor()
    try:
        c.executemany("""INSERT INTO bridge
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, data)
        print("Inserted data from " + filename + " to database")
    except sqlite3.IntegrityError as e:
        print("You have already added file " + filename + " to database")

    conn.commit()
    conn.close()


path = askdirectory(title='Select A Folder Full Of TABLES')  # shows dialog box and return the path

for file in os.listdir(path):
    if file.endswith(".csv"):
        csv_path = path + "/" + file
        csv_data = read_csv(csv_path)
        insert_many(csv_data, file)

