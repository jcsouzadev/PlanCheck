# 🛠️ PlanCheck - Sistema de Gestão de Manutenção e Inspeção

Sistema web completo para gerenciamento de planos de manutenção e inspeção de equipamentos industriais, desenvolvido em Python com Flask e PostgreSQL.

## 📋 Sobre o Projeto

PlanCheck é uma solução moderna e intuitiva para gestão de manutenção preventiva e corretiva de equipamentos industriais. O sistema oferece controle hierárquico completo desde empresas até componentes específicos, permitindo criar planos de inspeção detalhados, gerar ordens de execução automáticas, registrar manutenções não programadas e acompanhar o cumprimento através de dashboards analíticos avançados.

## ✨ Principais Funcionalidades

### 🏗️ Hierarquia Completa de Equipamentos (7 Níveis)

- **Estrutura organizacional**: Empresa → Setor → Área → Conjunto → Subconjunto → Equipamento → Componente
- CRUD completo para todos os níveis hierárquicos com botões visuais (editar/excluir)
- **Cadastro de Empresa Completo**:
  - Nome da empresa (obrigatório)
  - CNPJ formatado (XX.XXX.XXX/XXXX-XX)
  - Endereço completo: CEP, Cidade, País
  - Logo/Imagem da empresa (upload JPG, PNG, GIF até 2MB)
- Visualização em árvore expansível e interativa
- Exclusão em cascata com confirmação prévia
- Interface AJAX sem recarregamento total

### 📝 Planos de Inspeção Configuráveis

- Criação de planos vinculados a equipamentos específicos
- **Três tipos de itens inspecionais**:
  - **Visual**: Inspeção por visualização
  - **Sensitiva**: Inspeção por toque, som, vibração
  - **Medições/Grandezas**: Valores numéricos com limites min/max configuráveis
- Tipos de geração: por hora, diário ou data de abertura
- Definição de frequência e data de início
- Geração automática de ordens baseada em frequência

### ✅ Dois Tipos de Ordens de Execução

#### 📅 Ordens Programadas (Preventiva)
- Geração automática baseada nos planos de inspeção
- Checklist interativo completo para execução em campo
- Registro de não conformidades com campos dinâmicos:
  - Falha identificada
  - Solução proposta
  - Tempo necessário e quantidade de executantes
  - Materiais necessários
- Controle de status: Pendente, Em Andamento, Concluída

#### 🔧 Ordens Não Programadas (Corretiva/Emergencial)
- **Criação manual** para manutenções corretivas ou trabalhos não planejados
- **Seleção hierárquica em cascata**: Empresa → Setor → Área → Equipamento
- APIs REST dinâmicas para preenchimento automático de campos
- **Rastreamento completo de execução**:
  - Data e hora de início da execução
  - Data e hora de término da execução
  - Cálculo automático de duração (horas e minutos)
  - Validação: término deve ser posterior ao início
  - Serviço solicitado e serviço executado
  - Diagnóstico de falha detalhado
- Atribuição a múltiplos executantes
- Templates de PDF específicos sem checklist de inspeção

### 📊 Dashboard Analítico Avançado

#### 📈 Indicadores em Tempo Real
- **Cards de Estatísticas**:
  - Total de Equipamentos
  - Total de Planos
  - Total de Ordens
  - Ordens Pendentes (destaque vermelho)

#### 📉 Gráficos e Análises
- **Tabela de Cumprimento de Planos**: Equipamentos com ordens programadas, realizadas e % de cumprimento
- **Gráfico de Pizza - Tipos de Ordem**: Comparação visual entre ordens Programadas (azul) vs Não Programadas (vermelho)
- **Gráfico de Rosca - Status de Ordens Não Programadas**: Pendentes (vermelho), Em Andamento (azul), Concluídas (verde)
- **Card de Manutenções NÃO PROGRAMADAS**: Contadores por status em gradiente vermelho
- **Gráfico de Barras - Status das Ordens**: Pendentes (vermelho), Em Andamento (azul), Concluídas (verde)
- **Gráfico Mensal Agrupado**: Ordens programadas vs realizadas com % de cumprimento (últimos 6 meses)
- **Lista Interativa de Ordens**: Tabela com filtros de data e ícones de status coloridos

#### 🎨 Indicadores Visuais
- Cores dinâmicas baseadas em performance:
  - 🟢 Verde: ≥80% de cumprimento
  - 🟡 Amarelo: ≥50% de cumprimento
  - 🔴 Vermelho: <50% de cumprimento

### 📄 Relatórios Profissionais

#### PDF Formato A4
- **Relatórios de Ordem de Serviço**:
  - Cabeçalho: Logo da empresa + Nome + CNPJ
  - Corpo: Detalhes completos da ordem
  - Rodapé: Endereço completo (CEP, Cidade, País)
- **Relatórios Diferenciados**:
  - Ordens Programadas: Com tabela completa de checklist
  - Ordens Não Programadas: Focado em rastreamento de execução
