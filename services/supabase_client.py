import os
from functools import lru_cache

from dotenv import load_dotenv
from supabase import create_client


@lru_cache(maxsize=1)
def get_supabase():
    load_dotenv()

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not url:
        raise RuntimeError("SUPABASE_URL missing")

    if not key:
        raise RuntimeError("SUPABASE_SERVICE_ROLE_KEY missing")

    return create_client(url, key)
