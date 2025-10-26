from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
login_manager = LoginManager()

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # ALTERADO: Mudança para db.Text para garantir que o hash de senha não seja truncado
    password_hash = db.Column(db.Text, nullable=False) 
    nome = db.Column(db.String(120))
    matricula = db.Column(db.String(50), unique=True)
    funcao = db.Column(db.String(50), default='executante')
    area = db.Column(db.String(100))
    setor = db.Column(db.String(100))
    # ALTERADO: Adicionado index=True para otimizar buscas por perfil (segurança/controle de acesso)
    perfil_acesso = db.Column(db.String(50), nullable=False, default='executante', index=True) 

    ordens_executadas = db.relationship('OrdemExecucao', backref='executante', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.perfil_acesso == 'administrador'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Empresa(db.Model):
    __tablename__ = 'empresa'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    setores = db.relationship('Setor', backref='empresa', cascade='all, delete-orphan', lazy=True)

class Setor(db.Model):
    __tablename__ = 'setor'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    # ALTERADO: Adicionado index=True
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False, index=True) 

    areas = db.relationship('Area', backref='setor', cascade='all, delete-orphan', lazy=True)

class Area(db.Model):
    __tablename__ = 'area'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    # ALTERADO: Adicionado index=True
    setor_id = db.Column(db.Integer, db.ForeignKey('setor.id'), nullable=False, index=True) 

    conjuntos = db.relationship('Conjunto', backref='area', cascade='all, delete-orphan', lazy=True)

class Conjunto(db.Model):
    __tablename__ = 'conjunto'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    # ALTERADO: Adicionado index=True
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False, index=True) 

    subconjuntos = db.relationship('Subconjunto', backref='conjunto', cascade='all, delete-orphan', lazy=True)

class Subconjunto(db.Model):
    __tablename__ = 'subconjunto'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    # ALTERADO: Adicionado index=True
    conjunto_id = db.Column(db.Integer, db.ForeignKey('conjunto.id'), nullable=False, index=True) 

    equipamentos = db.relationship('Equipamento', backref='subconjunto', cascade='all, delete-orphan', lazy=True)

class Equipamento(db.Model):
    __tablename__ = 'equipamento'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    codigo = db.Column(db.String(50))
    # ALTERADO: Adicionado index=True
    subconjunto_id = db.Column(db.Integer, db.ForeignKey('subconjunto.id'), nullable=False, index=True) 

    planos = db.relationship('PlanoInspecao', backref='equipamento', cascade='all, delete-orphan', lazy=True)

class PlanoInspecao(db.Model):
    __tablename__ = 'plano_inspecao'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    # ALTERADO: Adicionado index=True
    equipamento_id = db.Column(db.Integer, db.ForeignKey('equipamento.id'), nullable=False, index=True) 

    tipo_geracao = db.Column(db.String(50))
    frequencia = db.Column(db.Float)
    data_inicio = db.Column(db.DateTime)

    itens = db.relationship('ItemInspecao', backref='plano', cascade='all, delete-orphan', lazy=True)
    ordens = db.relationship('OrdemExecucao', backref='plano', cascade='all, delete-orphan', lazy=True)

class ItemInspecao(db.Model):
    __tablename__ = 'item_inspecao'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50))
    # Colunas de Medição (Template)
    valor_min = db.Column(db.Float)
    valor_max = db.Column(db.Float)

    # ALTERADO: Removidos os campos de 'resultado de execução' (falha, solucao, valor_atual, etc.) 
    # que pertencem ao ItemInspecaoApontado.

    # ALTERADO: Adicionado index=True
    plano_id = db.Column(db.Integer, db.ForeignKey('plano_inspecao.id'), nullable=False, index=True) 

class OrdemExecucao(db.Model):
    __tablename__ = 'ordem_execucao'
    id = db.Column(db.Integer, primary_key=True)
    # ALTERADO: Adicionado index=True
    plano_id = db.Column(db.Integer, db.ForeignKey('plano_inspecao.id'), nullable=False, index=True) 
    # ALTERADO: Adicionado index=True
    executante_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True) 
    data_programada = db.Column(db.DateTime, nullable=False)
    data_conclusao = db.Column(db.DateTime)
    # ALTERADO: Adicionado index=True para otimizar filtros de status (Pendente, Concluído, etc.)
    status = db.Column(db.String(50), default='pendente', index=True) 

    itens_apontados = db.relationship('ItemInspecaoApontado', backref='ordem', cascade='all, delete-orphan', lazy=True)

class ItemInspecaoApontado(db.Model):
    __tablename__ = 'item_inspecao_apontado'
    id = db.Column(db.Integer, primary_key=True)
    # ALTERADO: Adicionado index=True
    item_inspecao_id = db.Column(db.Integer, db.ForeignKey('item_inspecao.id'), nullable=False, index=True) 
    # ALTERADO: Adicionado index=True
    ordem_id = db.Column(db.Integer, db.ForeignKey('ordem_execucao.id'), nullable=False, index=True) 

    # Colunas de Resultado de Execução (Correto: pertencem a esta tabela)
    resultado = db.Column(db.String(50)) # Ex: 'OK', 'Não Conforme', Valor
    observacao = db.Column(db.Text)
    valor_atual = db.Column(db.Float)

    # Não Conformidades (Correto: pertencem a esta tabela)
    falha = db.Column(db.Text)
    solucao = db.Column(db.Text)
    tempo_necessario = db.Column(db.Float)
    qtde_executantes = db.Column(db.Integer)
    materiais = db.Column(db.Text)
    outros = db.Column(db.Text)

    item_inspecao = db.relationship('ItemInspecao', backref='apontamentos', lazy=True)