import sqlite3


class DatabaseManager:
    def __init__(self, db_name="lego_planner.db"):
        self.db_name = db_name

    def create_tables(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS storage_boxes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                box_number TEXT NOT NULL UNIQUE,
                label TEXT,
                notes TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lego_sets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                set_number TEXT,
                status TEXT,
                box_id INTEGER,
                missing_pieces TEXT,
                rebuild_progress INTEGER,
                notes TEXT,
                FOREIGN KEY (box_id) REFERENCES storage_boxes(id)
            )
        """)

        connection.commit()
        connection.close()

    def add_box(self, box_number, label="", notes=""):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO storage_boxes (box_number, label, notes)
            VALUES (?, ?, ?)
            """,
            (box_number, label, notes)
        )

        connection.commit()
        connection.close()

    def add_lego_set(
        self,
        name,
        set_number,
        status,
        box_id,
        missing_pieces,
        rebuild_progress,
        notes
    ):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO lego_sets (
                name,
                set_number,
                status,
                box_id,
                missing_pieces,
                rebuild_progress,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                set_number,
                status,
                box_id,
                missing_pieces,
                rebuild_progress,
                notes
            )
        )

        connection.commit()
        connection.close()

    def get_all_lego_sets(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                lego_sets.id,
                lego_sets.name,
                lego_sets.set_number,
                lego_sets.status,
                storage_boxes.box_number,
                lego_sets.missing_pieces,
                lego_sets.rebuild_progress,
                lego_sets.notes
            FROM lego_sets
            LEFT JOIN storage_boxes
                ON lego_sets.box_id = storage_boxes.id
            ORDER BY lego_sets.id DESC
        """)

        rows = cursor.fetchall()
        connection.close()

        return rows

    def get_lego_set_by_id(self, set_id):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                lego_sets.id,
                lego_sets.name,
                lego_sets.set_number,
                lego_sets.status,
                storage_boxes.box_number,
                lego_sets.missing_pieces,
                lego_sets.rebuild_progress,
                lego_sets.notes
            FROM lego_sets
            LEFT JOIN storage_boxes
                ON lego_sets.box_id = storage_boxes.id
            WHERE lego_sets.id = ?
            """,
            (set_id,)
        )

        row = cursor.fetchone()
        connection.close()

        return row

    def update_lego_set(
        self,
        set_id,
        name,
        set_number,
        status,
        box_id,
        missing_pieces,
        rebuild_progress,
        notes
    ):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE lego_sets
            SET
                name = ?,
                set_number = ?,
                status = ?,
                box_id = ?,
                missing_pieces = ?,
                rebuild_progress = ?,
                notes = ?
            WHERE id = ?
            """,
            (
                name,
                set_number,
                status,
                box_id,
                missing_pieces,
                rebuild_progress,
                notes,
                set_id
            )
        )

        connection.commit()
        connection.close()

    def delete_lego_set(self, set_id):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM lego_sets WHERE id = ?",
            (set_id,)
        )

        connection.commit()
        connection.close()

    def get_all_boxes(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, box_number, label
            FROM storage_boxes
            ORDER BY box_number
        """)

        rows = cursor.fetchall()
        connection.close()

        return rows

    def get_or_create_box(self, box_number):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM storage_boxes WHERE box_number = ?",
            (box_number,)
        )

        row = cursor.fetchone()

        if row:
            box_id = row[0]
        else:
            cursor.execute(
                """
                INSERT INTO storage_boxes (box_number, label, notes)
                VALUES (?, ?, ?)
                """,
                (box_number, "", "")
            )
            connection.commit()
            box_id = cursor.lastrowid

        connection.close()

        return box_id