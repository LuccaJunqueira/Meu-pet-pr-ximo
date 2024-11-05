from flask import Blueprint, render_template, redirect, url_for, flash
from ..db import get_db_connection
import requests

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('api.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM characters')
    characters = cursor.fetchall()
    cursor.close()
    conn.close()

    if not characters:
        flash("No characters found, click to load", "info")
    return render_template('index.html', characters=characters)

@main_bp.route('/load_data')
def load_data():
    if 'username' not in session:
        return redirect(url_for('api.login'))

    url = "https://rickandmortyapi.com/api/character"
    while url:
        response = requests.get(url).json()
        for char_data in response['results']:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM characters WHERE character_id = %s', (char_data['id'],))
            existing_character = cursor.fetchone()

            if not existing_character:
                cursor.execute('''INSERT INTO characters (character_id, name, status, species, gender, origin, location, image, episodes, url, created)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                               (char_data['id'], char_data['name'], char_data['status'], char_data['species'],
                                char_data['gender'], char_data['origin']['name'], char_data['location']['name'],
                                char_data['image'], ", ".join(char_data['episode']), char_data['url'], char_data['created']))
                conn.commit()
            cursor.close()
            conn.close()
        url = response.get('info', {}).get('next')

    flash("Data loaded successfully", "success")
    return redirect(url_for('main.index'))
