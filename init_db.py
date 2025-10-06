from app import create_app
from models import db, User

app = create_app()

with app.app_context():
    print("Criando todas as tabelas...")
    db.create_all()
    print("Tabelas criadas com sucesso!")
    
    admin_exists = User.query.filter_by(username='admin').first()
    if not admin_exists:
        print("Criando usuário administrador...")
        admin = User(username='admin', funcao='administrador')
        admin.set_password('admin123')
        db.session.add(admin)
        
        executante = User(username='executante', funcao='executante')
        executante.set_password('exec123')
        db.session.add(executante)
        
        db.session.commit()
        print("Usuários criados com sucesso!")
        print("Admin: username=admin, password=admin123")
        print("Executante: username=executante, password=exec123")
    else:
        print("Usuário administrador já existe.")
    
    print("Banco de dados inicializado com sucesso!")
