## Bookshelf

This is Bookshelf, a telegram bot that connects buyers and sellers of used books, with a focus on university textbooks. The bot utilizes Telegram's chat functionalities to simplify communication and increase the potential user base.

# Features

Bookshelf currently supports the following commands:

- `/start`: starts the bot and prints all the necessary informations to start using it correctly.
- `/insert`: allows users to insert a book into the database. The command requires the following information: book name, book author, price, book condition, and book location.
- `/showmybooks`: allows users to see the books they've added to the database.
- `/delete`: allows users to delete one of their books from the database by providing the book ID.
- `/searchbyauthor`: allows users to search for books in the database by author.
- `/searchbyname`: allows users to search for books in the database by name.
- `/buythisbook`: allows users to express interest in buying a book, which will put them in contact directly with the seller.

# Getting Started

1. To use Bookshelf, start a chat with the bot on Telegram by searching for @the_book_shelf_bot or clicking on this [link](https://t.me/the_book_shelf_bot/).
2. Use the commands listed above to add, search for, delete books in the database.
3. To buy a book use the `/buythisbook` command followed by the unique ID of the book, you will receive a link to contact directly the seller. The seller will also be notified of your interest.
4. Remember to ask all the necessary informations about the book that you are interest in: version of the book, photos to see the actual status.
5. If you sell a book please remember to delete such book from your entries, with the `/delete` command.

# Future Improvements

- Improvements on the `/delete` command, to take into account users forgetting to delete sold books.
- Better reminder to delete a sold book
- `/help` command that lists the all the commands, currently `/start` does that
- `/help` command could also use some contact information, email, github link
- Improvements on cosmetic parts of the bot, picture, about, etc.
- `Category` field, either we let the seller add that or we can retrieve this information from the GoogleBooks API.
- It might be useful to use regex syntax to compare the name inserted by the seller with GoogleBooks, in order to minimize typos. Something like 'Do you mean ###?'
- should we get the API from GoogleBook to add the cover image to the query ouput?

# Contributing

Contributions to Bookshelf are welcome! If you'd like to contribute, please fork the repository and submit a pull request with your changes.
