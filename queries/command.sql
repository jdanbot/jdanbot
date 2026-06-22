-- name: log_command(chat_id, user_id, name, args)!
insert into commands (chat_id, user_id, name, args)
     values (:chat_id, :user_id, :name, :args);
