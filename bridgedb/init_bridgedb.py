import sqlite3

# connect to database
conn = sqlite3.connect('bridge.db')

# create a cursor
c = conn.cursor()

# create a table
c.execute(""" CREATE TABLE bridge(
        pt_number text PRIMARY KEY UNIQUE,
        sta text,
        os_ptl real,
        span integer,
        beam integer,
        location integer,
        top_deck real,
        adj null,
        hundred real,
        eighty text,
        one real,
        bottom_defl real,
        x_slope real,
        fill real,
        field_shot real,
        x_slope_two real,
        l_r_c text
    )""")

# commit our command
conn.commit()

# close connection
conn.close()
