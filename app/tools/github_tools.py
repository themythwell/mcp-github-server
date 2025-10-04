from app.github import GitHubClient
from app.models.github import ListReposParams, Repo

async def list_repos(params: ListReposParams):
    gh = GitHubClient()
    try:
        data = await gh.list_repos(
            visibility=params.visibility,
            affiliation=params.affiliation,
        )
        return [Repo(**{k: d[k] for k in ("id", "name", "full_name", "private")}) for d in data]
    finally:
        await gh.aclose()
