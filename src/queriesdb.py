#!/usr/bin/env python

import web
import __main__
from _mysql_exceptions import IntegrityError

class QueriesDB:
    """I/O class to database"""

    # init class vars
    dbhost = ""
    dbname = ""
    dbuser = ""
    dbpass = ""

    dbcon  = ""

    def __init__(self, dbhost, dbname, dbuser, dbpass):

        self.dbhost = dbhost
        self.dbname = dbname
        self.dbuser = dbuser
        self.dbpass = dbpass

        self.dbcon = web.database(dbn  = 'mysql',
                                  host = self.dbhost,
                                  db   = self.dbname,
                                  user = self.dbuser,
                                  pw   = self.dbpass)


    # Methods
    def addReport(self, report_data):
        """Introduces a new report with a map associated"""

        report_data = {'id_report': 00000000000000000001,
                       'img_url'  : "foo",
                       'table_csv': "table csv",
                       'column_name': "el nombre de la columna"}

        tablename = "map"
        id_map = None
        try:
            id_map = self.dbcon.insert(tablename,
                                   id_report = report_data['id_report'],
                                   image_url = report_data['img_url'],
                                   table_csv = report_data['table_csv'])
        except IntegrityError as ie:
            print ie

        return id_map

    def addMap(self, report, tags):
        """Introduces a new map in the database"""
        return 0


if __name__ == "__main__":

    import databasevalues

    q = QueriesDB(databasevalues.dbhost,
                  databasevalues.dbname,
                  databasevalues.dbuser,
                  databasevalues.dbpass)

    report_data = ""
    q.addReport(report_data)
