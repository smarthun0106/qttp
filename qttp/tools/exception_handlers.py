from qttp.tools.log import setup_custom_logger

logger = setup_custom_logger("Apis")

def exception_handler_01(func):
    def inner_function(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            done_message = (
                f"{args[0].api} - {args[0].market} - "
                f"{func.__name__.upper()} Method Execute Well"
            )
            logger.info(done_message)
            return result
        except (ccxt.NetworkError, ccxt.InsufficientFunds, IndexError) as e:
            error_message = (
                        f"{args[0].api}, {args[0].market}, "
                        f"{func.__name__.upper()}, {type(e).__name__}"
                    )
            logger.info(error_message)
    return inner_function
