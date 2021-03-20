from Common import logmngr

log = logmngr.get_logger()


def check_response_status(response):
    if response.status_code != 200:
        log.error("API Server: %s %s", str(
            response.status_code), response.text)
        raise RuntimeError('API Server error: ' +
                           str(response.status_code) + ": " + str(response.text))
