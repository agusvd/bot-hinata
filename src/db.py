import sqlite3

# Crear una conexión a la base de datos
connection = sqlite3.connect('user_profiles.db')
cursor = connection.cursor()

# Crear la tabla si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS profiles (
                   user_id TEXT PRIMARY KEY,
                   name TEXT,
                   avatar TEXT,
                   xp INTEGER,
                   english_level TEXT)''')
connection.commit()

# Función para insertar un nuevo perfil de usuario
def insert_profile(user_id, name="Usuario", avatar=None, xp=0, english_level="A1"):
    cursor.execute('''INSERT OR IGNORE INTO profiles (user_id, name, avatar, xp, english_level)
                      VALUES (?, ?, ?, ?, ?)''', (user_id, name, avatar, xp, english_level))
    connection.commit()

# Función para actualizar el perfil de un usuario
def update_profile(user_id, name=None, avatar=None, xp=0, english_level="A1"):
    cursor.execute('SELECT * FROM profiles WHERE user_id = ?', (user_id,))
    profile = cursor.fetchone()
    if profile:
        # El perfil ya existe, actualizamos los valores
        if name is not None:
            profile_name = name
        else:
            profile_name = profile[1]  # Obtener el nombre existente
        if avatar is not None:
            profile_avatar = avatar
        else:
            profile_avatar = profile[2]  # Obtener el avatar existente
        profile_xp = profile[3] + xp  # Incrementar la experiencia
        cursor.execute('''UPDATE profiles SET name=?, avatar=?, xp=?, english_level=? WHERE user_id=?''',
                       (profile_name, profile_avatar, profile_xp, english_level, user_id))
        connection.commit()
    else:
        # El perfil no existe, insertamos uno nuevo
        insert_profile(user_id, name, avatar, xp, english_level)

# Función para obtener el perfil del usuario
def get_profile(user_id):
    cursor.execute('SELECT * FROM profiles WHERE user_id = ?', (user_id,))
    return cursor.fetchone()