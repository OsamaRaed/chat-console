from enum import Enum


class OPTION(Enum):
    LIST_ONLINE_USERS = '1'
    SEND_MESSAGE_TO_USER = '2'
    CREATE_GROUP = '3'
    JOIN_GROUP = '4'
    SEND_MESSAGE_TO_GROUP = '5'

    SELECT_USER_ID = '4'
    SELECT_GROUP_ID = '5'
    SHOW_MESSAGES = '6'
    CLOSE_CONNECTION = '7'

