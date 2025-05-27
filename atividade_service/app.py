import os
from config import create_app, db
from controllers.atividade_controller import atividade_bp

app = create_app()
app.register_blueprint(atividade_bp, url_prefix='/api/atividades')

if __name__ == '__main__':
    porta = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=porta)