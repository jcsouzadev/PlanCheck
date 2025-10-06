from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Empresa, Setor, Area, Conjunto, Subconjunto, Equipamento, PlanoInspecao, ItemInspecao, OrdemExecucao, ItemInspecaoApontado
from utils import gerar_pdf, gerar_excel
from datetime import datetime
import pandas as pd
from functools import wraps

main_bp = Blueprint('main', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Acesso negado. Apenas administradores podem acessar esta página.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        total_empresas = Empresa.query.count()
        total_planos = PlanoInspecao.query.count()
        total_ordens = OrdemExecucao.query.count()
        ordens_pendentes = OrdemExecucao.query.filter_by(status='pendente').count()
        
        return render_template('index.html', 
                             total_empresas=total_empresas,
                             total_planos=total_planos,
                             total_ordens=total_ordens,
                             ordens_pendentes=ordens_pendentes)
    return redirect(url_for('main.login'))

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'Bem-vindo, {user.username}!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Usuário ou senha inválidos', 'danger')
    
    return render_template('login.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu do sistema', 'info')
    return redirect(url_for('main.login'))

@main_bp.route('/empresas', methods=['GET', 'POST'])
@login_required
@admin_required
def empresas():
    if request.method == 'POST':
        nome = request.form.get('nome')
        if nome:
            empresa = Empresa(nome=nome)
            db.session.add(empresa)
            db.session.commit()
            flash('Empresa criada com sucesso!', 'success')
        return redirect(url_for('main.empresas'))
    
    empresas = Empresa.query.order_by(Empresa.nome).all()
    return render_template('empresas.html', empresas=empresas)

