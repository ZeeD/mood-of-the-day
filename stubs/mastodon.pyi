class Mastodon:
    def __init__(
        self,
        *,
        client_id: str,
        client_secret: str,
        access_token: str,
        api_base_url: str,
    ) -> None: ...
    def toot(self, status: str) -> dict[str, object]: ...
