from lib.security.token import HTTPTokenHeader


token_security = HTTPTokenHeader(
    name="Authorization",
    scheme_name="JWT Token",
    description="Bearer Format: `Bearer xxxxxx.yyyyyyy.zzzzzz`",
    raise_error=True,
)