# Discord self bot

Discord self bots have been banned & unsupported by the API for about 5 years, therefore do not expec this to be perfect, and please acknowledge the risks you are taking by running this program as it is against their user agreement. However, if you wish to run it - navigate to settings.py, input your token and start the program. You may make any changes to your config by editing settings.py :)

# Requirements
    "pip install discord"

# Commands
    ".pfp (OPTIONAL: USER): displays a user's profile picture, if not specified it'll send yours"
    ".clear (OPTIONAL: USER): deletes all of the messages in the current channel if the username is not specified, otherwise deletes the messages with the specified person (tries to find it using the username you've specified)"
    ".attachments (OPTIONAL: USER): deletes all of the attachments/images you've sent in the current channel if the username is not specified, works the same way as .clear"
    ".edit "TEXT" (OPTIONAL: USER): edits all of your messages in the current channel if the username is not specified, works the same way as .clear"
    ".clearfriends: deletes all of your messages with every single person you have added"
    ".kick (USER): kicks a user from the server (requires permissions)"
    ".ban (USER): bans a user from the server (requires permissions)"
    ".unban (ID): unbans a user from the server (requires permissions)"
    ".role (USER) (ROLE): add/remove a role from a user (requires permissions)"
