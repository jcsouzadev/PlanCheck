from app import create_app
from models import db, User
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("Criando todas as tabelas...")
    db.create_all()
    print("Tabelas criadas com sucesso!")
    
    # Adicionar colunas que podem estar faltando (db.create_all não adiciona colunas em tabelas existentes)
    print("Verificando colunas adicionais...")
    try:
        db.session.execute(text("""
            ALTER TABLE empresa 
            ADD COLUMN IF NOT EXISTS cnpj VARCHAR(18),
            ADD COLUMN IF NOT EXISTS cep VARCHAR(10),
            ADD COLUMN IF NOT EXISTS cidade VARCHAR(100),
            ADD COLUMN IF NOT EXISTS pais VARCHAR(100) DEFAULT 'Brasil',
            ADD COLUMN IF NOT EXISTS logo_filename VARCHAR(255);
        """))
        
        db.session.execute(text("""
            ALTER TABLE ordem_execucao 
            ADD COLUMN IF NOT EXISTS tipo_ordem VARCHAR(50) DEFAULT 'programada',
            ADD COLUMN IF NOT EXISTS setor_id INTEGER,
            ADD COLUMN IF NOT EXISTS area_id INTEGER,
            ADD COLUMN IF NOT EXISTS equipamento_id INTEGER,
            ADD COLUMN IF NOT EXISTS servico_solicitado TEXT,
            ADD COLUMN IF NOT EXISTS tempo_previsto FLOAT,
            ADD COLUMN IF NOT EXISTS data_hora_inicio TIMESTAMP,
            ADD COLUMN IF NOT EXISTS data_hora_fim TIMESTAMP,
            ADD COLUMN IF NOT EXISTS servico_executado TEXT,
            ADD COLUMN IF NOT EXISTS diagnostico_falha TEXT;
        """))
        
        db.session.commit()
        print("Colunas adicionais verificadas/criadas com sucesso!")
    except Exception as e:
        print(f"Aviso ao verificar colunas: {e}")
        db.session.rollback()
    
    admin_exists = User.query.filter_by(username='admin').first()
    if not admin_exists:
        print("Criando usuário administrador...")
        admin = User(
            username='admin',
            nome='Administrador do Sistema',
            matricula='0001',
            funcao='Gestor de Manutenção',
            area='Administração',
            setor='TI',
            perfil_acesso='administrador'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        executante = User(
            username='executante',
            nome='João Silva',
            matricula='0002',
            funcao='Técnico de Manutenção',
            area='Operações',
            setor='Manutenção',
            perfil_acesso='executante'
        )
        executante.set_password('exec123')
        db.session.add(executante)
        
        db.session.commit()
        print("Usuários criados com sucesso!")
        print("Admin: username=admin, password=admin123")
        print("Executante: username=executante, password=exec123")
    else:
        print("Usuário administrador já existe.")
    
    print("Banco de dados inicializado com sucesso!")
