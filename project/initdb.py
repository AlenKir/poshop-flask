import sqlite3

connection = sqlite3.connect('../database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO products (name, cost, image, description, category) VALUES (?, ?, ?, ?, ?)",
            ('Plain Envelopes', 6.45, "envelopes.jpg", "An envelope is a common packaging item, usually made of thin, flat material. It is designed to contain a flat object, such as a letter or card. These shapes allow for the making of the envelope structure by folding the sheet sides around a central rectangular area.", "Envelope")
            )

cur.execute("INSERT INTO products (name, cost, image, description, category) VALUES (?, ?, ?, ?, ?)",
            ('Merry Xmas Card', 10.9, "card.jpg", "A Christmas card is a greeting card sent as part of the traditional celebration of Christmas in order to convey between people a range of sentiments related to Christmastide and the holiday season. Christmas cards are usually exchanged during the weeks preceding Christmas Day by many people (including some non-Christians) in Western society and in Asia. The traditional greeting reads wishing you a Merry Christmas and a Happy New Year. There are innumerable variations on this greeting, many cards expressing more religious sentiment, or containing a poem, prayer, Christmas song lyrics or Biblical verse; others focus on the general holiday season with an all-inclusive Season's greetings. The first modern Christmas card was by John Calcott Horsley.", "Card")
            )

cur.execute("INSERT INTO products (name, cost, image, description, category) VALUES (?, ?, ?, ?, ?)",
            ('Standard Royal Stamps', 3.5, "stamp.jpg", "25 x Second Class Stamps. For use with Royal Mail post and at the Post Office. Image used for illustration purpose only", "Stamp")
            )

cur.execute("INSERT INTO products (name, cost, image, description, category) VALUES (?, ?, ?, ?, ?)",
            ('Fox Postcard', 1.7, "fox_card.jpg", "Send a piece of cozyness to a friend with this sweet fox hug postcard.", "Postcard")
            )

cur.execute("INSERT INTO products (name, cost, image, description, category) VALUES (?, ?, ?, ?, ?)",
            ('Merry Xmas White Card', 2.27, "white_card.jpg", "Let's start with simple and concise postcards from zokris.blogspot.nl White paper (cardboard), cuttings( printouts), some decorative elements and a beautiful postcard comes out!", "Postcard")
            )

cur.execute("INSERT INTO orders (ready, shipped, cost, priority) VALUES (?, ?, ?, ?)",
            (0, 0, 50.3, 1)
            )

cur.execute("INSERT INTO orders (ready, shipped, cost, priority) VALUES (?, ?, ?, ?)",
            (1, 0, 9.1, 2)
            )

cur.execute("INSERT INTO orders (ready, shipped, cost, priority) VALUES (?, ?, ?, ?)",
            (1, 1, 19.7, 3)
            )

cur.execute("INSERT INTO product_order (product_id, order_id) VALUES (?, ?)",
            (1, 1)
            )

cur.execute("INSERT INTO product_order (product_id, order_id) VALUES (?, ?)",
            (2, 1)
            )

cur.execute("INSERT INTO product_order (product_id, order_id) VALUES (?, ?)",
            (3, 2)
            )

cur.execute("INSERT INTO product_order (product_id, order_id) VALUES (?, ?)",
            (2, 3)
            )

cur.execute("INSERT INTO reviews (mark, text, author, product_id) VALUES (?, ?, ?, ?)",
            (3.0, "Fine.", "Anonymous", 1)
            )

cur.execute("INSERT INTO reviews (mark, text, author, product_id) VALUES (?, ?, ?, ?)",
            (5.0, "Awesome", "Anonymous", 1)
            )

cur.execute("INSERT INTO reviews (mark, text, author, product_id) VALUES (?, ?, ?, ?)",
            (1.0, "Aenean semper a sapien non commodo.", "Anonymous", 1)
            )

cur.execute("INSERT INTO reviews (mark, text, author, product_id) VALUES (?, ?, ?, ?)",
            (4.0, "Donec in rutrum tellus, eget condimentum felis.", "Anonymous", 2)
            )

cur.execute("INSERT INTO reviews (mark, text, author, product_id) VALUES (?, ?, ?, ?)",
            (4.0, "Aliquam erat volutpat. Fusce mattis mattis sapien, eget viverra purus.", "Anonymous", 3)
            )

cur.execute("INSERT INTO cart (product_id, user_id) VALUES (?, ?)",
            (1, 1)
            )

cur.execute("INSERT INTO cart (product_id, user_id) VALUES (?, ?)",
            (1, 2)
            )

cur.execute("INSERT INTO cart (product_id, user_id) VALUES (?, ?)",
            (1, 3)
            )
cur.execute("INSERT INTO cart (product_id, user_id) VALUES (?, ?)",
            (2, 3)
            )
cur.execute("INSERT INTO cart (product_id, user_id) VALUES (?, ?)",
            (3, 3)
            )

# pr = cur.execute("SELECT * from products")
# for each in pr:
#     print(each)

connection.commit()
connection.close()
