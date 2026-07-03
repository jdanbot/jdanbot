-- name: get_top(chat_id, limit)
   select COUNT(e.id) as events_count,
          u.first_name,
          u.last_name,
          u.username
     from pidor_events e
left join pidors p
       on p.id = e.pidor_id
left join users u
       on u.id = p.user_id
    where e.chat_id = :chat_id
      and p.is_allowed = 1
 group by u.id
 order by events_count desc
    limit :limit;
