-- name: check_is_pidor(chat_id, user_id)$
SELECT EXISTS(
    SELECT 1 
    FROM pidors
    WHERE chat_id = :chat_id AND user_id = :user_id
);

-- name: get_or_create(chat_id, user_id)^
insert into pidors(chat_id, user_id)
     values (:chat_id, :user_id)
on conflict
  do update
        set chat_id = :chat_id
  returning id,
            chat_id,
            user_id,
            is_allowed,
            latest_time,
            _rowid_ = last_insert_rowid();

-- name: get_random_pidor(chat_id)^
  SELECT id, chat_id, user_id,
         is_allowed, latest_time
    FROM "pidors"
   WHERE "chat_id" = :chat_id
     AND "is_allowed" = 1
ORDER BY random() ASC
   LIMIT 1;

-- name: get_pidor_members_count(chat_id)$
SELECT COUNT(*)
FROM "pidors"
WHERE "chat_id" = :chat_id
AND "is_allowed" = 1;

