# migrate_csv_to_mysql.py
# Migrates data from CSV file to MySQL database

# STEP 1: Import what we need
import csv                                              # Python bulit-in CSV reader
from database import get_connection, close_connection   # Our database functions
from mysql.connector import Error                       # For handing database error

#Step 2: Function to insert one country into a database
def insert_country(connection, name, capital, population, area):
    """
    Insert a single country record into the database.

    Args:
        connection: MySQL connection object (the open door to database)
        name: Country name(string)
        capital: Capital city (string)
        population: Population number (string from CSV, will convert to int)
        area: Area in km² (string from CSV, will convert to float)

    Returns:
        bool: True if sucessful, False otherwise
    """
    #Create a cursor - this is like a "pointer" that that run SQL commmands
    cursor = connection.cursor()

    try:
        # Step 2a: Clean up the capital field
        # Handle "None" string and empty values from CSV
        capital = None if capital == "None" or capital == "" else capital

        # Step 2b: Convert population to integer
        # CSV  give us strings, but database needs numbers
        try:
            population = int(population) if population and population != "" else None
        except (ValueError, TypeError):
            # If conversion fails (bad data), set to none
            population = None

        # Step 2c: Convert area to decimal number
        # Handle scientific notation like "1.4E7" (14000000)
        try:
            if area and area != "":
                area = float(area) # Float() handles scientific notation
            else:
                area = None
        except (ValueError, TypeError):
            # If conversion fails, set to None
            area = None

        # Step 2d: Create SQL INSERT command
        # %s are placeholder - we'll fill them in with actual values
        insert_query = """
            INSERT INTO countries (name, capital, population, area)
            VALUES (%s, %s, %s, %s)
        """

        # Tuple of values to insert (matches the % placeholders)
        values = (name, capital, population, area)

        # Execute the SQL command with the vaules
        cursor.execute(insert_query, values)

        #Commit = save the changes to the database (like saving a file)
        connection.commit()

        return True #Success!

    except Error as e:
        # STEP 2e Handle errors gracefully
        # If duplicate entry error, that okay - just skip it
        if "Duplicate entry" in str(e):
            print(f"⚠️  Skipping duplicate: {name}")
            return False
        else:
            # Other errors are real problems
            print(f"❌ Error inserting {name}: {e}")
            return False
    finally:
        # Always close the cursor, even if there was an error
        cursor.close()

# Step 3: Main function to read CSV and migrate all data
def migrate_csv_to_mysql(csv_filename="country_data.csv"):
    """
    Reads CSV file and inserts all data into MySQL database.

    Args:
        csv_filename: Path to the CSV file to migrate
    """
    #  Get a connection to the database
    connection = get_connection()

    # If connection failed, stop here
    if not connection:
        print("❌ Cannot proceed - database connnection failed")
        return

    try:
        # STEP 3a: Open the CSV file for reading
        # 'r' = read mode, encoding='utf-8' handles special characters
        with open(csv_filename, "r", encoding="utf-8") as csvfile:

            # DictReader automatically reads the header row and creates a dictionary
            # Each row becomes: {'Name': 'Andorra', 'Captial': 'Andorra la Vella', ...}
            reader = csv.DictReader(csvfile)

            #Counters to track our progress
            inserted_count = 0
            skipped_count = 0

            #STEP 3b: Loop throught each row in the CSV
            for row in reader:
                # Get data from the row dictionary
                # Handle typo in CSV header: "INName" instead of "Name"
                name = row.get("Name") or row.get("INName") or ""
                capital = row.get("Capital") or ""
                population = row.get("Population") or ""
                area = row.get("Area") or ""
                
                # Skip this row if no name is found
                if not name:
                    continue

                # STEP 3c: Insert into database
                if insert_country(connection, name, capital, population, area):
                    inserted_count += 1
                    # Print progress every 10 countries (so screen doesn't get flooded)
                    if inserted_count % 10 == 0:
                        print(f"✅ Inserted {inserted_count} countries...")
                else:
                    skipped_count +=1

        # STEP 3c: Print final summery
        print(f"\n🎉 Migration complete!")
        print(f"   ✅ Inserted: {inserted_count} countries")
        print(f"   ⚠️  Skipped: {skipped_count} countries")

    except FileNotFoundError:
        # CSV file doesn't exist
        print(f"❌ Error: Could not find this file '{csv_filename}'")
    except Error as e:
        #Database error
        print(f"❌ Database error: {e}")
    finally:
        #Always close the connection, even if there was an error
        close_connection(connection)
# STEP 4: Run migration if script is executed directly
if __name__ == "__main__":
    print("Starting CSV to MySQL migration...")
    print("=" * 50)
    migrate_csv_to_mysql()