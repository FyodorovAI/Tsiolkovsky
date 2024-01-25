from pydantic import BaseModel, EmailStr
from supabase import  Client
from config.supabase import get_supabase

supabase: Client = get_supabase()

class User(BaseModel):
    email: EmailStr
    password

    def to_dict(self):
        return {
            'username': self.user.username,
            'email': self.user.email,
            'password': self.user.password
        }

    def sign_up(self, password: str):
        user = supabase.auth.sign_up({ "email": self.email, "password": password })
        print(f"Sign up: {user}")

    def authenticate(self, password: str):
        user = supabase.auth.sign_in_with_password({ "email": self.email, "password": password })
        print(f"Sign in: {user}")