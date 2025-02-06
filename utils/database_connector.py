#!/usr/bin/env python3

import sqlite3
import sys

sys.path.append('../')

class SQLiteConnection():
    def __init__(self, database : str):
        """
        @brief Connection Class to the Auction Database
        @param database name of database
        """
        self.connection = sqlite3.connect(database)
        self.cursor     = self.connection.cursor()


