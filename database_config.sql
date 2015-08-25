CREATE TABLE `db_lrlr`.`user_details` (
  `user_id` BIGINT NULL AUTO_INCREMENT,
  `user_name` TEXT NULL,
  `user_email` TEXT NULL,
  `user_password` TEXT NULL,
  PRIMARY KEY (`user_id`));

-- Stored Procedure for Creating Users

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name TEXT,
    IN p_email TEXT,
    IN p_password TEXT
)
BEGIN
    if ( select exists (select 1 from user_details where user_username = p_username) ) THEN
     
        select 'Username Already Exists';
     
    ELSE
     
        insert into user_details
        (
            user_name,
            user_email,
            user_password
        )
        values
        (
            p_name,
            p_email,
            p_password
        );
     
    END IF;
END$$
DELIMITER ;

-- End of Stored Procedure for Creating Users

