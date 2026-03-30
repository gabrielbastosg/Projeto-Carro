🚗 Car Explorer

Sistema web desenvolvido com Django para explorar, comparar e analisar carros com base em custo-benefício.

🧠 Sobre o projeto

O Car Explorer permite que usuários naveguem por uma lista de carros, filtrem por diferentes critérios e comparem veículos para encontrar a melhor opção com base em desempenho, consumo e preço.

O projeto também conta com um sistema de favoritos e cálculo automático de score para auxiliar na tomada de decisão.

⚙️ Funcionalidades
🔎 Explorar carros com filtros
📊 Cálculo automático de score (custo-benefício)
⚖️ Comparação entre múltiplos carros
❤️ Sistema de favoritos
📄 Página de detalhes do carro
📌 Paginação de resultados
🌙 Modo escuro (dark mode)
🧮 Lógica de Score

O score dos carros é calculado com base na seguinte fórmula:

score = potencia / (consumo * preco)

Onde:

Maior potência → melhor
Menor consumo → melhor
Menor preço → melhor
🛠️ Tecnologias utilizadas
Python
Django
HTML5
CSS3
JavaScript
Bootstrap
🚀 Como rodar o projeto
# Clonar o repositório
git clone https://github.com/gabrielbastosg/Projeto-Carro

# Entrar na pasta
cd Projeto-Carro

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Windows)
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Rodar servidor
python manage.py runserver

📈 Status do projeto

✔️ Funcionalidades principais completas (MVP)
🚧 Melhorias futuras em andamento

🔮 Melhorias futuras
Sistema de login e cadastro
API com Django REST Framework
Frontend com React
Dashboard com gráficos
Sistema de recomendação inteligente
👨‍💻 Autor

Desenvolvido por Gabriel Bastos
Projeto com foco em aprendizado e evolução em desenvolvimento web com Django.