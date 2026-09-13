import psycopg

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
            nameToAdd = str(input("What is your codename? "))
            
            # Inserts codename and ID into DB
            curs.execute(f"INSERT INTO players (id, codename) VALUES (%s, %s);",
            (highestID + 1, nameToAdd,))
            
            # Prints out entire table
            curs.execute("""
            SELECT * FROM players;
            """)
            print(curs.fetchall())
            
        
    print("Okay database stuff kinda works")

except Exception as e:
    print(f"An error occurred: {e}")
