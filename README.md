# Steam Wishlist Tracker

Pipeline de dados que monitora sua lista de desejos da Steam e te avisa no Discord sempre que um jogo entra em promoção.

**Stack**: Python | SQLAlchemy | Supabase/Postgres | Discord Webhook | Steam API | UV

### Como funciona
1. *Extração*: Puxa todos os jogos da sua wishlist da Steam via `steamid` e salva raw em `apps_info.json`  
2. *Transformação*: Normaliza preços, nomes, desconto % e dados da loja  
3. *Load*: Conecta no Supabase via *SQLAlchemy* e armazena os dados tratados  
4. *Monitor*: Compara preços atuais com o banco. Se detectar promoção nova, salva os `appids` em `promo_ids.json`  
5. *Notificação*: Dispara webhook no Discord com os jogos em promoção e registra em `notified.json` pra não spammar  

### Rodando local

**1. Clone o projeto**  
git clone https://github.com/seuuser/steam-wishlist-tracker  
cd steam-wishlist-tracker  
  
**2. Instale dependências com UV**  
uv sync  
O UV gerencia o venv e instala tudo do `pyproject.toml` automaticamente.  

**3. Configure o .env**  
STEAM_ID=7656119xxxxxxxxxx  
STEAM_API_KEY=sua_key_aqui  
DATABASE_URL=postgresql://postgres:senha@db.xxxx.supabase.co:porta/postgres  
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxxxx  
  
**4. Execute**  
uv run python main.py  

### Estrutura
.  
├── main.py              # Orquestra o pipeline  
├── extract.py           # Puxa dados da Steam  
├── transform.py         # Limpa e formata  
├── load.py              # SQLAlchemy + upsert no Supabase  
├── notify.py            # Dispara Discord  
├── apps_info.json       # Cache raw da wishlist  
├── promo_ids.json       # Jogos em promoção detectados  
├── notified.json        # Controle de notificações enviadas  
├── pyproject.toml       # Dependências gerenciadas pelo UV  
└── .env.example         # Template de variáveis  

### Tech Stack
- *UV*: Gerenciamento de dependências e ambiente virtual
- *SQLAlchemy*: ORM pra conectar no Postgres/Supabase
- *psycopg2*: Driver PostgreSQL
- *requests*: Chamadas HTTP pra API da Steam e Discord
- *logging*: Logs estruturados do pipeline

### Funcionalidades
- **Sem spam**: Só notifica uma vez por jogo até o preço mudar de novo
- **Histórico**: Guarda preços no Supabase pra acompanhar variação
- **Webhook**: Embed do Discord com nome, preço antigo/novo, % desconto e link da loja
- **ORM**: SQLAlchemy facilita migrações e queries
- **Automático**: Roda sozinho via Actions
