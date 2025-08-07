import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def fetch_url(session, url):
    """
    Fetches content from a URL asynchronously.

    Args:
        session (aiohttp.ClientSession): The HTTP session to use.
        url (str): The target URL.

    Returns:
        str: The content of the URL or an empty string in case of an error.
    """
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

async def scan_directory(url):
    """
    Scans a web directory asynchronously for hidden notes, usernames, passwords, or accessible files.

    Args:
        url (str): The base URL of the web directory to scan.

    Returns:
        dict: A dictionary containing found items and their details.
    """
    found_items = {
        "notes": [],
        "credentials": [],
        "accessible_files": []
    }

    async with aiohttp.ClientSession() as session:
        content = await fetch_url(session, url)
        if not content:
            return found_items

        soup = BeautifulSoup(content, 'html.parser')

        # Look for visible and hidden content
        for tag in soup.find_all(['a', 'p', 'div', 'span']):
            text = tag.get_text().strip()
            if 'note' in text.lower():
                found_items['notes'].append(text)
            if any(keyword in text.lower() for keyword in ['username', 'password', 'user', 'pass']):
                found_items['credentials'].append(text)

        # Look for accessible files
        tasks = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.endswith('/') or any(href.endswith(ext) for ext in ['.txt', '.log', '.json', '.xml']):
                full_url = url + href if not href.startswith("http") else href
                tasks.append(fetch_url(session, full_url))

        responses = await asyncio.gather(*tasks)
        for idx, response in enumerate(responses):
            if response:
                found_items['accessible_files'].append(tasks[idx]._coro.cr_frame.f_locals['url'])

    return found_items

async def main():
    print("--- Asynchronous Web Directory Scanner Tool ---")
    target_url = input("Enter the target URL (e.g., http://example.com/): ").strip()

    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        print("Invalid URL format. Make sure to include http:// or https://")
    else:
        results = await scan_directory(target_url)
        print("\n--- Scan Results ---")
        print("\n[Notes]")
        for note in results['notes']:
            print(f"- {note}")

        print("\n[Credentials]")
        for cred in results['credentials']:
            print(f"- {cred}")

        print("\n[Accessible Files]")
        for file in results['accessible_files']:
            print(f"- {file}")

if __name__ == "__main__":
    asyncio.run(main())