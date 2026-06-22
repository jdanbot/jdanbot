-- name: set_setting(chat_id, key, value)^
update chats
set    settings = json_set(settings, :key, :value)
where  id = :chat_id;
