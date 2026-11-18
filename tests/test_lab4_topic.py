from flask_login.test_client import FlaskLoginClient
from flaskbb.forum.models import Topic


def client_for(application, user):
    """Хелпер для создания тестового клиента с авторизованным пользователем"""
    application.test_client_class = FlaskLoginClient
    application.config["WTF_CSRF_ENABLED"] = False
    return application.test_client(user=user)


def test_create_topic_success(application, user, forum):
    """
    Задача 1: Тест проверяет обычный (успешный) случай создания темы.
    Ожидаемый результат: статус 302 (редирект после успешного создания)
    и появление темы в базе данных.
    """
    client = client_for(application, user)

    url = f"/{forum.id}-{forum.slug}/topic/new"

    response = client.post(
        url,
        data={"title": "Тестовая тема", "content": "Тестовое сообщение."},
        follow_redirects=True,
    )

    assert response.status_code == 200

    topic = Topic.query.filter_by(title="Тестовая тема").first()
    assert topic is not None
    assert topic.forum_id == forum.id


def test_create_topic_validation_error(application, user, forum):
    """
    Задача 2: Тест проверяет ошибку/граничное значение (пустой заголовок темы).
    Ожидаемый результат: тема не создается, модель Topic остается пустой.
    """
    client = client_for(application, user)

    url = f"/{forum.id}-{forum.slug}/topic/new"

    response = client.post(
        url, data={"title": "", "content": "Текст есть, заголовка нет."}, follow_redirects=True
    )

    assert response.status_code == 200

    topic_count = Topic.query.filter_by(forum_id=forum.id).count()
    assert topic_count == 0
