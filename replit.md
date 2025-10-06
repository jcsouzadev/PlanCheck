# PlanCheck - Sistema de Gestão de Manutenção e Inspeção

## Visão Geral
Sistema web completo para gestão de planos de manutenção e inspeção de equipamentos industriais, desenvolvido com Flask e PostgreSQL.

## Estrutura do Projeto

```
/project
├── app.py                      # Aplicação principal Flask
├── config.py                   # Configurações do sistema
├── models.py                   # Modelos do banco de dados
├── routes.py                   # Rotas e controladores
├── utils.py                    # Funções auxiliares (PDF/Excel)
├── init_db.py                  # Script de inicialização do BD
├── templates/                  # Templates HTML
│   ├── base.html              # Template base
│   ├── login.html             # Tela de login
│   ├── index.html             # Dashboard
│   ├── empresas.html          # Lista de empresas
│   ├── editar_empresa.html    # Edição de empresa
│   ├── ver_empresa.html       # Visualização hierárquica
│   ├── planos.html            # Lista de planos
│   ├── editar_plano.html      # Edição de planos
│   ├── ver_plano.html         # Visualização de planos
│   ├── ordens.html            # Lista de ordens
│   ├── ver_ordem.html         # Visualização de ordens
│   ├── executar_ordem.html    # Checklist de execução
│   └── relatorio_plano.html   # Template para PDF
└── static/                     # Arquivos estáticos
    ├── css/style.css          # Estilos customizados
    └── js/main.js             # JavaScript principal
```

## Funcionalidades Principais

### 1. Hierarquia de Equipamentos
- Estrutura completa: Empresa → Setor → Área → Conjunto → Subconjunto → Equipamento
- CRUD completo para todos os níveis da hierarquia
- Visualização em árvore expansível

### 2. Planos de Inspeção
- Criação de planos vinculados a equipamentos
- Tipos de geração: por hora, diário ou data de abertura
- Definição de frequência e data de início
- **Três tipos de itens inspecionais:**
  - **Visual**: Inspeção por visualização
  - **Sensitiva**: Inspeção por toque, som, vibração
  - **Medições/Grandezas**: Valores numéricos com limites min/max configuráveis

### 3. Ordens de Execução
- Geração de ordens vinculadas a planos
- Atribuição a executantes
- Acompanhamento de status (Pendente, Em Andamento, Concluída)
- Checklist interativo para execução

### 4. Campos Dinâmicos de Não Conformidade
Os campos de não conformidade aparecem automaticamente quando um item é marcado como "Não Conforme":
- Falha identificada
- Solução proposta
- Tempo necessário (horas)
- Quantidade de executantes
- Materiais necessários
- Outras informações

### 5. Relatórios
- Exportação em PDF com layout profissional
- Exportação em Excel para análise de dados
- Relatórios por plano com todos os itens de inspeção

### 6. Dashboard com Gráficos
- Estatísticas em tempo real
- Gráfico de pizza: Proporção de conformidades
- Gráfico de barras: Status das ordens
- Cards informativos: Total de empresas, planos e ordens

### 7. Controle de Acesso
- Autenticação de usuários
- Dois níveis de permissão:
  - **Administrador**: Acesso total (CRUD de todos os recursos)
  - **Executante**: Visualização e execução de ordens

## Tecnologias Utilizadas

### Backend
- Flask 3.1.2
- Flask-SQLAlchemy 3.1.1
- Flask-Login 0.6.3
- Flask-Migrate 4.1.0
- PostgreSQL (via psycopg2-binary)
- WeasyPrint 66.0 (geração de PDF)
- Pandas 2.3.3 + OpenPyXL 3.1.5 (geração de Excel)

### Frontend
- Bootstrap 5.3.0
- Bootstrap Icons 1.11.0
- Chart.js 4.4.0
- JavaScript Vanilla

## Credenciais de Acesso

### Administrador
- **Usuário**: admin
- **Senha**: admin123

### Executante
- **Usuário**: executante
- **Senha**: exec123

## Instruções de Uso

