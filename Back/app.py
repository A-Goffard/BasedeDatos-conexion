from flask import Flask, jsonify, request
import sqlite3
from flask_cors import CORS
import os

app = Flask(__name__)
DATABASE = 'database.db'
CORS(app, resources={r"/*": {"origins": "http://localhost:8080", "methods": ["GET", "POST", "PUT", "DELETE"]}})

def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.OperationalError:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        with open('schema.sql') as f:
            conn.executescript(f.read())
        return conn


def get_db_connection():
    if not os.path.exists(DATABASE):
        raise sqlite3.OperationalError(f"Database file {DATABASE} does not exist.")
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return 'Hello, World!'

# Routes for Torneos
@app.route('/torneos', methods=['GET'])
def get_torneos():
    conn = get_db_connection()
    torneos = conn.execute('SELECT * FROM Torneos').fetchall()
    conn.close()
    return jsonify([dict(row) for row in torneos])

@app.route('/torneos/<int:torneo_id>', methods=['GET'])
def get_torneo(torneo_id):
    conn = get_db_connection()
    torneo = conn.execute('SELECT * FROM Torneos WHERE TorneoID = ?', (torneo_id,)).fetchone()
    conn.close()
    if torneo is None:
        return jsonify({'error': 'Torneo no encontrado'}), 404
    return jsonify(dict(torneo))

@app.route('/torneos', methods=['POST'])
def create_torneo():
    new_torneo = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO Torneos (Nombre, Ubicacion, FechaInicio, FechaFin) VALUES (?, ?, ?, ?)',
                 (new_torneo['Nombre'], new_torneo['Ubicacion'], new_torneo['FechaInicio'], new_torneo['FechaFin']))
    conn.commit()
    conn.close()
    return jsonify(new_torneo), 201

@app.route('/torneos/<int:torneo_id>', methods=['PUT'])
def update_torneo(torneo_id):
    updated_torneo = request.get_json()
    conn = get_db_connection()
    conn.execute('UPDATE Torneos SET Nombre = ?, Ubicacion = ?, FechaInicio = ?, FechaFin = ? WHERE TorneoID = ?',
                 (updated_torneo['Nombre'], updated_torneo['Ubicacion'], updated_torneo['FechaInicio'], updated_torneo['FechaFin'], torneo_id))
    conn.commit()
    conn.close()
    return jsonify(updated_torneo)

@app.route('/torneos/<int:torneo_id>', methods=['DELETE'])
def delete_torneo(torneo_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Torneos WHERE TorneoID = ?', (torneo_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Torneo eliminado'})

# Routes for Participantes
@app.route('/participantes', methods=['GET'])
def get_participantes():
    conn = get_db_connection()
    participantes = conn.execute('SELECT * FROM Participantes').fetchall()
    conn.close()
    return jsonify([dict(row) for row in participantes])

@app.route('/participantes/<int:participante_id>', methods=['GET'])
def get_participante(participante_id):
    conn = get_db_connection()
    participante = conn.execute('SELECT * FROM Participantes WHERE ParticipanteID = ?', (participante_id,)).fetchone()
    conn.close()
    if participante is None:
        return jsonify({'error': 'Participante no encontrado'}), 404
    return jsonify(dict(participante))

@app.route('/participantes', methods=['POST'])
def create_participante():
    new_participante = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO Participantes (Nombre, Edad, Nacionalidad, Genero) VALUES (?, ?, ?, ?)',
                 (new_participante['Nombre'], new_participante['Edad'], new_participante['Nacionalidad'], new_participante['Genero']))
    conn.commit()
    conn.close()
    return jsonify(new_participante), 201

@app.route('/participantes/<int:participante_id>', methods=['PUT'])
def update_participante(participante_id):
    updated_participante = request.get_json()
    conn = get_db_connection()
    conn.execute('UPDATE Participantes SET Nombre = ?, Edad = ?, Nacionalidad = ?, Genero = ? WHERE ParticipanteID = ?',
                 (updated_participante['Nombre'], updated_participante['Edad'], updated_participante['Nacionalidad'], updated_participante['Genero'], participante_id))
    conn.commit()
    conn.close()
    return jsonify(updated_participante)

@app.route('/participantes/<int:participante_id>', methods=['DELETE'])
def delete_participante(participante_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Participantes WHERE ParticipanteID = ?', (participante_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Participante eliminado'})

# Routes for Partidos
@app.route('/partidos', methods=['GET'])
def get_partidos():
    conn = get_db_connection()
    partidos = conn.execute('SELECT * FROM Partidos').fetchall()
    conn.close()
    return jsonify([dict(row) for row in partidos])

