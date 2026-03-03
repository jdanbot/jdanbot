-- name: get_by(id, title, username)^
-- Get a user from the database using a named parameter
insert into chat(id, title, username)
     values (:id, :title, :username)
on conflict (id) do update set 
            title = excluded.title,
            username = excluded.username
returning *;
