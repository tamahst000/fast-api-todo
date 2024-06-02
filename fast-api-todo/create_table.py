from models import *
import db
import os


if __name__ == "__main__":
    path = SQLITE3_NAME
    if not os.path.isfile(path):

        Base.metadata.create_all(db.engine)

    admin = User(username="admin", password="fastapi", mail="hoge@example.com")
    db.session.add(admin)
    db.session.commit()

    task = Task(
        user_id=admin.id,
        content="太郎とランチ",
        deadline=datetime(2019, 10, 21, 12, 00, 00),
    )
    db.session.add(task)
    db.session.commit()

    db.session.close()
