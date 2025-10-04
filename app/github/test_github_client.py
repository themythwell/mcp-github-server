import asyncio
import os

from app.github import GitHubClient


async def main():
    # Make sure GITHUB_TOKEN is exported in your shell: export GITHUB_TOKEN=xxxx
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ No GITHUB_TOKEN found in environment.")
        return

    gh = GitHubClient(token=token)
    try:
        repos = await gh.list_repos(per_page=5)
        print(f"✅ Retrieved {len(repos)} repos")
        for r in repos:
            print("-", r.get("full_name"))
    finally:
        await gh.aclose()


if __name__ == "__main__":
    asyncio.run(main())