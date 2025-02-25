# docker
# docker run -p 3306:3306 -e MYSQL_ROOT_PASSWORD=#### -e MYSQL_DATABASE=todos -d -v todos:/db --name todos my sql:8.0
# docker exec -it todos bash
# mysql -u root -p # enter mysql, -u: user / -p: password

# SHOW databases; # Show all databases in docker_ mysql
# USE todos; # Change databases to "todos"

# DDL, rule

CREATE TABLE todo(
    id INT NOT NULL AUTO_INCREMENT,
    contents VARCHAR(256) NOT NULL,
    is_done BOOLEAN NOT NULL,
    PRIMARY KEY (id)
);

# INSERT
INSERT INTO todo (contents, is_done) VALUES ("FastAPI Section 0", true);

# SHOW
SELECT * FROM todo;

