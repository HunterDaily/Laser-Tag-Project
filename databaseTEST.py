import psycopg

try:
    with psycopg.connect(
        host="localhost",
        dbname="proton",
        port="5432"
    ) as conn:
        pass
        
    print("Okay database stuff kinda works")

except Exception as e:
    print(f"An error occurred: {e}")