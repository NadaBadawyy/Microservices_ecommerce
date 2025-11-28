
CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY 'Nada@186';

GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce_system.* TO 'root'@'localhost';

FLUSH PRIVILEGES;

SELECT User, Host FROM mysql.user WHERE User = 'root';

SELECT 'Database user created successfully!' AS Status;
SELECT 'Username: root' AS Credentials;
SELECT 'Password: Nada@186' AS Password;
SELECT 'IMPORTANT: Change this password in production!' AS Warning;