import psycopg # type: ignore -> Just so we don't have constantly get an import warning.

try:
    with psycopg.connect(
        dbname="photon"
    ) as conn:
        with conn.cursor() as curs:
			# Puts highest ID at top of table
            curs.execute("""
            SELECT * FROM players
			ORDER BY id DESC;
            """)
            
            # Saves highest ID as variable
            highestID = curs.fetchone()[0]
            
            # Gets codename value
            nameToAdd = str(input("What is the first player's codename? "))
            
            # Inserts codename and ID into DB
            curs.execute(f"INSERT INTO players (id, codename) VALUES (%s, %s);",
            (highestID + 1, nameToAdd,))
            
            # Gets codename value
            nameToAdd = str(input("What is the second player's codename? "))
            
            # Inserts codename and ID into DB
            curs.execute(f"INSERT INTO players (id, codename) VALUES (%s, %s);",
            (highestID + 2, nameToAdd,))
            
            # Prints out entire table
            curs.execute("""
            SELECT * FROM players;
            """)
            print(curs.fetchall())
            
        
    print("Players added successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
