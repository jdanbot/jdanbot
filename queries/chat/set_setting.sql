-- name: set_setting(chat_id, key, value)^
update chat
set    settings = json_set(settings, :key, :value)
where  id = :chat_id;
