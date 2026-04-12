-- name: get_by(id, first_name, last_name, username)^
-- Get a user from the database using a named parameter
insert into user(id, first_name, last_name, username)
     values (:id, :first_name, :last_name, :username)
on conflict (id)
do update set first_name = excluded.first_name,
              last_name = excluded.last_name,
              username = excluded.username
returning *;
