# lib/models/event.py
from models.__init__ import CURSOR, CONN
from .match import Match


class Event:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, time, commentary, match_id, id=None):
        self.id = id
        self.time = time
        self.commentary = commentary
        self.match_id = match_id

    def __repr__(self):
        return (
            f"<Event {self.id}: {self.time}, {self.commentary}, " +
            f"Match ID: {self.match_id}>"
        )

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, time):
        if isinstance(time, str) and len(time):
            self._time = time
        else:
            raise ValueError(
                "Time must be a non-empty string"
            )

    @property
    def commentary(self):
        return self._commentary

    @commentary.setter
    def commentary(self, commentary):
        if isinstance(commentary, str) and len(commentary):
            self._commentary = commentary
        else:
            raise ValueError(
                "commentary must be a non-empty string"
            )

    @property
    def match_id(self):
        return self._match_id

    @match_id.setter
    def match_id(self, match_id):
        if type(match_id) is int and Match.find_by_id(match_id):
            self._match_id = match_id
        else:
            raise ValueError(
                "match_id must reference a match in the database")

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Event instances """
        sql = """
              CREATE TABLE IF NOT EXISTS events (
              id INTEGER PRIMARY KEY,
              time TEXT,
              commentary TEXT,
            match_id INTEGER,
            FOREIGN KEY (match_id) REFERENCES matches(match_id)
            )
            """

        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Event instances """
        sql = """
            DROP TABLE IF EXISTS events;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the time, commentary, and match id values of the current Event object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO events (time, commentary, match_id)
                VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, (self.time, self.commentary, self.match_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        """Update the table row corresponding to the current Event instance."""
        sql = """
            UPDATE events
            SET time = ?, commentary = ?, match_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.time, self.commentary,
                             self.match_id, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Event instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM events
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def create(cls, time, commentary, match_id):
        """ Initialize a new Event instance and save the object to the database """
        event = cls(time, commentary, match_id)
        event.save()
        return event

    @classmethod
    def instance_from_db(cls, row):
        """Return an Event object having the attribute values from the table row."""

        # Check the dictionary for  existing instance using the row's primary key
        event = cls.all.get(row[0])
        if event:
            # ensure attributes match row values in case local instance was modified
            event.time = row[1]
            event.commentary = row[2]
            event.match_id = row[3]
        else:
            # not in dictionary, create new instance and add to dictionary
             event  = cls(row[1], row[2], row[3])
             event .id = row[0]
             cls.all[event.id] = event 
        return  event 

    @classmethod
    def get_all(cls):
        """Return a list containing one Event object per table row"""
        sql = """
            SELECT *
            FROM events
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return Event object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM events
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_time(cls, time):
        """Return Event object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM events
            WHERE time is ?
        """

        row = CURSOR.execute(sql, (time,)).fetchone()
        return cls.instance_from_db(row) if row else None