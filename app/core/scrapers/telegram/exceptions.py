class InvalidDateRangeException(Exception):
    """
    Exception raised when the maximum date is earlier than or equal to the minimum date.
    """

class UninitializedTakeoutSessionException(Exception):
    """
    Exception raised when the `takeout` session is not initialized.
    """

