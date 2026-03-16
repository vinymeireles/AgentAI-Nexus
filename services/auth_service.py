# services/auth_service.py

from services.supabase_client import supabase, supabase_admin

class AuthService:

    # -------------------------
    # CADASTRO
    # -------------------------
    @staticmethod
    def register_user(email: str, password: str):
        try:
            response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            if response.user is None:
                return False, "Erro ao criar usuário."

            return True, "Cadastro realizado. Aguarde aprovação do administrador."

        except Exception as e:
            return False, str(e)

    # -------------------------
    # LOGIN
    # -------------------------
    @staticmethod
    def login_user(email: str, password: str):
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
        except Exception:
            return False, "Credenciais inválidas."

        if response.user is None:
            return False, "Credenciais inválidas."

        # Buscar status na tabela users
        user_data = supabase.table("users") \
            .select("*") \
            .eq("id", response.user.id) \
            .execute()

        if not user_data.data:
            return False, "Usuário sem registro interno."

        if user_data.data[0]["status"] != "ativo":
            return False, "Aguardando aprovação do administrador."

        return True, user_data.data[0]
        

    # -------------------------
    # LOGOUT
    # -------------------------
    @staticmethod
    def logout():
        supabase.auth.sign_out()

    # -------------------------
    # APROVAR USUÁRIO
    # -------------------------
    @staticmethod
    def approve_user(user_id: str):
        if not supabase_admin:
            raise Exception("Supabase admin client não configurado.")

        response = supabase_admin.table("users") \
            .update({"status": "ativo"}) \
            .eq("id", user_id) \
            .execute()

        return response