from src.users.infrastructure.MySqlUserRepository import MySqlUserRepository
from src.users.application.UserCreator import UserCreator
from src.contact.infraestructure.MySqlContactRepository import MySqlContactRepository
from src.users.domain.User import User

from src.contact.infraestructure.orm.ContactModel import ContactModel
from src.users.infrastructure.orm.UserModel import UserModel
from src.schedules.infrastructure.orm.ScheduleModel import ScheduleModel
from src.notifications.infrastructure.orm.NotificationModel import NotificationModel
from src.Activities.infraestructure.orm.ActivitiesModel import ActivitiesModel
from src.payments.infrastructure.orm.PaymentModel import PaymentModel
from src.schedules.infrastructure.orm.ScheduleItemModel import ScheduleItemModel

def test_create_user_integration(db_session):
    # Repositorios
    user_repository = MySqlUserRepository(db_session)
    contact_repository = MySqlContactRepository(db_session)

    # Simula un contacto válido
    contact = ContactModel(id=1, email="221255@ids.upchiapas.edu.mx",phone="9611234567")
    db_session.add(contact)
    db_session.commit()

    # Servicio de creación de usuarios
    user_creator = UserCreator(user_repository, contact_repository)

    # Ejecuta la creación del usuario
    contact_id = contact.id
    username = "testuser"
    email = "test@example.com"
    password = "password123"

    user_creator.create(contact_id, username, email, password)

    # Verifica que el usuario fue guardado
    saved_user = db_session.query(UserModel).filter_by(username=username).first()

    assert saved_user is not None
    assert saved_user.username == username
    assert saved_user.email == email
    assert saved_user.password == password

    assert saved_user.schedules is not None
    assert saved_user.notifications is not None

    