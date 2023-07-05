import sqlite3
from datetime import datetime as dt
import pandas as pd


class Database:

    def __init__(self):
        self.conn = sqlite3.connect("database.db")


    def insert_listings(self, df):
        df.to_sql(name="listings_new", con=self.conn, index=False, if_exists="replace")
        sql = """
            CREATE TABLE IF NOT EXISTS listings (
                listing TEXT,
                new TEXT,
                available TEXT,
                available_on TEXT,
                discovered_on TEXT
            );
            DROP TABLE IF EXISTS listings_temp;
            CREATE TABLE listings_temp AS
            SELECT
                new.listing,
                CASE
                    WHEN old.listing IS NULL THEN "TRUE"
                    ELSE "FALSE"
                END AS new,
                new.available,
                new.available_on,
                COALESCE(old.discovered_on, new.discovered_on) AS discovered_on
            FROM listings_new new
            LEFT JOIN listings old
            ON new.listing = old.listing;
            DROP TABLE IF EXISTS listings;
            CREATE TABLE listings AS
            SELECT
                *
            FROM listings_temp;
            DROP TABLE IF EXISTS listings_temp;
            DROP TABLE IF EXISTS listings_new;
        """
        cur = self.conn.cursor()
        cur.executescript(sql)


    def get_listings(self, query):
        return pd.read_sql(query, self.conn)
