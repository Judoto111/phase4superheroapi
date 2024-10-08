import pytest
from app import create_app, db
from app.models import Hero, Power, HeroPower

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            seed_data()
            yield client
            db.drop_all()

def seed_data():
    heroes = [
        Hero(name="Kamala Khan", super_name="Ms. Marvel"),
        Hero(name="Doreen Green", super_name="Squirrel Girl"),
        Hero(name="Gwen Stacy", super_name="Spider-Gwen"),
    ]
    powers = [
        Power(name="super strength", description="gives the wielder super-human strengths"),
        Power(name="flight", description="gives the wielder the ability to fly through the skies at supersonic speed"),
    ]
    db.session.add_all(heroes + powers)
    db.session.commit()

def test_get_heroes(client):
    response = client.get('/heroes')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 3

def test_get_hero_by_id(client):
    response = client.get('/heroes/1')
    assert response.status_code == 200
    assert response.json['name'] == "Kamala Khan"

def test_get_hero_by_id_not_found(client):
    response = client.get('/heroes/999')
    assert response.status_code == 404
    assert response.json['error'] == "Hero not found"

def test_get_powers(client):
    response = client.get('/powers')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 2

def test_get_power_by_id(client):
    response = client.get('/powers/1')
    assert response.status_code == 200
    assert response.json['name'] == "super strength"

def test_get_power_by_id_not_found(client):
    response = client.get('/powers/999')
    assert response.status_code == 404
    assert response.json['error'] == "Power not found"

def test_update_power_description(client):
    response = client.patch('/powers/1', json={"description": "Updated description with more than 20 characters"})
    assert response.status_code == 200
    assert response.json['description'] == "Updated description with more than 20 characters"

def test_update_power_description_fail(client):
    response = client.patch('/powers/1', json={"description": "Short"})
    assert response.status_code == 400
    assert "errors" in response.json

def test_create_hero_power(client):
    response = client.post('/hero_powers', json={"strength": "Strong", "power_id": 1, "hero_id": 2})
    assert response.status_code == 200
    assert response.json['strength'] == "Strong"

def test_create_hero_power_fail(client):
    response = client.post('/hero_powers', json={"strength": "Invalid", "power_id": 1, "hero_id": 2})
    assert response.status_code == 400
    assert "errors" in response.json
