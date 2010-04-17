USE `mapastematicosweb`;

DROP TABLE IF EXISTS map;
CREATE TABLE map(
       id_map INT(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
       id_report INT(20) NOT NULL,
       image_url VARCHAR(25) UNIQUE NOT NULL,
       table_csv VARCHAR(250) NOT NULL,
       column_name VARCHAR(250) NOT NULL,
       n_views INT DEFAULT 0,
       n_scores INT DEFAULT 0)
       ;
       -- CHARACTER SET utf8 COLLATE utf8_bin;

DROP TABLE IF EXISTS report;
CREATE TABLE report(
       id_report INT(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
       title VARCHAR(50) NOT NULL,
       description LONGTEXT,
       units VARCHAR(120),
       region_analysis CHAR(4) DEFAULT 'ccaa',
       id_user INT(20) DEFAULT 0,
       data_source VARCHAR(120),
       footnotes LONGTEXT,
       data_copyright VARCHAR(120))
       ;
       -- CHARACTER SET utf8 COLLATE utf8_bin;

DROP TABLE IF EXISTS tags;
CREATE TABLE tags(
       id_tag INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
       tagname VARCHAR(50),
       isvisible INT DEFAULT 1,
       n_views INT DEFAULT 0)
       ;
       -- CHARACTER SET utf8 COLLATE utf8_bin;

DROP TABLE IF EXISTS tags_maps;
CREATE TABLE tags_maps(
       id_tag INT(20) NOT NULL,
       id_map INT(20) NOT NULL,
       PRIMARY KEY(id_tag, id_map))
       ;
       -- CHARACTER SET utf8 COLLATE utf8_bin;

DROP TABLE IF EXISTS user;
CREATE TABLE user(
       id_user INT(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
       nick VARCHAR(20) NOT NULL,
       email VARCHAR(50) NOT NULL)
       ;
       -- CHARACTER SET utf8 COLLATE utf8_bin;
