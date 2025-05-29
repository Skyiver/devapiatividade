import os
from atividade_service.config import create_app
from atividade_service.controllers.atividade_controller import atividade_bp
from atividade_service.models.atividade import Atividade

app = create_app()
app.register_blueprint(atividade_bp, url_prefix='/api/atividades')

if __name__ == '__main__':
    porta = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=porta)