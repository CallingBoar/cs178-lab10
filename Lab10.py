
import boto3

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('RainWorldSongs')

REGION = "us-east-1"
TABLE_NAME = "RainWorldSongs"

def create_movie():
    """
    Prompt user for a Movie Title.
    Add the movie to the database with the title and an empty Ratings list.
    """
    # Source - https://stackoverflow.com/a/33649402
    # Posted by omuthu, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-03-05, License - CC BY-SA 4.0

    input_title = input("What's the title of your song? ")

    table.put_item(TableName='RainWorldSongs', Item={'Title':input_title,'Ratings':[]})

    print("creating a song")

def print_movie(song):
    title = song.get("Title", "Unknown Title")
    ratings = song.get("Ratings", "No ratings")
    runtime = song.get("Runtime", "Unknown Runtime")

    print(f"  Title  : {title}")
    print(f"  Ratings: {ratings}")
    print(f"  Runtime: {runtime}")
    print()

def get_table():
    """Return a reference to the DynamoDB Movies table."""
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    return dynamodb.Table(TABLE_NAME)

def print_all_movies():
    """Scan the entire Movies table and print each item."""
    table = get_table()

    # scan() retrieves ALL items in the table.
    # For large tables you'd use query() instead — but for our small
    # dataset, scan() is fine.
    response = table.scan()
    items = response.get("Items", [])

    if not items:
        print("No songs found. Make sure your DynamoDB table has data.")
        return

    print(f"Found {len(items)} movie(s):\n")
    for song in items:
        print_movie(song)

def update_rating():
    """
    Prompt user for a Movie Title.
    Prompt user for a rating (integer).
    Append the rating to the movie's Ratings list in the database.
    """
    title = input("What is the song title? ")
    try:
        rating = int(input("What is the rating (integer): "))
    except:
        print("bru that's not an integer")
        return

    try:
        print("updating rating")
        table.update_item(
            Key={"Title": title},
            UpdateExpression="SET Ratings = list_append(Ratings, :r)",
            ExpressionAttributeValues={':r': [rating]}
            )
        print("updating rating")
    except:
        print("That song does not exist :(")

def delete_movie():
    """
    Prompt user for a Movie Title.
    Delete that item from the database.
    """
    input_title = input("What song would you like to delete? ")
    table.delete_item(
    Key={
        'Title': input_title
    }
)
    print("deleting song")

def query_movie():
    """
    Prompt user for a Movie Title.
    Print out the average of all ratings in the movie's Ratings list.
    """
    input_title = input("What song would you like to find the average rating of? ")

    response = table.get_item(
    Key={
        'Title': input_title
        }
    )
    song = response.get("Item")
    try:
        rating_list = song['Ratings']
    except:
        print("That song does not exist :(")

    try:
        print("The average of this song's ratings is:", sum(rating_list) / len(rating_list))
    except:
        print("That song has no ratings. Be the first to rate it!")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new song")
    print("Press R: to READ all songs")
    print("Press U: to UPDATE a song (add a review)")
    print("Press D: to DELETE a song")
    print("Press Q: to QUERY a song's average rating")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_movie()
        elif input_char.upper() == "R":
            print_all_movies()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_movie()
        elif input_char.upper() == "Q":
            query_movie()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()
