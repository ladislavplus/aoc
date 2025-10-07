import requests
from pathlib import Path
import browser_cookie3

def get_aoc_input(year: int, day: int) -> str:
    """Fetch Advent of Code input for a given year/day (caches locally)."""

    input_dir = Path("inputs")
    input_dir.mkdir(exist_ok=True)

    filename = input_dir / f"{year}_day{day:02d}.txt"
    if filename.exists():
        return filename.read_text().strip()

    try:
        session = Path(__file__).resolve().parent / "session.txt" # always the same folder as utils.py
        session_cookie = session.read_text().strip()
    except FileNotFoundError:
        raise RuntimeError("Missing session.txt with your AoC session cookie")

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    cookies = {"session": session_cookie}

    resp = requests.get(url, cookies=cookies)
    if resp.status_code != 200:
        raise RuntimeError(f"Error {resp.status_code}: {resp.text[:200]}")

    filename.write_text(resp.text.strip())
    return resp.text.strip()

""" def save_aoc_session(): # problematic on chrome/edge Windows, needs admin rights...
    # Try to read AoC cookie from your browser
    cj = browser_cookie3.load(domain_name="adventofcode.com")
    for cookie in cj:
        if cookie.name == "session":
            print(f"Found AoC session cookie in your browser: {cookie.value}")
            Path("session.txt").write_text(cookie.value)
            print("Session saved to session.txt")
            return
    raise RuntimeError("Could not find AoC session cookie") """

def print_aoc_session_on_firefox():
    """
    Print AoC session cookie from Firefox (for manual saving to session.txt).
    Works without admin rights, unlike Chrome/Edge. Just login to AoC in Firefox first.
    """
    cj = browser_cookie3.firefox(domain_name="adventofcode.com")
    for cookie in cj:
        if cookie.name == "session":
            print(cookie.value)


def print_utils_info():
    print("Utils module for Advent of Code")
    print("Functions:")
    print("- get_aoc_input(year, day): Fetch and cache AoC input for given year/day.")
    print("- print_aoc_session_on_firefox(): Print AoC session cookie from Firefox.")


if __name__ == "__main__":
    # print_aoc_session_on_firefox()
    # get_aoc_input(2021, 1)
    pass