- **Relatórios de Equipamento**: Visualização hierárquica com todos os planos

#### Excel para Análise
- Exportação completa de dados de ordens
- Formato otimizado para análise avançada
- Planilhas com todos os itens de inspeção

### 👥 Gestão Completa de Usuários

- **CRUD Completo** (exclusivo para administradores):
  - Nome completo
  - Matrícula única
  - Função (cargo/atividade)
  - Área de atuação e Setor
  - Perfil de acesso (Administrador/Executante)
  - Credenciais de login (usuário e senha)
- Validação de unicidade de matrícula e username
- Proteção contra auto-exclusão
- Interface intuitiva com listagem e formulários

### 🔐 Controle de Acesso (RBAC)

- **Administrador**: Acesso total (CRUD de todos os recursos, incluindo usuários)
- **Executante**: Visualização e execução de ordens atribuídas
- Proteção de rotas sensíveis
- Autenticação baseada em sessão

### 📱 Interface Responsiva

- Layout adaptativo para desktop, tablet e mobile
- Cards condensados em dispositivos móveis (<768px)
- Tabelas completas em desktop (≥768px)
- Experiência otimizada para todos os tamanhos de tela

## 🎨 Identidade Visual

### Paleta de Cores "Pentire Cool Summer Day" (WCAG AA)

- **#295673** - Azul petróleo escuro (cor principal)
  - Navbar, botões primários, cabeçalhos, ordens programadas, status "Em Andamento"

- **#7AAD6B** - Verde suave (sucesso)
  - Itens conformes, status "Concluída", gráficos de sucesso

- **#C7D7E4** - Azul claro acinzentado (secundária)
  - Cabeçalhos de cards, fundos de tabelas, itens N/A

- **#F2EBF3** - Lavanda muito claro (fundos suaves)
  - Fundo do body, caixas de informação em relatórios

- **#FFC107** - Amarelo (avisos)
  - Alertas gerais, medições fora da faixa

- **#DC3545** - Vermelho (perigo/pendente/não programada)
  - **Status "Pendente"** (em todos os contextos)
  - **Ordens "Não Programadas"** (tipo)
  - **Card de Manutenções NÃO PROGRAMADAS**
  - Itens não conformes, erros, validações

### Padronização Visual
✅ **Vermelho = Pendente + Não Programada** em todo o sistema

## 🚀 Tecnologias Utilizadas

### Backend
- **Python 3.11**
- **Flask 3.1.2** - Framework web
- **Flask-SQLAlchemy 3.1.1** - ORM para banco de dados
- **Flask-Login 0.6.3** - Gerenciamento de autenticação
- **Flask-Migrate 4.1.0** - Migrações de banco de dados
- **PostgreSQL** - Banco de dados relacional (Neon)
- **psycopg2-binary** - Adaptador PostgreSQL

### Geração de Relatórios
- **WeasyPrint 66.0** - Geração de PDF profissional
- **Pandas 2.3.3** - Manipulação de dados
- **OpenPyXL 3.1.5** - Geração de planilhas Excel

### Frontend
- **Bootstrap 5.3.0** - Framework CSS responsivo
- **Bootstrap Icons 1.11.0** - Biblioteca de ícones
- **Chart.js 4.4.0** - Gráficos interativos
- **JavaScript Vanilla** - Interatividade e AJAX

## 📦 Instalação e Execução

### Pré-requisitos
- Python 3.11+
- PostgreSQL 12+
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/plancheck.git
cd plancheck
```

2. **Instale as dependências:**
```bash
pip install flask flask-sqlalchemy flask-login flask-migrate psycopg2-binary weasyprint pandas openpyxl werkzeug
```

3. **Configure as variáveis de ambiente:**
```bash
export DATABASE_URL=postgresql://usuario:senha@localhost:5432/plancheck
export SESSION_SECRET=sua-chave-secreta-aqui
```

4. **Inicialize o banco de dados:**
```bash
python init_db.py
```

5. **Execute a aplicação:**
```bash
python app.py
```

6. **Acesse o sistema:**
```
http://localhost:5000
```

## 👤 Credenciais Padrão

### Administrador
- **Usuário**: `admin`
- **Senha**: `admin123`

### Executante
- **Usuário**: `executante`
- **Senha**: `exec123`

⚠️ **Importante**: Altere as credenciais após o primeiro acesso em produção!

## 📁 Estrutura do Projeto

```
plancheck/
│
├── app.py                      # Aplicação principal Flask
├── config.py                   # Configurações do sistema
├── models.py                   # Modelos do banco de dados (SQLAlchemy)
├── routes.py                   # Rotas e controladores
├── utils.py                    # Funções auxiliares (PDF/Excel)
├── init_db.py                  # Script de inicialização do BD
├── replit.md                   # Documentação técnica detalhada
│
├── templates/                  # Templates Jinja2
│   ├── base.html              # Template base
│   ├── login.html             # Tela de login
│   ├── index.html             # Dashboard analítico
│   ├── empresas.html          # Lista de empresas
│   ├── editar_empresa.html    # Formulário de empresa
│   ├── ver_empresa.html       # Visualização hierárquica
│   ├── planos.html            # Lista de planos
│   ├── editar_plano.html      # Formulário de planos
│   ├── ver_plano.html         # Visualização de planos
│   ├── ordens.html            # Lista de ordens
│   ├── ver_ordem.html         # Visualização de ordens
│   ├── executar_ordem.html    # Checklist de execução
│   ├── usuarios.html          # Lista de usuários
│   ├── editar_usuario.html    # Formulário de usuários
│   ├── relatorio_ordem.html   # PDF ordem programada
│   └── relatorio_ordem_nao_programada.html  # PDF ordem não programada
│
└── static/                     # Arquivos estáticos
    ├── css/
    │   └── style.css          # Estilos customizados
    └── js/
        └── main.js            # JavaScript principal
