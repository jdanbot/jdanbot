--name: get(id)^
--Get a user from the database using a named parameter
SELECT *
  FROM chats
 WHERE id = :id;
