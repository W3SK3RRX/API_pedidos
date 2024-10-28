from database import engine
from schemas import Base

Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")