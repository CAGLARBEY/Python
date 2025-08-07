from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    print(f"Request: {flow.request.method} {flow.request.pretty_url}")
    print(f"Headers: {flow.request.headers}")
    print(f"Body: {flow.request.get_text()}")

def response(flow: http.HTTPFlow) -> None:
    print(f"Response: {flow.response.status_code} {flow.request.pretty_url}")
    print(f"Headers: {flow.response.headers}")
    print(f"Body: {flow.response.get_text()}")
