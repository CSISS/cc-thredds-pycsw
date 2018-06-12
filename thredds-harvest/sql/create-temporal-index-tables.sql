CREATE TABLE `catalogs` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `parent_catalog_id` int(11) NOT NULL DEFAULT '1',
  `name` varchar(512) NOT NULL DEFAULT '',
  `url` varchar(512) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `datasets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `catalog_id` int(10) NOT NULL,
  `name` varchar(512) NOT NULL DEFAULT '''',
  `url_path` varchar(512) NOT NULL,
  `iso_url` varchar(512) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;