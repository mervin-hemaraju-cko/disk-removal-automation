###############################################################
############## All constants values resides here ##############
###############################################################

# VALUES
VALUE_URL_BASE_FRESH_SERVICE_TASKS = "{}/changes/{}/tasks"

# MESSAGE
MESSAGE_SNAPSHOT_CREATED = "The snapshot for {} has been created under {}"

# Descriptions
DESC_SNAPSHOT = "This is a snapshot for server {}"

# Exceptions
EXCEPTION_HTTP_ERROR_FRESHSERVICE = "An HTTP error occured while fetching tickets from FreshService"
EXCEPTION_NOT_FOUND_INSTANCE = "No instance found for the IP address {}"
EXCEPTION_TIMEOUT = "Request timeout occured: {}"
EXCEPTION_HTTP_ERROR = "HTTP error occured: {}"
EXCEPTION_GENERAL = "An unexpected error occurred: {}"
EXCEPTION_MESSAGE_ERROR_SLACK = "Message could not be posted to Slack channel"
EXCEPTION_OPTIONS_GENERAL = "{}. Use option -h for help"
EXCEPTION_OPTIONS_MISSING_ARGUMENTS = "Missing arguments"
EXCEPTION_OPTIONS_WRONG_ARGUMENTS = "Wrong arguments passed"
EXCEPTION_OPTIONS_HELP = "Options available: -t <ticket> -a <agent>"


def require_headers_template(api_key):
    return {"Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Basic {api_key}"}