```

## 🔄 Fluxo de Uso Completo

### 1️⃣ Configuração Inicial (Administrador)
- Criar empresa com logo e dados completos
- Definir hierarquia completa (7 níveis)
- Cadastrar usuários executantes

### 2️⃣ Criação de Planos (Administrador)
- Vincular plano a equipamento
- Adicionar itens de inspeção (Visual, Sensitiva, Medições)
- Definir frequência e data de início

### 3️⃣ Geração de Ordens Programadas (Administrador)
- Gerar ordens automaticamente baseado na frequência
- Atribuir ordens a executantes

### 4️⃣ Criação de Ordens Não Programadas (Administrador)
- Criar ordem manual para manutenção corretiva
- Selecionar equipamento via cascata hierárquica
- Definir serviço solicitado e tempo previsto
- Atribuir executantes

### 5️⃣ Execução (Executante)
- **Ordens Programadas**: Preencher checklist completo
- **Ordens Não Programadas**: Registrar execução com rastreamento de tempo
- Registrar não conformidades quando necessário
- Finalizar ordem

### 6️⃣ Análise (Administrador)
- Visualizar dashboard com todos os indicadores
- Analisar gráficos de tipos de ordem e status
- Exportar relatórios em PDF/Excel
- Acompanhar % de cumprimento de planos

## 📊 APIs REST Internas

### Endpoints do Dashboard
- `GET /api/dashboard/stats` - Estatísticas gerais e dados mensais
- `GET /api/dashboard/ordens` - Lista de ordens com filtros
- `GET /api/dashboard/tipo-ordem` - Total de ordens programadas vs não programadas
- `GET /api/dashboard/nao-programadas-status` - Status de ordens não programadas

### Endpoints de Seleção Dinâmica
- `GET /api/empresas` - Lista todas as empresas
- `GET /api/setores/<empresa_id>` - Setores de uma empresa
- `GET /api/areas/<setor_id>` - Áreas de um setor
- `GET /api/equipamentos/<area_id>` - Equipamentos de uma área

### Parâmetros de Filtro
- `data_inicio` - Data de início (YYYY-MM-DD)
- `data_fim` - Data de fim (YYYY-MM-DD)

## 🔒 Segurança

- ✅ Senhas armazenadas com hash seguro (Werkzeug)
- ✅ Proteção CSRF em formulários
- ✅ Controle de acesso baseado em funções (RBAC)
- ✅ Validação de dados no servidor
- ✅ Sessões seguras com chave secreta
- ✅ Sanitização de uploads de arquivos

## 🚀 Deploy em Produção

### Recomendações
1. **Servidor WSGI**: Use Gunicorn (não use Flask development server)
2. **Proxy Reverso**: Configure Nginx ou Apache
3. **HTTPS**: Sempre use certificado SSL/TLS
4. **Variáveis de Ambiente**: Nunca commite credenciais
5. **Backup**: Configure backups automáticos do PostgreSQL

### Exemplo com Gunicorn
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 --reuse-port --workers 4 app:app
```

## 📈 Funcionalidades Recentes (Outubro 2025)

### ✅ Sistema de Ordens Não Programadas
- Criação manual de ordens para manutenção corretiva
- Rastreamento completo de execução com duração automática
- Template PDF específico sem checklist

### ✅ Dashboard Aprimorado
- Gráfico de Pizza: Programadas vs Não Programadas
- Gráfico de Rosca: Status de ordens não programadas
- Card de Manutenções NÃO PROGRAMADAS em vermelho
- 2 novas APIs REST para análise de dados

### ✅ Padronização Visual
- Vermelho para tudo que é Pendente ou Não Programada
- Identidade visual consistente em todo o sistema

## 📝 Licença

Este projeto está sob a licença MIT.

## 👥 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou reportar problemas, abra uma issue no GitHub.

---

**Desenvolvido com ❤️ usando Flask, PostgreSQL e Chart.js**

*Sistema completo de gestão de manutenção preventiva e corretiva para a indústria*
