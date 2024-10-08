from flask import Blueprint, jsonify, request, abort
from . import db
from .models import Hero, Power, HeroPower
from .validations import validate_hero_power_strength, validate_power_description

main_bp = Blueprint('main', __name__)

@main_bp.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([{"id": hero.id, "name": hero.name, "super_name": hero.super_name} for hero in heroes])

@main_bp.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    return jsonify({
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "hero_powers": [{
            "id": hp.id,
            "strength": hp.strength,
            "power_id": hp.power_id,
            "hero_id": hp.hero_id,
            "power": {
                "id": hp.power.id,
                "name": hp.power.name,
                "description": hp.power.description
            }
        } for hp in hero.hero_powers]
    })

@main_bp.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([{"id": power.id, "name": power.name, "description": power.description} for power in powers])

@main_bp.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify({"id": power.id, "name": power.name, "description": power.description})

@main_bp.route('/powers/<int:id>', methods=['PATCH'])
def update_power_description(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    try:
        validate_power_description(data['description'])
        power.description = data['description']
        db.session.commit()
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400

    return jsonify({"id": power.id, "name": power.name, "description": power.description})

@main_bp.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    try:
        validate_hero_power_strength(data['strength'])
        hero_power = HeroPower(
            strength=data['strength'],
            hero_id=data['hero_id'],
            power_id=data['power_id']
        )
        db.session.add(hero_power)
        db.session.commit()
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400

    return jsonify({
        "id": hero_power.id,
        "hero_id": hero_power.hero_id,
        "power_id": hero_power.power_id,
        "strength": hero_power.strength,
        "hero": {
            "id": hero_power.hero.id,
            "name": hero_power.hero.name,
            "super_name": hero_power.hero.super_name
        },
        "power": {
            "id": hero_power.power.id,
            "name": hero_power.power.name,
            "description": hero_power.power.description
        }
    })
