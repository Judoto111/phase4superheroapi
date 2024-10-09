# Superheroes API

This is a Flask API to track superheroes and their powers.

## Features

- **Heroes:** Manage a list of heroes and their superpowers.
- **Powers:** Manage a list of powers and their descriptions.
- **Hero Powers:** Assign strengths to the heroes' powers.

## Endpoints

- `GET /heroes` - Get a list of all heroes.
- `GET /heroes/:id` - Get details of a specific hero.
- `GET /powers` - Get a list of all powers.
- `GET /powers/:id` - Get details of a specific power.
- `PATCH /powers/:id` - Update the description of a power.
- `POST /hero_powers` - Create a new hero power.

## Models

- **Hero**: Represents a superhero.
- **Power**: Represents a superpower.
- **HeroPower**: Represents the relationship between heroes and powers with an additional strength attribute.

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt

2. Run migrations:

   ```bash
   flask db upgrade

3. Start the server:

   ```bash
   flask run --port=5555
