--name: get_by(id, title, username)^
--Get a user from the database using a named parameter
   INSERT INTO chats (id, title, username)
   VALUES (:id, :title, :username)
       ON CONFLICT (id)
       DO UPDATE
             SET title = excluded.title,
                 username = excluded.username
RETURNING *;

