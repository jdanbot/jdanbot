-- name: get_note (chat_id, name)^
select name, text
  from note
 where chat_id = :chat_id and name = :name

-- name: get_notes (chat_id)
select name
  from note
 where chat_id = :chat_id