@main_bp.route('/empresas/<int:empresa_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_empresa(empresa_id):
    empresa = Empresa.query.get_or_404(empresa_id)
    if request.method == 'POST':
        nome = request.form.get('nome')
        if nome:
            empresa.nome = nome
            db.session.commit()
            flash('Empresa atualizada com sucesso!', 'success')
            return redirect(url_for('main.empresas'))
    return render_template('editar_empresa.html', empresa=empresa)

@main_bp.route('/empresas/<int:empresa_id>/delete', methods=['POST'])
@login_required
@admin_required
def deletar_empresa(empresa_id):
    empresa = Empresa.query.get_or_404(empresa_id)
    db.session.delete(empresa)
    db.session.commit()
    flash('Empresa excluída com sucesso!', 'success')
    return redirect(url_for('main.empresas'))

@main_bp.route('/empresas/<int:empresa_id>/setor', methods=['POST'])
@login_required
@admin_required
def adicionar_setor(empresa_id):
    empresa = Empresa.query.get_or_404(empresa_id)
    nome = request.form.get('nome')
    if nome:
        setor = Setor(nome=nome, empresa_id=empresa.id)
        db.session.add(setor)
        db.session.commit()
        flash('Setor adicionado com sucesso!', 'success')
    return redirect(url_for('main.ver_empresa', empresa_id=empresa_id))

@main_bp.route('/empresas/<int:empresa_id>')
@login_required
def ver_empresa(empresa_id):
    empresa = Empresa.query.get_or_404(empresa_id)
    return render_template('ver_empresa.html', empresa=empresa)

@main_bp.route('/setores/<int:setor_id>/editar', methods=['POST'])
@login_required
@admin_required
def editar_setor(setor_id):
    setor = Setor.query.get_or_404(setor_id)
    nome = request.form.get('nome')
    if nome:
        setor.nome = nome
        db.session.commit()
        flash('Setor atualizado com sucesso!', 'success')
    return redirect(url_for('main.ver_empresa', empresa_id=setor.empresa_id))

@main_bp.route('/setores/<int:setor_id>/delete', methods=['POST'])
@login_required
@admin_required
def deletar_setor(setor_id):
    setor = Setor.query.get_or_404(setor_id)
    empresa_id = setor.empresa_id
    db.session.delete(setor)
    db.session.commit()
    flash('Setor excluído com sucesso!', 'success')
    return redirect(url_for('main.ver_empresa', empresa_id=empresa_id))

@main_bp.route('/setores/<int:setor_id>/area', methods=['POST'])
@login_required
@admin_required
def adicionar_area(setor_id):
    setor = Setor.query.get_or_404(setor_id)
    nome = request.form.get('nome')
    if nome:
        area = Area(nome=nome, setor_id=setor.id)
        db.session.add(area)
        db.session.commit()
        flash('Área adicionada com sucesso!', 'success')
    return redirect(url_for('main.ver_empresa', empresa_id=setor.empresa_id))

@main_bp.route('/areas/<int:area_id>/editar', methods=['POST'])
@login_required
@admin_required
def editar_area(area_id):
    area = Area.query.get_or_404(area_id)
    nome = request.form.get('nome')
    if nome:
        area.nome = nome
        db.session.commit()
        flash('Área atualizada com sucesso!', 'success')
    return redirect(url_for('main.ver_empresa', empresa_id=area.setor.empresa_id))

@main_bp.route('/areas/<int:area_id>/delete', methods=['POST'])
@login_required
@admin_required
def deletar_area(area_id):
    area = Area.query.get_or_404(area_id)
    empresa_id = area.setor.empresa_id
    db.session.delete(area)
    db.session.commit()
    flash('Área excluída com sucesso!', 'success')
    return redirect(url_for('main.ver_empresa', empresa_id=empresa_id))

@main_bp.route('/areas/<int:area_id>/conjunto', methods=['POST'])
@login_required
@admin_required
def adicionar_conjunto(area_id):
    area = Area.query.get_or_404(area_id)
    nome = request.form.get('nome')
    if nome:
        conjunto = Conjunto(nome=nome, area_id=area.id)
        db.session.add(conjunto)
        db.session.commit()
        flash('Conjunto adicionado com sucesso!', 'success')
    return redirect(url_for('main.ver_empresa', empresa_id=area.setor.empresa_id))

@main_bp.route('/conjuntos/<int:conjunto_id>/editar', methods=['POST'])
@login_required
@admin_required
def editar_conjunto(conjunto_id):
    conjunto = Conjunto.query.get_or_404(conjunto_id)
    nome = request.form.get('nome')
    if nome:
        conjunto.nome = nome
        db.session.commit()
        flash('Conjunto atualizado com sucesso!', 'success')
    return redirect(url_for('main.ver_empresa', empresa_id=conjunto.area.setor.empresa_id))

@main_bp.route('/conjuntos/<int:conjunto_id>/delete', methods=['POST'])
@login_required
@admin_required
def deletar_conjunto(conjunto_id):
    conjunto = Conjunto.query.get_or_404(conjunto_id)
    empresa_id = conjunto.area.setor.empresa_id
    db.session.delete(conjunto)
    db.session.commit()
    flash('Conjunto excluído com sucesso!', 'success')
    return redirect(url_for('main.ver_empresa', empresa_id=empresa_id))

@main_bp.route('/conjuntos/<int:conjunto_id>/subconjunto', methods=['POST'])
@login_required
@admin_required
def adicionar_subconjunto(conjunto_id):
    conjunto = Conjunto.query.get_or_404(conjunto_id)
    nome = request.form.get('nome')
    if nome:
        subconjunto = Subconjunto(nome=nome, conjunto_id=conjunto.id)
        db.session.add(subconjunto)
        db.session.commit()
        flash('Subconjunto adicionado com sucesso!', 'success')
    return redirect(url_for('main.ver_empresa', empresa_id=conjunto.area.setor.empresa_id))

@main_bp.route('/subconjuntos/<int:subconjunto_id>/editar', methods=['POST'])
@login_required
@admin_required
def editar_subconjunto(subconjunto_id):
    subconjunto = Subconjunto.query.get_or_404(subconjunto_id)
    nome = request.form.get('nome')
    if nome:
        subconjunto.nome = nome
        db.session.commit()
        flash('Subconjunto atualizado com sucesso!', 'success')
    return redirect(url_for('main.ver_empresa', empresa_id=subconjunto.conjunto.area.setor.empresa_id))

@main_bp.route('/subconjuntos/<int:subconjunto_id>/delete', methods=['POST'])
@login_required
@admin_required
def deletar_subconjunto(subconjunto_id):
    subconjunto = Subconjunto.query.get_or_404(subconjunto_id)
    empresa_id = subconjunto.conjunto.area.setor.empresa_id
    db.session.delete(subconjunto)
    db.session.commit()
    flash('Subconjunto excluído com sucesso!', 'success')
    return redirect(url_for('main.ver_empresa', empresa_id=empresa_id))

@main_bp.route('/subconjuntos/<int:subconjunto_id>/equipamento', methods=['POST'])
@login_required
@admin_required
def adicionar_equipamento(subconjunto_id):
    subconjunto = Subconjunto.query.get_or_404(subconjunto_id)
    nome = request.form.get('nome')
    codigo = request.form.get('codigo')
    if nome:
        equipamento = Equipamento(nome=nome, codigo=codigo, subconjunto_id=subconjunto.id)
        db.session.add(equipamento)
        db.session.commit()
        flash('Equipamento adicionado com sucesso!', 'success')
    return redirect(url_for('main.ver_empresa', empresa_id=subconjunto.conjunto.area.setor.empresa_id))

@main_bp.route('/equipamentos/<int:equipamento_id>/editar', methods=['POST'])
@login_required
@admin_required
def editar_equipamento(equipamento_id):
    equipamento = Equipamento.query.get_or_404(equipamento_id)
    nome = request.form.get('nome')
    codigo = request.form.get('codigo')
    if nome:
        equipamento.nome = nome
        equipamento.codigo = codigo
        db.session.commit()
        flash('Equipamento atualizado com sucesso!', 'success')
    return redirect(url_for('main.ver_empresa', empresa_id=equipamento.subconjunto.conjunto.area.setor.empresa_id))

@main_bp.route('/equipamentos/<int:equipamento_id>/delete', methods=['POST'])
@login_required
@admin_required
def deletar_equipamento(equipamento_id):
    equipamento = Equipamento.query.get_or_404(equipamento_id)
    empresa_id = equipamento.subconjunto.conjunto.area.setor.empresa_id
    db.session.delete(equipamento)
    db.session.commit()
    flash('Equipamento excluído com sucesso!', 'success')
    return redirect(url_for('main.ver_empresa', empresa_id=empresa_id))

@main_bp.route('/planos', methods=['GET', 'POST'])
@login_required
@admin_required
def planos():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        equipamento_id = request.form.get('equipamento_id')
        tipo_geracao = request.form.get('tipo_geracao')
        frequencia = request.form.get('frequencia')
        data_inicio_str = request.form.get('data_inicio')
        
        if titulo and equipamento_id:
            plano = PlanoInspecao(
                titulo=titulo,
                equipamento_id=equipamento_id,
                tipo_geracao=tipo_geracao,
                frequencia=float(frequencia) if frequencia else None,
                data_inicio=datetime.strptime(data_inicio_str, '%Y-%m-%d') if data_inicio_str else None
            )
            db.session.add(plano)
            db.session.commit()
            flash('Plano criado com sucesso!', 'success')
            return redirect(url_for('main.editar_plano', plano_id=plano.id))
    
    planos = PlanoInspecao.query.order_by(PlanoInspecao.data_criacao.desc()).all()
    equipamentos = Equipamento.query.order_by(Equipamento.nome).all()
    return render_template('planos.html', planos=planos, equipamentos=equipamentos)

@main_bp.route('/planos/<int:plano_id>')
@login_required
def ver_plano(plano_id):
    plano = PlanoInspecao.query.get_or_404(plano_id)
    return render_template('ver_plano.html', plano=plano)

@main_bp.route('/planos/<int:plano_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_plano(plano_id):
    plano = PlanoInspecao.query.get_or_404(plano_id)
    
    if request.method == 'POST':
        if 'adicionar_item' in request.form:
            descricao = request.form.get('descricao')
            tipo = request.form.get('tipo')
            
            if descricao:
                item = ItemInspecao(
                    descricao=descricao,
                    tipo=tipo,
                    plano_id=plano.id
                )
                db.session.add(item)
                db.session.commit()
                flash('Item adicionado com sucesso!', 'success')
        
        return redirect(url_for('main.editar_plano', plano_id=plano_id))
    
    return render_template('editar_plano.html', plano=plano)

@main_bp.route('/planos/<int:plano_id>/delete', methods=['POST'])
@login_required
@admin_required
def deletar_plano(plano_id):
    plano = PlanoInspecao.query.get_or_404(plano_id)
    db.session.delete(plano)
    db.session.commit()
    flash('Plano excluído com sucesso!', 'success')
    return redirect(url_for('main.planos'))

@main_bp.route('/itens/<int:item_id>/delete', methods=['POST'])
@login_required
@admin_required
def deletar_item(item_id):
    item = ItemInspecao.query.get_or_404(item_id)
    plano_id = item.plano_id
    db.session.delete(item)
    db.session.commit()
    flash('Item excluído com sucesso!', 'success')
    return redirect(url_for('main.editar_plano', plano_id=plano_id))

@main_bp.route('/ordens', methods=['GET', 'POST'])
@login_required
def ordens():
    if request.method == 'POST' and current_user.is_admin():
        plano_id = request.form.get('plano_id')
        executante_id = request.form.get('executante_id')
        data_programada_str = request.form.get('data_programada')
        
        if plano_id and executante_id and data_programada_str:
            ordem = OrdemExecucao(
                plano_id=plano_id,
                executante_id=executante_id,
                data_programada=datetime.strptime(data_programada_str, '%Y-%m-%d')
            )
            db.session.add(ordem)
            db.session.commit()
            flash('Ordem de execução criada com sucesso!', 'success')
        return redirect(url_for('main.ordens'))
    
    if current_user.is_admin():
        ordens = OrdemExecucao.query.order_by(OrdemExecucao.data_programada.desc()).all()
    else:
        ordens = OrdemExecucao.query.filter_by(executante_id=current_user.id).order_by(OrdemExecucao.data_programada.desc()).all()
    
    planos = PlanoInspecao.query.all()
    executantes = User.query.all()
    return render_template('ordens.html', ordens=ordens, planos=planos, executantes=executantes)

@main_bp.route('/ordens/<int:ordem_id>')
@login_required
def ver_ordem(ordem_id):
    ordem = OrdemExecucao.query.get_or_404(ordem_id)
    
    if not current_user.is_admin() and ordem.executante_id != current_user.id:
        flash('Você não tem permissão para visualizar esta ordem', 'danger')
        return redirect(url_for('main.ordens'))
    
    return render_template('ver_ordem.html', ordem=ordem)

@main_bp.route('/ordens/<int:ordem_id>/executar', methods=['GET', 'POST'])
@login_required
def executar_ordem(ordem_id):
    ordem = OrdemExecucao.query.get_or_404(ordem_id)
    
    if not current_user.is_admin() and ordem.executante_id != current_user.id:
        flash('Você não tem permissão para executar esta ordem', 'danger')
        return redirect(url_for('main.ordens'))
    
    if request.method == 'POST':
        ordem.status = 'em_andamento'
        
        for item in ordem.plano.itens:
            resultado = request.form.get(f'resultado_{item.id}')
            observacao = request.form.get(f'observacao_{item.id}')
            valor_atual = request.form.get(f'valor_atual_{item.id}')
            
            item_apontado = ItemInspecaoApontado.query.filter_by(
                ordem_id=ordem.id,
                item_inspecao_id=item.id
            ).first()
            
            if not item_apontado:
                item_apontado = ItemInspecaoApontado(
                    ordem_id=ordem.id,
                    item_inspecao_id=item.id
                )
                db.session.add(item_apontado)
            
            item_apontado.resultado = resultado
            item_apontado.observacao = observacao
            item_apontado.valor_atual = float(valor_atual) if valor_atual else None
            
            if resultado == 'nao_conforme':
                item_apontado.falha = request.form.get(f'falha_{item.id}')
                item_apontado.solucao = request.form.get(f'solucao_{item.id}')
                tempo = request.form.get(f'tempo_{item.id}')
                qtde = request.form.get(f'qtde_{item.id}')
                item_apontado.tempo_necessario = float(tempo) if tempo else None
                item_apontado.qtde_executantes = int(qtde) if qtde else None
                item_apontado.materiais = request.form.get(f'materiais_{item.id}')
                item_apontado.outros = request.form.get(f'outros_{item.id}')
        
        if 'finalizar' in request.form:
            ordem.status = 'concluida'
            ordem.data_conclusao = datetime.utcnow()
            flash('Ordem finalizada com sucesso!', 'success')
        else:
            flash('Progresso salvo!', 'success')
        
        db.session.commit()
        return redirect(url_for('main.ver_ordem', ordem_id=ordem.id))
    
    return render_template('executar_ordem.html', ordem=ordem)

@main_bp.route('/relatorios/planos/<int:plano_id>/pdf')
@login_required
def relatorio_plano_pdf(plano_id):
    plano = PlanoInspecao.query.get_or_404(plano_id)
    return gerar_pdf('relatorio_plano.html', plano=plano)

@main_bp.route('/relatorios/planos/<int:plano_id>/excel')
@login_required
def relatorio_plano_excel(plano_id):
    plano = PlanoInspecao.query.get_or_404(plano_id)
    data = []
    
    for item in plano.itens:
        data.append({
            'Descrição': item.descricao,
            'Tipo': item.tipo or '-',
            'Valor Mínimo': item.valor_min or '-',
            'Valor Máximo': item.valor_max or '-'
        })
    
    df = pd.DataFrame(data)
    return gerar_excel(df, filename=f'plano_{plano_id}_{plano.titulo}.xlsx')

@main_bp.route('/api/dashboard/stats')
@login_required
def dashboard_stats():
    total_ordens = OrdemExecucao.query.count()
    ordens_pendentes = OrdemExecucao.query.filter_by(status='pendente').count()
    ordens_em_andamento = OrdemExecucao.query.filter_by(status='em_andamento').count()
    ordens_concluidas = OrdemExecucao.query.filter_by(status='concluida').count()
    
    total_itens = 0
    itens_conformes = 0
    itens_nao_conformes = 0
    itens_na = 0
    
    for item in ItemInspecaoApontado.query.all():
        total_itens += 1
        if item.resultado == 'conforme':
            itens_conformes += 1
        elif item.resultado == 'nao_conforme':
            itens_nao_conformes += 1
        elif item.resultado == 'na':
            itens_na += 1
    
    return jsonify({
        'ordens': {
            'total': total_ordens,
            'pendentes': ordens_pendentes,
            'em_andamento': ordens_em_andamento,
            'concluidas': ordens_concluidas
        },
        'itens': {
            'total': total_itens,
            'conformes': itens_conformes,
            'nao_conformes': itens_nao_conformes,
            'na': itens_na
        }
    })
