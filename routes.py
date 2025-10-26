from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
# IMPORT COMPLETO COM NOVO MODELO COMPONENTE
from models import db, User, Empresa, Setor, Area, Conjunto, Subconjunto, Equipamento, PlanoInspecao, ItemInspecao, OrdemExecucao, ItemInspecaoApontado, Componente 
from utils import gerar_pdf, gerar_excel
from datetime import datetime, timedelta
import pandas as pd
from functools import wraps
# IMPORTAÇÕES ESSENCIAIS PARA OTIMIZAÇÃO DE CONSULTAS
from sqlalchemy.orm import joinedload
from sqlalchemy import func

main_bp = Blueprint('main', __name__)

# ==============================================================================
# DECORADORES
# ==============================================================================
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Acesso negado. Apenas administradores podem acessar esta página.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

# ==============================================================================
# Rotas de Navegação e Autenticação
# ==============================================================================
@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        total_equipamentos = Equipamento.query.count()
        total_planos = PlanoInspecao.query.count()
        total_ordens = OrdemExecucao.query.count()
        ordens_pendentes = OrdemExecucao.query.filter_by(status='pendente').count()

        return render_template('index.html', 
                             total_equipamentos=total_equipamentos,
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

# ==============================================================================
# Rotas de CRUD da Hierarquia (Empresa)
# ==============================================================================
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

# ==============================================================================
# Rotas de CRUD da Hierarquia (Setor, Área, Conjunto, Subconjunto)
# ==============================================================================
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

# ==============================================================================
# Rotas de CRUD de Equipamento (Com Gestão de Ativos)
# ==============================================================================
@main_bp.route('/subconjuntos/<int:subconjunto_id>/equipamento', methods=['POST'])
@login_required
@admin_required
def adicionar_equipamento(subconjunto_id):
    subconjunto = Subconjunto.query.get_or_404(subconjunto_id)
    nome = request.form.get('nome')
    codigo = request.form.get('codigo')
    criticidade = request.form.get('criticidade') 
    valor_aquisicao = request.form.get('valor_aquisicao') 

    if nome:
        equipamento = Equipamento(
            nome=nome, 
            codigo=codigo, 
            subconjunto_id=subconjunto.id,
            criticidade=criticidade,
            valor_aquisicao=float(valor_aquisicao) if valor_aquisicao else None
        )
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
    criticidade = request.form.get('criticidade') 
    valor_aquisicao = request.form.get('valor_aquisicao') 

    if nome:
        equipamento.nome = nome
        equipamento.codigo = codigo
        equipamento.criticidade = criticidade
        equipamento.valor_aquisicao = float(valor_aquisicao) if valor_aquisicao else None
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

# ==============================================================================
# Rotas de CRUD de COMPONENTE (Novo Nível)
# ==============================================================================
@main_bp.route('/equipamentos/<int:equipamento_id>/componente', methods=['POST'])
@login_required
@admin_required
def adicionar_componente(equipamento_id):
    equipamento = Equipamento.query.get_or_404(equipamento_id)
    nome = request.form.get('nome')
    tag = request.form.get('tag')
    vida_util_estimada = request.form.get('vida_util_estimada')

    if nome:
        componente = Componente(
            nome=nome, 
            tag=tag,
            vida_util_estimada=float(vida_util_estimada) if vida_util_estimada else None,
            equipamento_id=equipamento.id
        )
        db.session.add(componente)
        db.session.commit()
        flash('Componente adicionado com sucesso!', 'success')

    empresa_id = equipamento.subconjunto.conjunto.area.setor.empresa_id
    return redirect(url_for('main.ver_empresa', empresa_id=empresa_id))

@main_bp.route('/componentes/<int:componente_id>/editar', methods=['POST'])
@login_required
@admin_required
def editar_componente(componente_id):
    componente = Componente.query.get_or_404(componente_id)

    nome = request.form.get('nome')
    tag = request.form.get('tag')
    vida_util_estimada_str = request.form.get('vida_util_estimada')

    if nome:
        componente.nome = nome
        componente.tag = tag

        try:
            componente.vida_util_estimada = float(vida_util_estimada_str) if vida_util_estimada_str else None
        except ValueError:
            flash('Erro: A Vida Útil Estimada deve ser um número.', 'danger')
            equipamento = componente.equipamento
            empresa_id = equipamento.subconjunto.conjunto.area.setor.empresa_id
            return redirect(url_for('main.ver_empresa', empresa_id=empresa_id))

    db.session.commit()

    flash('Componente atualizado com sucesso!', 'success')
    equipamento = componente.equipamento
    empresa_id = equipamento.subconjunto.conjunto.area.setor.empresa_id
    return redirect(url_for('main.ver_empresa', empresa_id=empresa_id))


@main_bp.route('/componentes/<int:componente_id>/delete', methods=['POST'])
@login_required
@admin_required
def deletar_componente(componente_id):
    componente = Componente.query.get_or_404(componente_id)
    equipamento = componente.equipamento 

    empresa_id = equipamento.subconjunto.conjunto.area.setor.empresa_id

    db.session.delete(componente)
    db.session.commit()
    flash('Componente excluído com sucesso!', 'success')
    return redirect(url_for('main.ver_empresa', empresa_id=empresa_id))

# ==============================================================================
# Rotas de Planos de Inspeção
# ==============================================================================
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
    usuarios = User.query.all()
    return render_template('ver_plano.html', plano=plano, User=User)

@main_bp.route('/planos/<int:plano_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_plano(plano_id):
    plano = PlanoInspecao.query.get_or_404(plano_id)

    if request.method == 'POST':
        if 'adicionar_item' in request.form:
            descricao = request.form.get('descricao')
            tipo = request.form.get('tipo')
            observacao = request.form.get('observacao')
            valor_min = request.form.get('valor_min')
            valor_max = request.form.get('valor_max')

            if descricao:
                item = ItemInspecao(
                    descricao=descricao,
                    tipo=tipo,
                    observacao=observacao if observacao else None,
                    valor_min=float(valor_min) if valor_min else None,
                    valor_max=float(valor_max) if valor_max else None,
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

# ==============================================================================
# Rotas de Ordens de Execução e Lógica de Geração
# ==============================================================================
@main_bp.route('/planos/<int:plano_id>/gerar-ordem', methods=['POST'])
@login_required
@admin_required
def gerar_ordem_automatica(plano_id):
    plano = PlanoInspecao.query.get_or_404(plano_id)
    executante_id = request.form.get('executante_id')

    if not executante_id:
        flash('Selecione um executante!', 'warning')
        return redirect(url_for('main.ver_plano', plano_id=plano_id))

    ultima_ordem = OrdemExecucao.query.filter_by(plano_id=plano_id).order_by(OrdemExecucao.data_programada.desc()).first()

    if plano.tipo_geracao == 'horario':
        if ultima_ordem:
            data_programada = ultima_ordem.data_programada + timedelta(hours=plano.frequencia)
        else:
            data_programada = plano.data_inicio or datetime.now()
    elif plano.tipo_geracao == 'diario':
        if ultima_ordem:
            data_programada = ultima_ordem.data_programada + timedelta(days=plano.frequencia)
        else:
            data_programada = plano.data_inicio or datetime.now()
    else:
        data_programada = datetime.now()

    ordem = OrdemExecucao(
        plano_id=plano_id,
        executante_id=executante_id,
        data_programada=data_programada
    )
    db.session.add(ordem)
    db.session.commit()

    flash(f'Ordem gerada automaticamente para {data_programada.strftime("%d/%m/%Y %H:%M")}!', 'success')
    return redirect(url_for('main.ver_plano', plano_id=plano_id))

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

# ==============================================================================
# Rotas de Relatórios
# ==============================================================================
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

@main_bp.route('/relatorios/ordens/<int:ordem_id>/pdf')
@login_required
def relatorio_ordem_pdf(ordem_id):
    from datetime import datetime
    ordem = OrdemExecucao.query.get_or_404(ordem_id)
    return gerar_pdf('relatorio_ordem.html', ordem=ordem, data_geracao=datetime.now())

@main_bp.route('/relatorios/ordens/<int:ordem_id>/excel')
@login_required
def relatorio_ordem_excel(ordem_id):
    ordem = OrdemExecucao.query.get_or_404(ordem_id)
    data = []

    for apontamento in ordem.itens_apontados:
        data.append({
            'Item': apontamento.item_inspecao.descricao,
            'Tipo': apontamento.item_inspecao.tipo or '-',
            'Resultado': apontamento.resultado or '-',
            'Observação': apontamento.observacao or '-',
            'Valor Atual': apontamento.valor_atual or '-',
            'Falha': apontamento.falha or '-',
            'Solução': apontamento.solucao or '-',
            'Tempo (h)': apontamento.tempo_necessario or '-',
            'Qtd Executantes': apontamento.qtde_executantes or '-',
            'Materiais': apontamento.materiais or '-'
        })

    df = pd.DataFrame(data)
    return gerar_excel(df, filename=f'ordem_{ordem_id}.xlsx')

@main_bp.route('/relatorios/equipamentos/<int:equipamento_id>/pdf')
@login_required
def relatorio_equipamento_pdf(equipamento_id):
    equipamento = Equipamento.query.get_or_404(equipamento_id)
    planos = PlanoInspecao.query.filter_by(equipamento_id=equipamento_id).all()
    return gerar_pdf('relatorio_equipamento.html', equipamento=equipamento, planos=planos)

# ==============================================================================
# Rotas OTIMIZADAS de API para o Dashboard
# ==============================================================================
@main_bp.route('/api/dashboard/stats')
@login_required
def dashboard_stats():
    total_ordens = OrdemExecucao.query.count()
    ordens_pendentes = OrdemExecucao.query.filter_by(status='pendente').count()
    ordens_em_andamento = OrdemExecucao.query.filter_by(status='em_andamento').count()
    ordens_concluidas = OrdemExecucao.query.filter_by(status='concluida').count()

    # Agregação Mensal (Mantido o processamento Python)
    todas_ordens = OrdemExecucao.query.all()
    dados_mensais = {}

    for ordem in todas_ordens:
        data_ref = ordem.data_programada if ordem.data_programada else ordem.data_criacao
        if data_ref:
            data_ref = data_ref if isinstance(data_ref, datetime) else datetime(data_ref.year, data_ref.month, data_ref.day)

            mes_str = data_ref.strftime('%m/%Y')
            if mes_str not in dados_mensais:
                dados_mensais[mes_str] = {'programadas': 0, 'realizadas': 0}

            dados_mensais[mes_str]['programadas'] += 1
            if ordem.status == 'concluida':
                dados_mensais[mes_str]['realizadas'] += 1

    meses_ordenados = sorted(dados_mensais.keys(), key=lambda x: datetime.strptime(x, '%m/%Y'))
    meses = meses_ordenados[-6:] if len(meses_ordenados) > 6 else meses_ordenados

    programadas_mensal = [dados_mensais[m]['programadas'] for m in meses]
    realizadas_mensal = [dados_mensais[m]['realizadas'] for m in meses]
    percentual_mensal = [round((dados_mensais[m]['realizadas'] / dados_mensais[m]['programadas'] * 100), 1) if dados_mensais[m]['programadas'] > 0 else 0 for m in meses]

    # OTIMIZAÇÃO CRÍTICA: Estatísticas por Equipamento (Agregação no PostgreSQL)
    equipamentos_data_agregada = db.session.query(
        Equipamento.nome,
        Equipamento.codigo,
        func.count(OrdemExecucao.id).label('total_programadas'),
        func.sum(db.case((OrdemExecucao.status == 'concluida', 1), else_=0)).label('total_realizadas')
    ).select_from(Equipamento).outerjoin(PlanoInspecao).outerjoin(OrdemExecucao).group_by(
        Equipamento.id, Equipamento.nome, Equipamento.codigo
    ).all()

    equipamentos_stats = []
    for nome, codigo, total_programadas, total_realizadas in equipamentos_data_agregada:
        percentual = round((total_realizadas / total_programadas * 100), 1) if total_programadas > 0 else 0

        equipamentos_stats.append({
            'equipamento': nome,
            'codigo': codigo or '-',
            'programadas': total_programadas,
            'realizadas': total_realizadas,
            'percentual': percentual
        })

    equipamentos_stats.sort(key=lambda x: x['percentual'], reverse=True)

    return jsonify({
        'ordens': {
            'total': total_ordens,
            'pendentes': ordens_pendentes,
            'em_andamento': ordens_em_andamento,
            'concluidas': ordens_concluidas
        },
        'equipamentos': equipamentos_stats,
        'mensal': {
            'meses': meses,
            'programadas': programadas_mensal,
            'realizadas': realizadas_mensal,
            'percentual': percentual_mensal
        }
    })

@main_bp.route('/api/dashboard/ordens')
@login_required
def dashboard_ordens():
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')

    # OTIMIZAÇÃO CRÍTICA: Eager Loading (joinedload) para carregar relações em poucas queries.
    query = OrdemExecucao.query.options(
        joinedload(OrdemExecucao.plano).joinedload(PlanoInspecao.equipamento),
        joinedload(OrdemExecucao.executante)
    )

    if data_inicio:
        data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d')
        query = query.filter(OrdemExecucao.data_programada >= data_inicio_obj)

    if data_fim:
        data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d') + timedelta(days=1, seconds=-1) 
        query = query.filter(OrdemExecucao.data_programada <= data_fim_obj)

    ordens = query.order_by(OrdemExecucao.data_programada.desc()).all()

    ordens_lista = []
    hoje_date = datetime.now().date() 

    for ordem in ordens:
        data_prog = ordem.data_programada.strftime('%d/%m/%Y') if ordem.data_programada else '-'
        data_real = ordem.data_conclusao.strftime('%d/%m/%Y') if ordem.data_conclusao else '-'

        status_visual = ordem.status

        if ordem.status == 'concluida':
            if ordem.data_conclusao and ordem.data_programada:
                if ordem.data_conclusao.date() <= ordem.data_programada.date():
                    status_visual = 'no_prazo'
                else:
                    status_visual = 'atrasado_concluido' 
            else:
                status_visual = 'concluido'
        elif ordem.status == 'pendente':
            if ordem.data_programada and ordem.data_programada.date() < hoje_date:
                status_visual = 'atrasado'
            else:
                status_visual = 'pendente'
        elif ordem.status == 'em_andamento':
            status_visual = 'em_andamento'

        ordens_lista.append({
            'id': ordem.id,
            'plano': ordem.plano.titulo if ordem.plano else '-',
            'equipamento': ordem.plano.equipamento.nome if ordem.plano and ordem.plano.equipamento else '-',
            'executante': ordem.executante.username if ordem.executante else '-',
            'data_programada': data_prog,
            'data_realizada': data_real,
            'status': ordem.status,
            'status_visual': status_visual
        })

    return jsonify(ordens_lista)

# ==============================================================================
# Rotas de CRUD de Usuários
# ==============================================================================
@main_bp.route('/usuarios', methods=['GET'])
@login_required
@admin_required
def usuarios():
    usuarios = User.query.order_by(User.nome).all()
    return render_template('usuarios.html', usuarios=usuarios)

@main_bp.route('/usuarios/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo_usuario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        matricula = request.form.get('matricula')
        funcao = request.form.get('funcao')
        area = request.form.get('area')
        setor = request.form.get('setor')
        perfil_acesso = request.form.get('perfil_acesso')
        username = request.form.get('username')
        password = request.form.get('password')

        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('Nome de usuário já existe!', 'danger')
            return redirect(url_for('main.novo_usuario'))

        matricula_exists = User.query.filter_by(matricula=matricula).first()
        if matricula_exists:
            flash('Matrícula já cadastrada!', 'danger')
            return redirect(url_for('main.novo_usuario'))

        novo_user = User(
            nome=nome,
            matricula=matricula,
            funcao=funcao,
            area=area,
            setor=setor,
            perfil_acesso=perfil_acesso,
            username=username
        )
        novo_user.set_password(password)

        db.session.add(novo_user)
        db.session.commit()

        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('main.usuarios'))

    return render_template('editar_usuario.html', usuario=None)

@main_bp.route('/usuarios/<int:usuario_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_usuario(usuario_id):
    usuario = User.query.get_or_404(usuario_id)

    if request.method == 'POST':
        nome = request.form.get('nome')
        matricula = request.form.get('matricula')
        funcao = request.form.get('funcao')
        area = request.form.get('area')
        setor = request.form.get('setor')
        perfil_acesso = request.form.get('perfil_acesso')
        username = request.form.get('username')
        password = request.form.get('password')

        user_exists = User.query.filter(User.username == username, User.id != usuario_id).first()
        if user_exists:
            flash('Nome de usuário já existe!', 'danger')
            return redirect(url_for('main.editar_usuario', usuario_id=usuario_id))

        matricula_exists = User.query.filter(User.matricula == matricula, User.id != usuario_id).first()
        if matricula_exists:
            flash('Matrícula já cadastrada!', 'danger')
            return redirect(url_for('main.editar_usuario', usuario_id=usuario_id))

        usuario.nome = nome
        usuario.matricula = matricula
        usuario.funcao = funcao
        usuario.area = area
        usuario.setor = setor
        usuario.perfil_acesso = perfil_acesso
        usuario.username = username

        if password:
            usuario.set_password(password)

        db.session.commit()

        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('main.usuarios'))

    return render_template('editar_usuario.html', usuario=usuario)

@main_bp.route('/usuarios/<int:usuario_id>/delete', methods=['POST'])
@login_required
@admin_required
def deletar_usuario(usuario_id):
    usuario = User.query.get_or_404(usuario_id)

    if usuario.id == current_user.id:
        flash('Você não pode excluir seu próprio usuário!', 'danger')
        return redirect(url_for('main.usuarios'))

    db.session.delete(usuario)
    db.session.commit()

    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('main.usuarios'))