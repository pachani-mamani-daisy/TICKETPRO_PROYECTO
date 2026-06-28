from run import flask_app
from app.extensions import db
from app.models import Role, User

def crear_todo():
    with flask_app.app_context():
        admin_role = Role.query.filter_by(nombre='Admin').first()
        if not admin_role:
            admin_role = Role(nombre='Admin')
            db.session.add(admin_role)
        
        if not Role.query.filter_by(nombre='Cliente').first():
            db.session.add(Role(nombre='Cliente'))
        
        db.session.commit()

        user = User.query.filter_by(username='daisy_admin').first()
        if not user:
            user = User(username='daisy_admin', role=admin_role)
            user.set_password('admin123') 
            db.session.add(user)
            print("✅ Usuario 'daisy_admin' CREADO.")
        else:
            user.role = admin_role
            print("✅ Usuario 'daisy_admin' ya existía, ahora es ADMIN.")
        
        db.session.commit()

if __name__ == "__main__":
    crear_todo()
    print("🚀 PROCESO FINALIZADO CON ÉXITO")