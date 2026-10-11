import os
import requests

M3U_FILE = "playlists/roku_all.m3u"

def resolve_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        # First try HEAD request for speed
        response = requests.head(url, headers=headers, allow_redirects=True, timeout=10)
        if response.status_code == 200 and response.url:
            return response.url
        # Fallback to GET if HEAD fails or gets blocked
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        return response.url
    except Exception as e:
        print(f"Error resolving {url}: {e}")
        return url

def update_m3u():
    if not os.path.exists(M3U_FILE):
        print(f"File not found: {M3U_FILE}")
        return

    with open(M3U_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = []
    changed = False

    for line in lines:
        stripped = line.strip()
        # Check if line is a stream link (starts with http/https and is not an EXT tag)
        if stripped and not stripped.startswith("#") and stripped.startswith("http"):
            print(f"Resolving: {stripped}")
            new_url = resolve_url(stripped)
            if new_url != stripped:
                print(f"Updated: {stripped} -> {new_url}")
                changed = True
                updated_lines.append(new_url + "\n")
            else:
                updated_lines.append(line)
        else:
            updated_lines.append(line)

    if changed:
        with open(M3U_FILE, "w", encoding="utf-8") as f:
            f.writelines(updated_lines)
        print("M3U file updated successfully.")
    else:
        print("No link changes detected.")

if __name__ == "__main__":
    update_m3u()
