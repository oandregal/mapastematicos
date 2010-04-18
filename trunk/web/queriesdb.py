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

    def __init__(self, db_config):

        self.dbhost = db_config['dbhost']
        self.dbname = db_config['dbname']
        self.dbuser = db_config['dbuser']
        self.dbpass = db_config['dbpass']

        self.dbcon = web.database(dbn  = 'mysql',
                                  host = self.dbhost,
                                  db   = self.dbname,
                                  user = self.dbuser,
                                  pw   = self.dbpass)


    # Methods
    def addReport(self, report_data):
        """Introduces the meta information associated to a new report"""

        tablename = "report"
        id_report = None
        try:
            id_report = self.dbcon.insert(tablename,
                                          id_report       = report_data['id_report'],
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

    def addMap(self, map_data, tags):
        """Introduces a new map linked to a report"""

        tablename = "map"
        try:
            id = self.dbcon.insert(tablename,
                                   id_map    = map_data['id_map'],
                                   id_report = map_data['id_report'],
                                   image     = map_data['id_map'] + ".png",
                                   stats     = map_data['id_map'] + "_stats" + ".png",
                                   map_name  = map_data['map_name'])

        except Exception as e:
            print e

        self.addTagsToMap(map_data['id_map'], tags)
        return map_data['id_map']

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

    def getTags(self, id_mapa):

        idtags_list   = []
        tagnames_list = []

        tablename = "tags_maps"
        sql_where = "id_map = " + str(id_mapa)
        try:
            idtags_list = self.dbcon.select(tablename,
                                            where = sql_where)

        except Exception as e:
            print e

        sql_where = ""
        sql_where = sql_where + "id_tag = " + str(idtags_list[0]['id_tag'])
        if len(idtags_list) > 0:
            for i in range(len(idtags_list)-1):
                sql_where = sql_where + " OR id_tag = " + str(idtags_list[i+1]['id_tag'])

        tablename = "tags"
        try:
            tagnames_list = self.dbcon.select(tablename,
                                              where = sql_where)

        except Exception as e:
            print e

        aux = []
        for i in range(len(tagnames_list)):
            aux.append(tagnames_list[i]['tagname'])

        return aux


if __name__ == "__main__":

    from tests import db_config
    from tests import report_data, map_data, tags
    from tests import user

    q = QueriesDB(db_config)

    #INSERT TESTS
    id_report = q.addReport(report_data)
    print "Created report nro " + str(id_report)

    id_map    = q.addMap(map_data, tags)
    print "Created map nro " + str(id_map)

    id_user   = q.addUser(user['nick'],
                          user['email'])
    print "Created user nro " + str(id_user)

    #SELECT TESTS
    tag_list = q.getTags(id_map)
    print tag_list