### 1. Como Começar
1. Faça login com uma das credenciais acima
2. Como admin, comece criando uma empresa
3. Dentro da empresa, adicione a hierarquia (Setor → Área → Conjunto → Subconjunto → Equipamento)
4. Crie planos de inspeção vinculados aos equipamentos
5. Adicione itens de inspeção aos planos
6. Gere ordens de execução e atribua aos executantes

### 2. Executando uma Inspeção
1. Acesse a aba "Ordens"
2. Clique em "Executar" na ordem desejada
3. Preencha o checklist, marcando cada item como:
   - **Conforme**: Item está OK
   - **Não Conforme**: Item com problema (campos adicionais aparecem)
   - **N/A**: Não se aplica
4. Para itens não conformes, preencha os campos de falha e solução
5. Clique em "Salvar Progresso" para continuar depois ou "Finalizar Ordem" para concluir

### 3. Gerando Relatórios
1. Acesse a lista de planos
2. Clique em "PDF" ou "Excel" para exportar
3. O PDF abre em nova aba para visualização/impressão
4. O Excel é baixado automaticamente

## Arquitetura do Banco de Dados

### Principais Modelos
- **User**: Usuários do sistema (admin/executante)
- **Empresa**: Empresa raiz da hierarquia
- **Setor, Area, Conjunto, Subconjunto**: Níveis intermediários
- **Equipamento**: Equipamento final que recebe planos
- **PlanoInspecao**: Plano de inspeção do equipamento
- **ItemInspecao**: Itens do checklist
- **OrdemExecucao**: Ordem de trabalho gerada
- **ItemInspecaoApontado**: Resultado da execução

### Relacionamentos
- Cascata de exclusão em toda a hierarquia
- Relacionamento many-to-one entre níveis hierárquicos
- One-to-many entre planos e itens
- One-to-many entre ordens e apontamentos

## Variáveis de Ambiente

O sistema utiliza as seguintes variáveis de ambiente (já configuradas automaticamente):
- `DATABASE_URL`: URL de conexão com PostgreSQL
- `SESSION_SECRET`: Chave secreta para sessões Flask
- `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`: Credenciais do PostgreSQL

## Funcionalidades Implementadas Recentemente

### Geração Automática de Ordens
- Sistema de geração automática baseado em frequência do plano
- Cálculo inteligente de datas (por hora ou diário)
- Modal para seleção de executante
- Botão disponível na visualização de planos (apenas para administradores)

### Relatórios Avançados
- **Relatório de Ordem** (PDF/Excel): Exporta dados completos da execução
- **Relatório de Equipamento** (PDF): Visualização hierárquica com todos os planos
- Botões de exportação na visualização de ordens concluídas
- Formatação profissional com cores e badges

### Dashboard Aprimorado
- **Gráfico de Linha Temporal**: Evolução das inspeções (últimas 30 ordens)
- Comparação visual entre conformes e não conformes ao longo do tempo
- API de estatísticas com dados temporais
- Três gráficos interativos: Pizza (conformidade), Barras (status) e Linha (evolução)

## Melhorias Futuras Sugeridas

1. **Notificações**: Sistema de alertas para ordens pendentes
2. **Filtros Avançados**: Busca e filtro em todas as listas
3. **Dashboard Analítico**: Drill-down por empresa/setor/área
4. **Anexos**: Upload de fotos durante inspeção
5. **Assinatura Digital**: Registro de responsáveis
6. **API REST**: Para integração com outros sistemas
7. **Mobile**: Interface responsiva otimizada para tablets

## Estado Atual do Projeto

✅ CRUD completo para toda a hierarquia de equipamentos
✅ Sistema de autenticação e autorização
✅ Planos de inspeção com itens configuráveis
✅ Ordens de execução com checklist interativo
✅ Campos dinâmicos de não conformidade
✅ **Geração automática de ordens baseada em frequência**
✅ **Relatórios por ordem de execução (PDF/Excel)**
✅ **Relatórios por equipamento com hierarquia completa**
✅ **Gráfico de linha temporal mostrando evolução das inspeções**
✅ **Dashboard com estatísticas avançadas e análise temporal**
✅ Interface em português brasileiro
✅ Banco de dados PostgreSQL configurado
✅ Sistema rodando na porta 5000

## Última Atualização
06 de outubro de 2025
