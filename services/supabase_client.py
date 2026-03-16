# services/supabase_client.py

from supabase import create_client
import os
from dotenv import load_dotenv

#load_dotenv()

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")


if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError("Variáveis SUPABASE_URL ou SUPABASE_ANON_KEY não definidas.")

# 🔓 Cliente padrão (respeita RLS)
supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# 👑 Cliente admin (ignora RLS)
supabase_admin = None
if SUPABASE_SERVICE_ROLE_KEY:
    supabase_admin = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)