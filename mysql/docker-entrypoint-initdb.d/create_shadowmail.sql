CREATE TABLE virtual_alias (
  id int(11) NOT NULL AUTO_INCREMENT,
  alias_email varchar(100) NOT NULL,
  real_email varchar(100) NOT NULL,
  enabled tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (id),
  UNIQUE KEY alias_email (alias_email)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

