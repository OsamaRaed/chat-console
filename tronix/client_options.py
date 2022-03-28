from enum import Enum


class OPTION(Enum):
    LIST_ONLINE_USERS = '1'
    SEND_MESSAGE_TO_USER = '2'
    SEND_MESSAGE_TO_GROUP = '3'
    SELECT_USER_ID = '4'
    SELECT_GROUP_ID = '5'
    CLOSE_CONNECTION = '6'
