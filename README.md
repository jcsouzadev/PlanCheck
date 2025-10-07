# 🛠️ PlanCheck - Sistema de Gestão de Manutenção e Inspeção

Sistema web completo para gerenciamento de planos de manutenção e inspeção de equipamentos industriais, desenvolvido em Python com Flask e PostgreSQL.

## 📋 Sobre o Projeto

PlanCheck é uma solução moderna e intuitiva para gestão de manutenção preventiva e inspeção de equipamentos industriais. O sistema oferece controle hierárquico completo desde empresas até equipamentos específicos, permitindo criar planos de inspeção detalhados, gerar ordens de execução automáticas e acompanhar o cumprimento através de dashboards analíticos.

### ✨ Principais Funcionalidades

#### 🏗️ Hierarquia de Equipamentos
- Estrutura organizacional completa: **Empresa → Setor → Área → Conjunto → Subconjunto → Equipamento**
- CRUD completo para todos os níveis hierárquicos
- Visualização em árvore expansível e navegável
- Exclusão em cascata com integridade referencial

#### 📝 Planos de Inspeção
- Criação de planos vinculados a equipamentos específicos
- Três tipos de itens inspecionais:
  - **Visual**: Inspeção por visualização
  - **Sensitiva**: Inspeção por toque, som, vibração
  - **Medições/Grandezas**: Valores numéricos com limites mínimo e máximo configuráveis
- Definição de frequência de execução (por hora ou diário)
- Configuração de data de início e tipo de geração

#### ✅ Ordens de Execução
- Geração automática de ordens baseada na frequência dos planos
- Atribuição de ordens a executantes específicos
- Checklist interativo para execução em campo
- Registro de não conformidades com campos dinâmicos:
  - Falha identificada
  - Solução proposta
  - Tempo necessário e quantidade de executantes
  - Materiais necessários
- Controle de status: Pendente, Em Andamento, Concluída

#### 📊 Dashboard Analítico
- **Tabela de Cumprimento de Planos**: Exibe equipamentos com ordens programadas, realizadas e % de cumprimento
- **Gráfico de Barras Agrupadas Mensal**: Visualização de ordens programadas vs realizadas por mês (MM/YYYY)
- **Lista Interativa de Ordens**: Tabela com filtros de data e ícones de status coloridos
- **Indicadores de Performance**: Cores dinâmicas baseadas em % de cumprimento (verde ≥80%, amarelo ≥50%, vermelho <50%)
- **Gráfico de Linha Temporal**: Evolução das últimas 30 inspeções

#### 📄 Relatórios Profissionais
- **PDF Formato A4**: Relatórios de ordem de serviço com layout profissional
- **Excel**: Exportação de dados para análise avançada
- Relatórios por plano com todos os itens de inspeção
- Relatórios por equipamento com hierarquia completa

#### 🔐 Controle de Acesso
- Sistema de autenticação baseado em funções
- **Administrador**: Acesso total ao sistema (CRUD completo)
- **Executante**: Visualização e execução de ordens atribuídas
- Proteção de rotas sensíveis

#### 📱 Interface Responsiva
- Layout adaptativo para desktop e mobile
- Cards condensados em dispositivos móveis (<768px)
- Tabelas completas em desktop (≥768px)
- Experiência otimizada para tablets e smartphones

## 🎨 Identidade Visual

**Paleta de Cores "Pentire Cool Summer Day"** (WCAG AA Acessível):

- **#295673** - Azul petróleo escuro (primária)
- **#7AAD6B** - Verde suave (sucesso)
- **#C7D7E4** - Azul claro acinzentado (secundária)
- **#F2EBF3** - Lavanda muito claro (fundos)
- **#FFC107** - Amarelo (avisos)
- **#DC3545** - Vermelho (perigo)

## 🚀 Tecnologias Utilizadas

### Backend
- **Python 3.11**
- **Flask 3.1.2** - Framework web
- **Flask-SQLAlchemy 3.1.1** - ORM para banco de dados
- **Flask-Login 0.6.3** - Gerenciamento de autenticação
- **Flask-Migrate 4.1.0** - Migrações de banco de dados
- **PostgreSQL** - Banco de dados relacional
- **psycopg2-binary 2.9.10** - Adaptador PostgreSQL

### Geração de Relatórios
- **WeasyPrint 66.0** - Geração de PDF profissional
- **Pandas 2.3.3** - Manipulação de dados
- **OpenPyXL 3.1.5** - Geração de planilhas Excel

### Frontend
- **Bootstrap 5.3.0** - Framework CSS responsivo
- **Bootstrap Icons 1.11.0** - Biblioteca de ícones
- **Chart.js 4.4.0** - Gráficos interativos
- **JavaScript Vanilla** - Interatividade

## 📦 Instalação e Execução

