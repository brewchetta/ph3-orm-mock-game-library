from lib import CONN, CURSOR
from lib.classes.player import Player

class Game:

    # MAGIC METHODS #

    def __init__(self, name, hours_played, player_id):
        self.id = id
        self.name = name
        self.hours_played = hours_played
        self.player_id = player_id

    def __repr__(self):
        return f"Game(id={self.id}, name={self.name}, hours_played={self.hours_played}, player_id={self.player_id})"

    # THIS METHOD WILL CREATE THE SQL TABLE #

    @classmethod
    def create_table(cls):
        sql="""CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY,
        name TEXT,
        hours_played INTEGER,
        player_id INTEGER
        )
        """

        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql="DROP TABLE games"
        CURSOR.execute(sql)

    # PROPERTIES #

    @property
    def hours_played(self):
        return self._hours_played

    @hours_played.setter
    def hours_played(self, value):
        if value > 0:
            self._hours_played = value
        else:
            raise ValueError('hours_played must be a number greater than zero')

    # SQL METHODS #

    def create(self):
        # insert instance into database
        sql="""INSERT INTO games (name, hours_played, player_id)
        VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, [self.name, self.hours_played, self.player_id])
        CONN.commit()

        self.id = CURSOR.lastrowid
        return self

    @classmethod
    def query_all(cls):
        sql="SELECT * FROM games"
        rows = CURSOR.execute(sql).fetchall()

        return [ Game(row[1], row[2], row[3], row[0]) for row in rows ]

    @classmethod
    def query_by_id(cls, id):
        sql="SELECT * FROM games WHERE id = ?"
        row = CURSOR.execute(sql, [id]).fetchone()
        if row:
            return Game(row[1], row[2], row[3], row[0])

    def delete(self):
        sql="""DELETE FROM games
        WHERE id = ?
        """

        CURSOR.execute(sql, [self.id] )
        CONN.commit()

        self.id = None

    # ASSOCATION PROPERTIES #

    @property
    def customer(self):
        sql="SELECT * FROM customers WHERE id = ?"
        row = CURSOR.execute(sql, [self.player_id]).fetchone()
        if row:
            return Customer(row[1], row[0])

    @customer.setter
    def customer(self, value):
        if isinstance(value, Customer):
            self.player_id = value.id
        else:
            raise ValueError("Customer must be of type Customer class")
