from database import Base, SessionLocal, engine
from models import Book, User

Base.metadata.create_all(bind=engine)

with SessionLocal() as session:
    usuario = session.query(User).filter_by(email="maria@email.com").first()
    if usuario is None:
        usuario = User(nome="Maria", email="maria@email.com")
        session.add(usuario)
        session.commit()

    livro = session.query(Book).filter_by(titulo="Dom Casmurro").first()
    if livro is None:
        livro = Book(titulo="Dom Casmurro", user_id=usuario.id)
        session.add(livro)
        session.commit()

    print("Usuário:", usuario.nome)
    print("Livro:", livro.titulo)
    print("Relacionamento:", livro.user.nome)
