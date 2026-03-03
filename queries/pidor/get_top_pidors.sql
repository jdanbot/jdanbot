-- name: get_top(chat_id, limit)
-- Get a user from the database using a named parameter
   select COUNT(e.id) as events_count,
          u.first_name,
          u.last_name,
          u.username
     from pidorevent e
left join pidor p
       on p.id = e.pidor_id
left join user u
       on u.id = p.user_id
    where e.chat_id = :chat_id
 group by u.id
    limit :limit;
