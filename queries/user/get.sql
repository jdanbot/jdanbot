-- name: get(id)^
-- Get a user from the database using a named parameter
select *
  from users
 where id =:id;
