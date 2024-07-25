from __init__ import CURSOR, CONN

class Department:

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        """Create a new table to persist the attributes of Department instances."""
        sql = """
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT
        );
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the table that persists Department instances."""
        sql = "DROP TABLE IF EXISTS departments;"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """Insert or update a row with the current Department instance."""
        if self.id is None:
            sql = "INSERT INTO departments (name, location) VALUES (?, ?)"
            CURSOR.execute(sql, (self.name, self.location))
            self.id = CURSOR.lastrowid
        else:
            sql = "UPDATE departments SET name = ?, location = ? WHERE id = ?"
            CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    @classmethod
    def create(cls, name, location):
        """Initialize a new Department instance and save the object to the database."""
        department = cls(name, location)
        department.save()
        return department

    def update(self):
        """Update the table row corresponding to the current Department instance."""
        if self.id is None:
            raise ValueError("Can't update a department that doesn't exist in the database.")
        self.save()

    def delete(self):
        """Delete the table row corresponding to the current Department instance."""
        if self.id is None:
            raise ValueError("Can't delete a department that doesn't exist in the database.")
        sql = "DELETE FROM departments WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        affected_rows = CURSOR.rowcount
        if affected_rows == 0:
            raise ValueError(f"No department found with id {self.id}, or deletion failed.")
        CONN.commit()
        # Set the id to None to indicate that the object no longer corresponds to a database row
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        """Takes a database row and returns a corresponding Department instance."""
        id, name, location = row
        return cls(name, location, id)

    @classmethod
    def get_all(cls):
        """Return a list of Department instances for every row in the departments table."""
        sql = "SELECT * FROM departments"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return a Department instance corresponding to a row retrieved by its id."""
        sql = "SELECT * FROM departments WHERE id = ?"
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.instance_from_db(row)
        return None

    @classmethod
    def find_by_name(cls, name):
        """Return a Department instance corresponding to a row retrieved by its name."""
        sql = "SELECT * FROM departments WHERE name = ?"
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.instance_from_db(row)
        return None