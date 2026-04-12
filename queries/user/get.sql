-- name: get(id)^
-- Get a user from the database using a named parameter
select *
  from user
 where id = :id;
