#!/usr/bin/env python

import web
import __main__

class QueriesDB:
    """I/O class to database"""

    # init class vars
    dbhost = ""
    dbname = ""
    dbuser = ""
    dbpass = ""

    dbcon  = ""

    last_id_map = 0

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
    def addReport(self, report_data, map_data, tags):
        id_report = self.addReportMetaInfo(report_data)
        id_map    = self.addMap(id_report, map_data, tags)
        return id_report

    def addReportMetaInfo(self, report_data):
        """Introduces the meta information associated to a new report"""

        tablename = "report"
        id_report = None
        try:
            id_report = self.dbcon.insert(tablename,
                                          title           = report_data['title'],
                                          description     = report_data['description'],
                                          units           = report_data['units'],
                                          region_analysis = report_data['region_analysis'],
                                          id_user         = report_data['id_user'],
                                          data_source     = report_data['data_source'],
                                          footnotes       = report_data['footnotes'],
                                          data_copyright  = report_data['data_copyright'])

        except Exception as e:
            print e

        return id_report

    def addMap(self, idx_report, map_data, tags):
        """Introduces a new map linked to a report"""

        tablename = "map"
        id_map = None
        img_url = str(self.last_id_map + 1) + ".png"
        self.last_id_map += 1
        try:
            id_map = self.dbcon.insert(tablename,
                                       id_report   = idx_report,
                                       image_url   = img_url,
                                       table_csv   = map_data['table_csv'],
                                       column_name = map_data['column_name'])

        except Exception as e:
            print e

        self.addTagsToMap(id_map, tags)
        return id_map

    def addTagsToMap(self, id_map, tags):
        for i in range(len(tags)):
            id_tag = self.addTag(tags[i])
            self.linkTagAndMap(id_map, id_tag)

        return 0

    def addTag(self, tag):

        tablename = "tags"
        id_tag = None
        try:
            id_tag = self.dbcon.insert(tablename,
                                       tagname   = tag)
        except Exception as e:
            print e

        return id_tag

    def linkTagAndMap(self, idx_map, idx_tag):

        tablename = "tags_maps"
        id = None
        try:
            id = self.dbcon.insert(tablename,
                                   id_map = idx_map,
                                   id_tag = idx_tag)
        except Exception as e:
            print e

        return id

    def addUser(self, usernick, useremail):
        tablename = "user"
        id_user = None
        try:
            id_user = self.dbcon.insert(tablename,
                                        nick  = usernick,
                                        email = useremail)
        except Exception as e:
            print e

        return id_user

if __name__ == "__main__":

    from tests import db_config
    from tests import report_data, map_data, tags
    from tests import user

    q = QueriesDB(db_config['dbhost'],
                  db_config['dbname'],
                  db_config['dbuser'],
                  db_config['dbpass'])

    id_report = q.addReport(report_data, map_data, tags)
    print "Created report nro " + str(id_report)

    id_map    = q.addMap(id_report, map_data, tags)
    print "Created map nro " + str(id_map)

    id_user   = q.addUser(user['nick'],
                          user['email'])
    print "Created user nro " + str(id_user)