@app.route('/partidos/<int:partido_id>', methods=['GET'])
def get_partido(partido_id):
    conn = get_db_connection()
    partido = conn.execute('SELECT * FROM Partidos WHERE PartidoID = ?', (partido_id,)).fetchone()
    conn.close()
    if partido is None:
        return jsonify({'error': 'Partido no encontrado'}), 404
    return jsonify(dict(partido))

@app.route('/partidos', methods=['POST'])
def create_partido():
    new_partido = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO Partidos (TorneoID, Participante1ID, Participante2ID, Fecha) VALUES (?, ?, ?, ?)',
                 (new_partido.get('TorneoID'), new_partido['Participante1ID'], new_partido['Participante2ID'], new_partido['Fecha']))
    conn.commit()
    conn.close()
    return jsonify(new_partido), 201

@app.route('/partidos/<int:partido_id>', methods=['PUT'])
def update_partido(partido_id):
    updated_partido = request.get_json()
    conn = get_db_connection()
    conn.execute('UPDATE Partidos SET TorneoID = ?, Participante1ID = ?, Participante2ID = ?, Fecha = ? WHERE PartidoID = ?',
                 (updated_partido.get('TorneoID'), updated_partido['Participante1ID'], updated_partido['Participante2ID'], updated_partido['Fecha'], partido_id))
    conn.commit()
    conn.close()
    return jsonify(updated_partido)

@app.route('/partidos/<int:partido_id>', methods=['DELETE'])
def delete_partido(partido_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Partidos WHERE PartidoID = ?', (partido_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Partido eliminado'})

# Routes for Sponsors
@app.route('/sponsors', methods=['GET'])
def get_sponsors():
    conn = get_db_connection()
    sponsors = conn.execute('SELECT * FROM Sponsors').fetchall()
    conn.close()
    return jsonify([dict(row) for row in sponsors])

@app.route('/sponsors/<int:sponsor_id>', methods=['GET'])
def get_sponsor(sponsor_id):
    conn = get_db_connection()
    sponsor = conn.execute('SELECT * FROM Sponsors WHERE SponsorID = ?', (sponsor_id,)).fetchone()
    conn.close()
    if sponsor is None:
        return jsonify({'error': 'Sponsor no encontrado'}), 404
    return jsonify(dict(sponsor))

@app.route('/sponsors', methods=['POST'])
def create_sponsor():
    new_sponsor = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO Sponsors (Nombre) VALUES (?)',
                 (new_sponsor['Nombre'],))
    conn.commit()
    conn.close()
    return jsonify(new_sponsor), 201

@app.route('/sponsors/<int:sponsor_id>', methods=['PUT'])
def update_sponsor(sponsor_id):
    updated_sponsor = request.get_json()
    conn = get_db_connection()
    conn.execute('UPDATE Sponsors SET Nombre = ? WHERE SponsorID = ?',
                 (updated_sponsor['Nombre'], sponsor_id))
    conn.commit()
    conn.close()
    return jsonify(updated_sponsor)

@app.route('/sponsors/<int:sponsor_id>', methods=['DELETE'])
def delete_sponsor(sponsor_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Sponsors WHERE SponsorID = ?', (sponsor_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Sponsor eliminado'})

# Routes for Jugador_Sponsor
@app.route('/jugador_sponsors', methods=['GET'])
def get_jugador_sponsors():
    conn = get_db_connection()
    jugador_sponsors = conn.execute('SELECT * FROM Jugador_Sponsor').fetchall()
    conn.close()
    return jsonify([dict(row) for row in jugador_sponsors])

@app.route('/jugador_sponsors/<int:jugador_id>/<int:sponsor_id>', methods=['GET'])
def get_jugador_sponsor(jugador_id, sponsor_id):
    conn = get_db_connection()
    jugador_sponsor = conn.execute('SELECT * FROM Jugador_Sponsor WHERE JugadorID = ? AND SponsorID = ?', (jugador_id, sponsor_id)).fetchone()
    conn.close()
    if jugador_sponsor is None:
        return jsonify({'error': 'Relación jugador-sponsor no encontrada'}), 404
    return jsonify(dict(jugador_sponsor))

@app.route('/jugador_sponsors', methods=['POST'])
def create_jugador_sponsor():
    new_jugador_sponsor = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO Jugador_Sponsor (JugadorID, SponsorID) VALUES (?, ?)',
                 (new_jugador_sponsor['JugadorID'], new_jugador_sponsor['SponsorID']))
    conn.commit()
    conn.close()
    return jsonify(new_jugador_sponsor), 201

@app.route('/jugador_sponsors/<int:jugador_id>/<int:sponsor_id>', methods=['DELETE'])
def delete_jugador_sponsor(jugador_id, sponsor_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Jugador_Sponsor WHERE JugadorID = ? AND SponsorID = ?', (jugador_id, sponsor_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Relación jugador-sponsor eliminada'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

