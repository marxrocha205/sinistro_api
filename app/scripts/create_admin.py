from app.database.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password

db = SessionLocal()

admin = User(
    username="admin",
    senha_hash=hash_password("admin123"),
    perfil="ADMIN",
)

db.add(admin)
db.commit()

print("Usuário ADMIN criado com sucesso")