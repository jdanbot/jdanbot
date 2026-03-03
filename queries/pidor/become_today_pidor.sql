-- name: new_pidor_event(pidor_id, chat_id)$
-- Get a user from the database using a named parameter
insert into pidorevent(chat_id, pidor_id)
     values (:chat_id, :pidor_id)
  returning id;

-- name: update_latest_time(pidor_id, event_id)<!
update pidor
   set latest_time = :event_id
 where id = :pidor_id;

-- name: update_chat_pidor(chat_id, pidor_id)<!
update chat
   set pidor_id = :pidor_id
 where id = :chat_id;
