# NUShackerz2021
1. Installed Packages:

# Activating Virtual Environment
- $ python3 -m venv venv
- $ . venv/bin/activate

# Inside the Virtual Environment
- $ pip3 install pymongo
- $ python3 -m pip install "pymongo[srv]"
- $ pip3 install pyTelegramBotAPI

# Documentation
1. handle_start
    - param[in] message : The message given by the user.
    - Used to handle the "/start" command.
    - If the Bot is started in a Telegram Group, 
        - Check whether there is a document with the group_id and group_name stored. If no, create one.
        - Proceed to request user to start the bot in private chat.


    - If the bot is started in a private chat,
        - Check whether the bot is started in any group. If no, redirect to Telegram Group.
        - Selects the group to be have the information to be posted inside

2. send_message_logic
    - param[in] chat_id : The id of the private chat.
    - param[in] group_name: The name of the group (*** Currently accepts 1 word. Fix it tomorrow)
    - param[in] user : The name of the user
    - Initialized after the user chooses which group he would like to post his information in.
    - Stores a dictionary of data.

# Database Schema
{
    "group_id" : XXX,
    "group_name": YYY,
    {
        "name": John,
        "preferences": ,
        "secret images": 
    },
    {
        "name": Dan,
        "preferences": ,
        "secret images": 
    }
}