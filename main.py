import asyncio
import aiohttp
from bs4 import BeautifulSoup
import sys


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


URLS = [
    "https://www.python.org",
    "https://www.wikipedia.org",
    "https://www.github.com",
    "https://www.stackoverflow.com",
]


async def fetch_page(session, url):
    """Fetch the HTML content of a page."""
    async with session.get(url) as response:
        return await response.text()


async def scrape_title(html, url):
    """Parse the HTML and extract the title of the webpage."""
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string if soup.title else "No Title Found"
    print(f"Title for {bcolors.HEADER}{url}: {bcolors.OKGREEN}{title}{bcolors.ENDC}")


async def scrape_website(session, url):
    """Fetch the page and extract its title."""
    html = await fetch_page(session, url)
    await scrape_title(html, url)


async def main():
    """Main function to run the scraping concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_website(session, url) for url in URLS]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # set the event loop policy to avoid "event loop is closed" (Windows and Python 3.8+)
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
