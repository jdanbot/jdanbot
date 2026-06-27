-- name: get_note (chat_id, name)^
select name, text
  from notes
 where chat_id = :chat_id and name = :name;

-- name: get_notes (chat_id)
select name
  from notes
 where chat_id = :chat_id;

-- name: add_or_update(chat_id, name, text, author_id)$
insert into notes(chat_id, name, text, author_id)
     values (:chat_id, :name, :text, :author_id)
on conflict (chat_id, name)
         do
 update set text = :text,
            editor_id = :author_id,
            updated_at = unixepoch()
  returning _rowid_ = last_insert_rowid();
  
-- name: delete_note (chat_id, name)!
delete
  from notes
 where chat_id = :chat_id
   and name = :name;

