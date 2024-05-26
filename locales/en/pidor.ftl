pidor-top_10 = Top 10 *pidors* of all time:
pidor-members = All members — `{ $count }`

reg = You're not in the database\. Sign up via /pidorreg
in_db = Caught in the database, look for yourself in `jdanbot\.db`
already_in_db = Find youself in `jdanbot\.db`
work_only_in_chats = Pidor of the day only works in chats!
pidor_left = I found the pidor of the day, but it looks like he left from this chat (wow pidor!), So try again!

pidor-templates = { $prop -> 
  *[0] Today *pidor of day* is { $user }
  [1] { $user }, you're the *pidor of day*
  [2] You *pidor of day*, { $user } 🌚
}
templates-count = 3

pidor-templates-finden = { $prop ->
  *[0] Today *pidor of the day* has already been discovered, it is { $user }
  [1] You really don't remember who the *pidor of the day* is? Today it is { $user }
  [2] Remind, { $user } is *pidor of day*
}
pidor-templates-finden-count = 3

pidor-finding = { $prop ->
  *[0]
    The search for the pidor started...
    Nowhere to go 🌚
    The removal of the protection is successful!
    Pidor found... don't go anywhere!
  [1]
    You shouldn't have called that command...
    There's no going back!
  [2]
    Are you sure you want to know?
    I understand your impatience to find out...
    I think /donate would solve the problem 🌚
    \*Just kidding*
  [3]
    Running a pidor detection system
    ZeroDivisionError: division by zero
    Hm, jokes from the bot's author.
    Doesn't matter, because the faggot is found
}
pidor-finding-count = 4