import configparser
from telethon import TelegramClient, events
import sqlite3
from datetime import datetime

print("Initializing configurations...")

API_ID = "26464259"
API_HASH = "715c925fbcea1e1d8c34d99447ee1689"
BOT_TOKEN = "6260769580:AAHR8JWrQzBawUi_qMSKyhAAjvRfrGDu-OQ"
session_name = "/home/filippoferrari/Documents/book_test/sessions/Bot"


# Start the bot session
client = TelegramClient(session_name, API_ID, API_HASH).start(bot_token=BOT_TOKEN)


@client.on(events.NewMessage(pattern="(?i)/start"))
async def start(event):
    sender = await event.get_sender()
    SENDER = sender.id
    text = "Benvenuto nel bot di compravendita di libri usati, usa /help per vedere la lista di comandi disponibili"
    await client.send_message(SENDER, text, parse_mode='html')


######
###### INSERT COMMAND
######

# Insert command
@client.on(events.NewMessage(pattern="(?i)/insert"))
async def insert(event):
    try:
        # Get the sender of the message
        sender = await event.get_sender()
        SENDER = sender.id

       # Get the text of the user AFTER the /insert command and split it into a list using the first space as the separator
        message_text = event.message.text.strip()
        command_parts = message_text.split(" ", 1)
        if len(command_parts) < 2:
            raise ValueError("Invalid command format")
        
        # Get the book details by splitting the remaining message using commas as the separator
        book_parts = command_parts[1].split(",")
        if len(book_parts) != 5:
            raise ValueError("Invalid book details format")
        book_name = book_parts[0].strip()
        book_author = book_parts[1].strip()
        book_price = book_parts[2].strip()
        book_status = book_parts[3].strip()
        book_location = book_parts[4].strip()
        dt_string = datetime.now().strftime("%d/%m/%Y") # Use the datetime library to the get the date (DAY/MONTH/YEAR)


        # Create the tuple "params" with all the parameters inserted by the user
        params = (book_name, book_author, book_price, book_status, book_location, SENDER, dt_string)
        sql_command = "INSERT INTO orders VALUES (NULL, ?, ?, ?, ?, ?, ?, ?);" # the initial NULL is for the AUTOINCREMENT id in the database
        crsr.execute(sql_command, params) # Execute the query
        conn.commit() # commit the changes

        # If at least 1 row is affected by the query we send specific messages
        if crsr.rowcount < 1:
            text = "Something went wrong, please try again"
            await client.send_message(SENDER, text, parse_mode='html')
        else:
            text = "Book correctly inserted"
            await client.send_message(SENDER, text, parse_mode='html')


    except Exception as e:
        print(e)
        await client.send_message(SENDER, "<b>Conversation Terminated✔</b>", parse_mode='html')
        return


######
###### SHOWMYBOOKS COMMAND
######

# Function that creates a message the contains a list of all the books
def create_message_select_query(ans):
    text = ""
    for i in ans:
        id = i[0]
        book_name = i[1]
        book_author = i[2]
        book_price = i[3]
        book_status = i[4]
        book_location = i[5]
        sender = i[6]
        creation_date = i[7]
        text += "<b>" + str(id) +"</b> | " + "<b>"+ str(book_name) +"</b> | " + "<b>"+ str(book_author) +"</b> | " + "<b>"+ str(book_price)+"</b> | " + "<b>"+ str(book_status)+"</b> |  " + "<b>"+ str(book_location)+"</b> | " + "<b>"+ str(sender)+"</b> | " + "<b>"+ str(creation_date)+"</b>\n"
    message = "<b>Received 📖 </b> Information about orders:\n\n"+text
    return message



@client.on(events.NewMessage(pattern="(?i)/showmybooks"))
async def select(event):
    try:
        # Get the sender of the message
        sender = await event.get_sender()
        SENDER = sender.id
        # Execute the query and get all (*) the oders
        crsr.execute("SELECT * FROM orders WHERE SENDER = ?", (SENDER,)) # Make sure the query is ONLY for books of a specific user
        res = crsr.fetchall() # fetch all the results

        # If there is at least 1 row selected, print a message with the list of all the oders
        # The message is created using the function defined above
        if(res):
            testo_messaggio = create_message_select_query(res)
            await client.send_message(SENDER, testo_messaggio, parse_mode='html')
        # Otherwhise, print a default text
        else:
            text = "No orders found inside the database."
            await client.send_message(event.chat_id, testo_messaggio, parse_mode='html')

    except Exception as e:
        print(e)
        await client.send_message(SENDER, "<b>Conversation Terminated✔</b>", parse_mode='html')
        return
    

