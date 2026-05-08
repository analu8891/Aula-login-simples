# Iniciando o alembic 

no terminal:
```bash 
python -m alembic init migrations 
```

# apagar o valor da linha 89 - no arquivo alembic.ini
deixe assim:

sqlalchemy.url =

# Edite o arquivo migrations/env.py 

from dotenv import load_dotenv
import os 
import database
from database import Base


load_dotenv()

config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

target_metadata = Base.metadata 

# Gere a migrations com autogenerate

```bash 
python -m alembic revision --autogenerate -m "Cria tabela usuario"
```

# aplicar a migrations 
```bash
python -m alembic upgrade head
```