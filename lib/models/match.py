# lib/models/department.py
from models.__init__ import CURSOR, CONN


class Match:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, home, away, id=None):
        self.id = id
        self.home = home
        self.away = away

    def __repr__(self):
        return f"<Match{self.id}: home team: {self.home}, away team {self.away}>"

    @property
    def home(self):
        return self._home

    @home.setter
    def home(self, home):
        if isinstance(home, str) and len(home):
            self._home = home
        else:
            raise ValueError(
                "Home must be a non-empty string"
            )

    @property
    def away(self):
        return self._away

    @away.setter
    def away(self, away):
        if isinstance(away, str) and len(away):
            self._away = away
        else:
            raise ValueError(
                "Away must be a non-empty string"
            )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Match instances """
        sql = """
            CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY,
           home TEXT,
            away TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Match instances """
        sql = """
            DROP TABLE IF EXISTS matches;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the home and away values of the current Match instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO matches (home, away)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.home, self.away))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, home, away):
        """ Initialize a new Match instance and save the object to the database """
        match = cls(home, away)
        match.save()
        return match

    def update(self):
        """Update the table row corresponding to the current Match instance."""
        sql = """
            UPDATE matches
            SET home = ?, away = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.home, self.away, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Match instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM matches
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        """Return a Match object having the attribute values from the table row."""

        # Check the dictionary for an existing instance using the row's primary key
        match = cls.all.get(row[0])
        if match:
            # ensure attributes match row values in case local instance was modified
            match.home = row[1]
            match.away= row[2]
        else:
            # not in dictionary, create new instance and add to dictionary
            match = cls(row[1], row[2])
            match.id = row[0]
            cls.all[match.id] = match
        return match

    @classmethod
    def get_all(cls):
        """Return a list containing a Match object per row in the table"""
        sql = """
            SELECT *
            FROM matches
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return Match object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM matches
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_home(cls, home):
        """Return a Match object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM matches
            WHERE home is ?
        """

        row = CURSOR.execute(sql, (home,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def events(self):
        """Return list of events associated with current match"""
        from .event import Event
        sql = """
            SELECT * FROM events
            WHERE match_id = ?
        """
        CURSOR.execute(sql, (self.id,),)

        rows = CURSOR.fetchall()
        return [
            Event.instance_from_db(row) for row in rows
        ]