import random

import psycopg2
import csv
import os


def getCSV(dir_path):
    csv_files = [file[:-4] for file in os.listdir(dir_path) if file.endswith(".csv")]
    return csv_files


def shorteningTheLine(string, length=49):
    if len(string) > length:
        return string[:length]
    else:
        return string


def inputDataIntoTable(path_to_file, table_name, column_names, cursor, connection):
    i = 0
    with open(path_to_file + ".csv", 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            column1_value = shorteningTheLine(row[0])
            category = random.randint(0, 1)
            if path_to_file == 'computer_acessories':
                category = 0
            elif path_to_file == 'home_audio':
                category = 1
            column2_value = shorteningTheLine(row[1], 49)
            column3_value = shorteningTheLine(row[2], 49)
            column4_value = shorteningTheLine(row[3], 49)
            column5_value = shorteningTheLine(row[4], 150)

            insert_query = f"INSERT INTO {table_name} (id, category_id, {column_names[0]}, {column_names[1]}, {column_names[2]}, " \
                           f"{column_names[3]}, {column_names[4]}) VALUES " \
                           f"({i}, {category},'{column1_value}', '{column2_value}', '{column3_value}', '{column4_value}', '{column5_value}');"
            i += 1
            cursor.execute(insert_query)
            connection.commit()


if __name__ == '__main__':
    pass_path = "D:\\Programs\\PostgresSQL\\1_pass.txt"
    column_names = getCSV(os.getcwd())
    password = ''
    with open(pass_path, 'r') as file:
        password = file.read()
    conn = psycopg2.connect(database="electronics", user="postgres", password=password)
    cur = conn.cursor()
    create_table_query = f" CREATE TABLE IF NOT EXISTS Categories (id INTEGER,name VARCHAR(50));"
    cur.execute(create_table_query)
    conn.commit()
    for i in range(len(column_names)):
        insert_query = f"INSERT INTO Categories (id, name) VALUES ({i}, '{column_names[i]}')"
        cur.execute(insert_query)
        conn.commit()
    table2_columns = []
    with open(column_names[0] + ".csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            for i in range(len(row)):
                row[i] = row[i].capitalize()
            table2_columns = row
            break
        file.close()
    create_table_query = f"CREATE TABLE IF NOT EXISTS Items (id INTEGER, category_id INTEGER, {table2_columns[0]} VARCHAR(50), " \
                         f"{table2_columns[1]} VARCHAR(50), {table2_columns[2]} VARCHAR(50)," \
                         f" {table2_columns[3]} VARCHAR(50), {table2_columns[4]} VARCHAR(150));"
    cur.execute(create_table_query)
    conn.commit()

    for i in column_names:
        inputDataIntoTable(i, "Items", table2_columns, cur, conn)

    cur.execute("ALTER TABLE Categories ADD CONSTRAINT pk_category PRIMARY KEY (id)")
    conn.commit()

    cur.execute("ALTER TABLE Items ADD CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES Categories(id)")
    conn.commit()

    cur.execute("DELETE FROM items WHERE id NOT IN ( SELECT MIN(id) AS keep_id FROM items GROUP BY title, price HAVING COUNT(*) > 1 );")
    conn.commit()
    cur.close()
    conn.close()