######
###### DELETE COMMAND
######

## /delete x     where "x" is the id of the book, no other values needed
## BUGTESTING STILL REQUIRED FOR FIELD INPUT ##

@client.on(events.NewMessage(pattern="(?i)/delete"))
async def delete(event):
    try:
        # Get the sender
        sender = await event.get_sender()
        SENDER = sender.id

        # get list of words inserted by the user
        list_of_words = event.message.text.split(" ")
        id = list_of_words[1] # The second (1) element is the id

        # Crete the DELETE query passing the is as a parameter
        sql_command = "DELETE FROM orders WHERE id = (?);"
        ans = crsr.execute(sql_command, (id,))
        conn.commit()
        
        # If at least 1 row is affected by the query we send a specific message
        if ans.rowcount < 1:
            text = "Order with id {} is not present".format(id)
            await client.send_message(SENDER, text, parse_mode='html')
        else:
            text = "Order with id {} correctly deleted".format(id)
            await client.send_message(SENDER, text, parse_mode='html')

    except Exception as e: 
        print(e)
        await client.send_message(SENDER, "<b>Conversation Terminated✔️</b>", parse_mode='html')
        return
    


######
###### DELETE COMMAND
######

#create a function that searches a book by name
def search_book_by_name(book_name):
    sql_command = "SELECT * FROM orders WHERE name = ?;"
    crsr.execute(sql_command, (book_name,))
    rows = crsr.fetchall
    return rows


######
###### SEARCH BY NAME COMMAND
######

@client.on(events.NewMessage(pattern="^/searchbyname"))
async def search_by_name(event):
    try:
        # Get the sender
        sender = await event.get_sender()
        SENDER = sender.id

        # get list of words inserted by the user
        list_of_words = event.message.text.split(" ")
        book_name = " ".join(list_of_words[1:])  # Join all the words from the list except the command name

        # Create the SELECT query
        sql_command = "SELECT * FROM orders WHERE LOWER(book_name) LIKE LOWER('%{}%')".format(book_name)

        # Execute the query
        crsr.execute(sql_command)
        result = crsr.fetchall()

        # If no result is found, we send a message to inform the user
        if not result:
            text = "No book found with the name '{}'. Please try again with a different name.".format(book_name)
            await client.send_message(SENDER, text, parse_mode='html')
        else:
            # Build the message to send to the user with all the books information
            text = "Books found with the name '{}':\n".format(book_name)
            for row in result:
                text += "Name: {}\nAuthor: {}\nPrice: {}\nStatus: {}\nLocation: {}\nDate of upload: {}\n\n".format(row[1], row[2], row[3], row[4], row[5], row[7])

            await client.send_message(SENDER, text, parse_mode='html')

    except Exception as e: 
        print(e)
        await client.send_message(SENDER, "<b>Conversation Terminated✔️</b>", parse_mode='html')
        return



########################################################################################################
##### MAIN
if __name__ == '__main__':
    try:
        print("Initializing Database...")
        # Connect to local database
        db_name = '/home/filippoferrari/Documents/book_test/test-database.db' # Insert the database name. Database is the folder
        conn = sqlite3.connect(db_name, check_same_thread=False)
        # Create the cursor
        # The cursor is an instance using which you can invoke methods that execute SQLite statements, fetch data from the result sets of the queries.
        crsr = conn.cursor()
        print("Connected to the database")

        # Command that creates the "oders" table 
        sql_command = """CREATE TABLE IF NOT EXISTS orders ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            book_name VARCHAR(300),
            book_author VARCHAR(300), 
            book_price VARCHAR(100),
            book_status VARCHAR(200),
            book_location VARCHAR(200),
            SENDER VARCHAR(300),
            LAST_EDIT VARCHAR(100));"""
        crsr.execute(sql_command)
        print("All tables are ready")

        print("Bot Started")
        client.run_until_disconnected()

    except Exception as error:
        print('Cause: {}'.format(error))

                                                                                                                                                                                                                                                                                                                                                                                                
