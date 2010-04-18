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
        """
        devuelve un diccionario con { id_tag1 = 'tagname1' , ... , id_tagn = 'tagnamen' }
        devuelve None si ha habido error o no hay tags asociadas
        """

        idtags_list   = []
        tagnames_list = []
        result = {}

        # Recupero los id_tags asociados a un mapa
        tablename = "tags_maps"
        sql_where = "id_map = " + str(id_mapa)
        try:
            idtags_list = self.dbcon.select(tablename,
                                            where = sql_where)

        except Exception as e:
            print e

        if len(idtags_list) < 1:
            return None

        # Recupero el el par id_tag | tagname
        sql_where = ""
        sql_where = sql_where + "id_tag = " + str(idtags_list[0]['id_tag'])
        for i in range(len(idtags_list)-1):
            sql_where = sql_where + " OR id_tag = " + str(idtags_list[i+1]['id_tag'])

        tablename = "tags"
        sql_what = "id_tag, tagname"
        try:
            tagnames_list = self.dbcon.select(tablename,
                                              what = sql_what,
                                              where = sql_where)

        except Exception as e:
            print e

        if len(tagnames_list) < 1:
            return None

        for i in range(len(tagnames_list)):
            aux = tagnames_list[i]
            key = aux['id_tag']
            value = aux['tagname']
            result[key] = value

        return result



    def getTitle(self, id_mapa):
        # select t2.title from map as t1, report as t2 where t1.id_map = '2' AND t1.id_report = t2.id_report;
        # devuelve un diccionario columna = resultado
        sql_what = "t2.title"
        sql_table = "map as t1, report as t2"
        sql_where = "t1.id_map = " + str(id_mapa) + " AND t1.id_report = t2.id_report;"
        title = None
        rs = None
        try:
            rs = self.dbcon.select(sql_table,
                                   what = sql_what,
                                   where = sql_where)
        except Exception as e:
            print e
            return title

        if len(rs) > 0:
            title = rs[0]['title']
            if len(title) <= 0:
                title = None

        return title


    def getResultsByTag(self, id_tag):
        """
        Devuelve un diccionario {id_map1 : map_name1, ..., id_mapn : map_namen}
        """
        # SELECT m.id_map, m.map_name FROM map as m, tags_maps as tm WHERE tm.id_tag = 15 AND tm.id_map = m.id_map;
        sql_what = "m.id_map, m.map_name"
        sql_tables = "map as m, tags_maps as tm"
        sql_where = "tm.id_tag = "+ str(id_tag) + " AND tm.id_map = m.id_map"

        rs = []
        result = {}
        try:
            rs = self.dbcon.select(sql_tables,
                                   what = sql_what,
                                   where = sql_where)
        except Exception as e:
            print e

        if len(rs) < 1:
            return None

        for i in range(len(rs)):
            aux = rs[i]
            key = aux['id_map']
            value = aux['map_name']
            result[key] = value

        return result






if __name__ == "__main__":

    from tests import db_config
    from tests import report_data, map_data, tags
    from tests import user

    q = QueriesDB(db_config)

    # INSERT TESTS
    # id_report = q.addReport(report_data)
    # print "Created report nro " + str(id_report)

    # id_map    = q.addMap(map_data, tags)
    # print "Created map nro " + str(id_map)

    # id_user   = q.addUser(user['nick'],
    #                       user['email'])
    # print "Created user nro " + str(id_user)

    # SELECT TESTS
    # id_map = 12345678901234567890123456789012
    # id_map = 12
    # tag_dict = q.getTags(id_map)
    # print str(tag_dict)

    # getTitleTest
    # t = q.getTitle(id_map)
    # print t


    # TEST FOR getResultsByTag
    # resultsByTag = q.getResultsByTag(4)
    # print str(resultsByTag)

