import psycopg2

if __name__ == "__main__":
    pass_path = "D:\\Programs\\PostgresSQL\\1_pass.txt"
    password = ''
    with open(pass_path, 'r') as file:
        password = file.read()
    conn = psycopg2.connect(database="electronics", user="postgres", password=password)
    cur = conn.cursor()

    table_name = "items"

    cur.execute("""
        SELECT constraint_name, constraint_type
        FROM information_schema.table_constraints
        WHERE table_name = %s
    """, (table_name,))

    constraints = cur.fetchall()

    if constraints:
        print("Foreign keys for the table ", table_name, "were found:")
        for constraint in constraints:
            constraint_name, constraint_type = constraint
            print("Name:", constraint_name)
            print("Type:", constraint_type)
    else:
        print("Foreign keys for the table", table_name, "weren't found.")

    cur.close()
    conn.close()
