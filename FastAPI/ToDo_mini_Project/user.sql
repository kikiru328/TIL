# docker
# docker run -p 3306:3306 -e MYSQL_ROOT_PASSWORD=#### -e MYSQL_DATABASE=todos -d -v todos:/db --name todos my sql:8.0
# docker exec -it todos bash
# mysql -u root -p # enter mysql, -u: user / -p: password

# SHOW databases; # Show all databases in docker_ mysql

# DDL, rule

CREATE TABLE user(
     id INTEGER NOT NULL AUTO_INCREMENT,
     username VARCHAR(256) NOT NULL,
     password VARCHAR(256) NOT NULL,
     PRIMARY KEY (id)
);

# Connect todo - user
ALTER TABLE todo ADD COLUMN user_id INTEGER;

# Foreign Key
ALTER TABLE todo ADD FOREIGN KEY(user_id) REFERENCES user (id);

# insert
INSERT INTO user (username, password) VALUES ("admin", "password");

# mapping
UPDATE todo set user_id = 1 where id = 1;

# JOIN
SELECT * FROM todo t JOIN user u ON t.user_id = u.id;

