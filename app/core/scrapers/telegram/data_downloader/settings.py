from pathlib import Path


BASE_PATH = Path(__file__).resolve().parent

# Telegram API Settings

# API version the client is using. Do not change unless you know what you are doing.
CLIENT_SYSTEM_VERSION = "4.16.30-vxCUSTOM"

# As Telegram can raise "429 Too Many Requests" error, we need to limit the number of
# concurrently processed dialogs. In case your download is too slow, you can try to
# increase this number.
CONCURRENT_DIALOG_DOWNLOADS=5

# Number of reactions to download per message.
REACTIONS_LIMIT_PER_MESSAGE=100

# Reaction fetching can sometimes fail due to Telegram API limitations.
# If download script still says about timeout, try to increase these values.
MESSAGE_REACTION_EXPONENTIAL_BACKOFF_SLEEP_TIME=5.0
MESSAGE_REACTION_EXPONENTIAL_BACKOFF_MAX_TRIES=5

# File export paths
DATA_FOLDER = Path("./data" or BASE_PATH / "data").resolve()

# https://core.telegram.org/api/takeout
# Options for the takeout method.
# For basic usage, should be left as is.
CLIENT_TAKEOUT_FINALIZE: bool = True

CLIENT_TAKEOUT_FETCH_CONTACTS: bool = False

CLIENT_TAKEOUT_FETCH_USERS: bool = False

CLIENT_TAKEOUT_FETCH_GROUPS: bool = True

CLIENT_TAKEOUT_FETCH_MEGAGROUPS: bool = True

CLIENT_TAKEOUT_FETCH_CHANNELS: bool = True

CLIENT_TAKEOUT_FETCH_FILES: bool = False

#
# # General running settings
#
# # Set to "DEBUG" in config file for detailed info on per-chat download progress.
# LOG_LEVEL = "INFO"
#
# # Message formatting for logging. Do not change unless you know what you are doing.
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "console": {
#             "level": LOG_LEVEL,
#             "class": "logging.StreamHandler",
#             "formatter": "default",
#         },
#     },
#     "formatters": {
#         "default": {
#             "format": "[%(asctime)s] |%(levelname)7s| %(filename)s:%(funcName)s():%(lineno)d: %(message)s",
#         },
#     },
#     "loggers": {
#         "data_downloader": {
#             "handlers": ["console"],
#             "level": LOG_LEVEL,
#             "propagate": False,
#         },
#         "asyncio": {
#             "level": "DEBUG",
#             "propagate": False,
#         },
#     },
# }
