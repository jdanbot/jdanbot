mute =
  test*{admin}* muted *{user}*

  🤔 *Reason:* {why}
  🕓 *Term:* {time}

  ⛓ *Unmute date:* {unban_time} MSK

selfmute =
  test*{admin}* selfmuted

  🤔 *Reason:* {why}
  🕓 *Term:* {time}

  ⛓ *Ummute date:* {unban_time} MSK

warn =
  test*{admin}* warned {i} time *{user}*

  🤔 *Reason:* {why}

unwarn =
  test*{admin}* unwarned {i} time *{user}*

  🤔 *Reason:* {why}

warn_limit_reached = got {i} warn
admin_cant_unwarn_self = Admin can't unwarn self
warns_not_found = No warns
reason_not_found = unknown
selfmute_limit_reached =  Banned selfmute for more than a week (10080 seconds)
