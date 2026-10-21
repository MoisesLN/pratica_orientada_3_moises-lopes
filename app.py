from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import select

from database import Base, SessionLocal, engine
from models import Book, User

Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.secret_key = "biblioteca"

@app.route("/")
def index():
    with SessionLocal() as session:
        usuarios = session.execute(select(User).order_by(User.nome)).scalars().all()
        livros = session.execute(select(Book).order_by(Book.titulo)).scalars().all()
        return render_template("index.html", usuarios=usuarios, livros=livros)

@app.route("/usuarios/novo", methods=["GET", "POST"])
@app.route("/usuario/novo", methods=["GET", "POST"])
def criar_usuario():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()

        if nome and email:
            with SessionLocal() as session:
                usuario_existente = session.execute(select(User).where(User.email == email)).scalar_one_or_none()
                if usuario_existente is None:
                    usuario = User(nome=nome, email=email)
                    session.add(usuario)
                    session.commit()
                    return redirect(url_for("listar_usuarios"))
        return render_template("user_form.html", erro="Dados inválidos ou usuário já cadastrado.")

    return render_template("user_form.html")

@app.route("/usuarios")
@app.route("/usuarios/listar")
def listar_usuarios():
    with SessionLocal() as session:
        usuarios = session.execute(select(User).order_by(User.nome)).scalars().all()
        livros = session.execute(select(Book).order_by(Book.titulo)).scalars().all()
        return render_template("index.html", usuarios=usuarios, livros=livros)

@app.route("/livros/novo", methods=["GET", "POST"])
def criar_livro():
    with SessionLocal() as session:
        usuarios = session.execute(select(User).order_by(User.nome)).scalars().all()

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        user_id = request.form.get("user_id")

        if titulo and user_id:
            with SessionLocal() as session:
                livro_existente = session.execute(select(Book).where(Book.titulo == titulo)).scalar_one_or_none()
                if livro_existente is None:
                    livro = Book(titulo=titulo, user_id=int(user_id))
                    session.add(livro)
                    session.commit()
                    return redirect(url_for("listar_livros"))
        return render_template("book_form.html", usuarios=usuarios, erro="Dados inválidos ou livro já cadastrado.")

    return render_template("book_form.html", usuarios=usuarios)

@app.route("/livros")
@app.route("/livros/listar")
def listar_livros():
    with SessionLocal() as session:
        usuarios = session.execute(select(User).order_by(User.nome)).scalars().all()
        livros = session.execute(select(Book).order_by(Book.titulo)).scalars().all()
        return render_template("index.html", usuarios=usuarios, livros=livros)

if __name__ == "__main__":
    app.run(debug=True)


