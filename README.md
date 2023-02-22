# Book Bot

This is a Telegram bot that allows users to buy and sell books. The bot currently supports the following commands:

- `/insert`: allows users to insert a book into the database. The command requires the following information: book name, book author, price, book condition, and book location.
- `/showmybooks`: allows users to see the books they've added to the database.
- `/delete`: allows users to delete one of their books from the database by providing the book ID.
- `/searchbyauthor`: allows users to search for books in the database by author.
- `/searchbyname`: allows users to search for books in the database by name.
- `/search`: allows users to search for books in the database by name or author.
- `/update`: allows users to update the information of a book they have added to the database.
- `/iwanttobuythat`: allows users to express interest in buying a book, which will put them in contact with the seller.

To use the bot, search for "@booktest_bot" on Telegram.

## Future Improvements

- Bug testing for `/delete` and `/searchbyauthor` commands.
- Logic to put two users in contact for the buying process.
- /help command that lists the commands
- reminder to delete a sold book
- `Category` field, either we let the seller add that or we can retrieve this information from the GoogleBooks API.
- It might be useful to use regex syntax to compare the name inserted by the seller with GoogleBooks, in order to minimize typos. Something like 'Do you mean ###?'
- should we get the API from GoogleBook to add the cover image to the query ouput?