### Pré-requisitos
- Python 3.11+
- PostgreSQL 12+
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/plancheck-sistema-manutencao.git
cd plancheck-sistema-manutencao
```

2. **Configure o ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**
Crie um arquivo `.env` na raiz do projeto:
```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/plancheck
SESSION_SECRET=sua-chave-secreta-aqui
```

5. **Inicialize o banco de dados:**
```bash
python init_db.py
```

6. **Execute a aplicação:**
```bash
python app.py
```

7. **Acesse o sistema:**
Abra o navegador em `http://localhost:5000`

## 👤 Credenciais Padrão

### Administrador
- **Usuário**: `admin`
- **Senha**: `admin123`

### Executante
- **Usuário**: `executante`
- **Senha**: `exec123`

⚠️ **Importante**: Altere as credenciais padrão após o primeiro acesso em ambiente de produção.

## 📁 Estrutura do Projeto

```
plancheck-sistema-manutencao/
│
├── app.py                      # Aplicação principal Flask
├── config.py                   # Configurações do sistema
├── models.py                   # Modelos do banco de dados (SQLAlchemy)
├── routes.py                   # Rotas e controladores
├── utils.py                    # Funções auxiliares (PDF/Excel)
├── init_db.py                  # Script de inicialização do BD
├── requirements.txt            # Dependências Python
├── replit.md                   # Documentação técnica detalhada
│
├── templates/                  # Templates Jinja2
│   ├── base.html              # Template base
│   ├── login.html             # Tela de login
│   ├── index.html             # Dashboard analítico
│   ├── empresas.html          # CRUD de empresas
│   ├── editar_empresa.html    # Formulário de empresa
│   ├── ver_empresa.html       # Visualização hierárquica
│   ├── planos.html            # Lista de planos
│   ├── editar_plano.html      # Formulário de planos
│   ├── ver_plano.html         # Visualização de planos
│   ├── ordens.html            # Lista de ordens
│   ├── ver_ordem.html         # Visualização de ordens
│   ├── executar_ordem.html    # Checklist de execução
│   └── relatorio_plano.html   # Template para PDF
│
└── static/                     # Arquivos estáticos
    ├── css/
    │   └── style.css          # Estilos customizados (v10)
    └── js/
        └── main.js            # JavaScript principal
```

## 🔄 Fluxo de Uso

1. **Configuração Inicial (Admin)**
   - Criar empresa
   - Definir hierarquia (Setor → Área → Conjunto → Subconjunto → Equipamento)

2. **Criação de Planos (Admin)**
   - Vincular plano a equipamento
   - Adicionar itens de inspeção (Visual, Sensitiva, Medições)
   - Definir frequência e data de início

3. **Geração de Ordens (Admin)**
   - Gerar ordens automaticamente baseado na frequência
   - Atribuir ordens a executantes

4. **Execução (Executante)**
   - Acessar ordens atribuídas
   - Preencher checklist interativo
   - Registrar não conformidades quando necessário
   - Finalizar ordem

5. **Análise (Admin)**
   - Visualizar dashboard com indicadores
   - Exportar relatórios em PDF/Excel
   - Acompanhar % de cumprimento de planos

## 📊 APIs Internas

### Endpoints do Dashboard
- `GET /api/dashboard/stats` - Estatísticas gerais
- `GET /api/dashboard/equipamentos` - Tabela de cumprimento de planos
- `GET /api/dashboard/ordens` - Lista de ordens com filtros de data

### Parâmetros de Filtro
- `data_inicio` - Data de início (formato: YYYY-MM-DD)
- `data_fim` - Data de fim (formato: YYYY-MM-DD)

## 🔒 Segurança

- Senhas armazenadas com hash seguro (Werkzeug)
- Proteção CSRF em formulários
- Controle de acesso baseado em funções (RBAC)
- Validação de dados no servidor
- Sessões seguras com chave secreta

## 🚀 Deploy em Produção

### Recomendações
1. **Servidor WSGI**: Use Gunicorn ou uWSGI (não use o servidor de desenvolvimento Flask)
2. **Proxy Reverso**: Configure Nginx ou Apache na frente
3. **HTTPS**: Sempre use certificado SSL/TLS
4. **Variáveis de Ambiente**: Nunca commite credenciais no código
5. **Backup**: Configure backups automáticos do PostgreSQL

### Exemplo com Gunicorn
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 4 app:app
```

## 📈 Próximas Melhorias

- [ ] Sistema de notificações para ordens pendentes
- [ ] Filtros avançados e busca em todas as listas
- [ ] Dashboard com drill-down por empresa/setor
- [ ] Upload de fotos durante inspeção
- [ ] Assinatura digital de responsáveis
- [ ] API REST para integração externa
- [ ] App mobile nativo (iOS/Android)
- [ ] Relatórios avançados com gráficos personalizáveis

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas, sugestões ou reportar problemas, abra uma [issue](https://github.com/seu-usuario/plancheck-sistema-manutencao/issues) no GitHub.

---

**Desenvolvido com ❤️ usando Flask e PostgreSQL**
