import httpx


def status_changed_notify(callback_url: str, callback_data):
    response = httpx.post(url=callback_url, data={'callback_data': callback_data})
    return response.status_code