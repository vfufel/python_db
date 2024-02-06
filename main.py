import psycopg2

def create_db(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS client (
        client_id   SERIAL      PRIMARY KEY,
        first_name  VARCHAR(40) NOT NULL,
        last_name   VARCHAR(40) NOT NULL,
        email       VARCHAR(40) NOT NULL UNIQUE
    );    
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS number ( 
        number_id    SERIAL      PRIMARY KEY,
        client_id    SERIAL      REFERENCES client(client_id),
        phone_number VARCHAR(15) UNIQUE
    );
    """)
    conn.commit()

def add_client(cur, first_name, last_name, email):
    try:
        cur.execute("""
        INSERT INTO client(first_name, last_name, email) VALUES(%s, %s, %s);
        """, (first_name, last_name, email))
        conn.commit()
    except psycopg2.errors.UniqueViolation as e:
        return print(f"Email {email} already exists for this client.")

def add_phone(cur, client_id, phone_number):
    try:
        cur.execute("""
        INSERT INTO number(client_id, phone_number) VALUES(%s, %s);
        """, (client_id, phone_number))
    except psycopg2.errors.UniqueViolation as e:
        return print(f'Phone number {phone_number} already exists for this client.')

def change_client(cur, client_id, modification, object):
    match modification:
        case "first_name":
            cur.execute("""
            UPDATE client SET first_name = %s WHERE client_id = %s;
            """, (object, client_id))
        case "last_name":
            cur.execute("""
            UPDATE client SET last_name = %s WHERE client_id = %s;
            """, (object, client_id))
        case "email":
            cur.execute("""
            UPDATE client SET email = %s WHERE client_id = %s;
            """, (object, client_id))
    conn.commit()

def delete_phone(cur, client_id, phone_number):
    cur.execute("""
    DELETE FROM number WHERE client_id = %s AND phone_number = %s;
    """, (client_id, phone_number))
    conn.commit()

def delete_client(cur, client_id):
    try:
        cur.execute("""
           DELETE FROM client WHERE client_id = %s;
           """, (client_id,))
    except psycopg2.errors.ForeignKeyViolation as e:
        return print(f"Please delete associated phone numbers first.")

def find_client(cur, first_name=None, last_name=None, email=None, phone_number=None):
    cur.execute("""
    SELECT c.first_name, c.last_name, c.email, n.phone_number
    FROM client c
    LEFT JOIN number n ON c.client_id = n.client_id
    WHERE 
        (c.first_name = %s OR %s IS NULL) AND
        (c.last_name = %s OR %s IS NULL) AND
        (c.email = %s OR %s IS NULL) AND
        (n.phone_number = %s OR %s IS NULL);
    """, (first_name, first_name, last_name, last_name, email, email, phone_number, phone_number))

    result = cur.fetchall()

    if not result:
        return print("Client not found.")

    return print(result)

with psycopg2.connect(database="python_db_test", user="postgres", password="Internet2536") as conn:
    with conn.cursor() as cur:
        # create_db(cur)

        # add_client(cur, 'Vladislav', 'Bubelev', 'bubelev.vlad@gmail.com')

        # add_phone(cur, 6, '+375336848054')

        # add_phone(cur, 6, '+375447113645')

        # change_client(cur, 6, 'last_name', 'Melnikov')

        # delete_phone(cur, 6, '+375447113645')
        # delete_phone(cur, 6, '+375336848054')

        # delete_client(cur, 6)

        # result_by_name = find_client(cur, first_name='Vladislav')
        # result_by_last_name = find_client(cur, last_name='Bubelev')
        # result_by_email = find_client(cur, email='bubelev.vlad@gmail.com')
        # result_by_phone = find_client(cur, phone_number='+375336848054')

conn.close()