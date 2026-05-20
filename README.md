# 🏢 Office Reserve — Sistema de Reservas de Mesas

> Sistema web em **Django** para gerenciar reservas de mesas em escritórios: mapa do escritório, reservas por usuário, proteção de horários e dashboard de ocupação.

---

## 🔥 Destaques
- Autenticação com usuários Django
- Mapa visual com posição de mesas (coordenadas)
- Bloqueio de conflitos: mesma mesa no mesmo intervalo e usuário não pode ter duas reservas simultâneas
- Dashboard com métricas diárias
- Código organizado por apps (`mesas`, `contas` / `accounts`)

---

## 📁 Estrutura do repositório (resumida)




office_reserve/

├─ office_reserve/       # settings, urls, wsgi

├─ contas/               # app de contas (login, cadastro, perfil)

├─ mesas/                # app de mesas e reservas (models, views, templates)

├─ templates/

├─ static/     

├─ README.md

└─ requirements.txt


## 🚀 Como rodar (local)

# clone
git clone https://github.com/Luiz-Carlos-A/office_reserve.git
cd office_reserve

# criar e ativar venv
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# instalar dependências
pip install -r requirements.txt

# migrations
python manage.py makemigrations
python manage.py migrate

# criar superuser (opcional)
python manage.py createsuperuser

# rodar servidor
python manage.py runserver
# abrir: http://127.0.0.1:8000/




## 🧩 Funcionalidades principais

* Cadastro e login de usuários
* Visualização do mapa do escritório com mesas posicionadas por coordenadas
* Criar / cancelar reservas com validação de conflitos
* Dashboard com: total de mesas, ocupadas, livres e reservas do dia
* Interface responsiva com Bootstrap



