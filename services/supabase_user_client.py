import os

from dotenv import load_dotenv
from supabase import create_client


def get_supabase_for_user(jwt_token: str):
    """Supabase client scoped to the caller JWT (RLS enforced)."""
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    anon_key = os.getenv("SUPABASE_ANON_KEY")
    if not url or not anon_key:
        raise RuntimeError("SUPABASE_URL or SUPABASE_ANON_KEY missing")
    client = create_client(url, anon_key)
    client.postgrest.auth(jwt_token)
    return client
