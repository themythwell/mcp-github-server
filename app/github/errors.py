class GitHubError(Exception):
    """Base for GitHub client errors."""
    pass

class Unauthorized(GitHubError):
    """Missing/invalid token or 401 from GitHub."""
    pass

class NotFound(GitHubError):
    """404 from GitHub or wrong resource type."""
    pass

class RateLimited(GitHubError):
    """Hit GitHub rate limit; header contains reset epoch."""
    def __init__(self, reset_epoch: str | None = None):
        super().__init__(f"Rate limited. Reset: {reset_epoch}")
        self.reset_epoch = reset_epoch
