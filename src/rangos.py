# Rangos de experiencia necesarios para avanzar de nivel
from db import get_profile, update_profile
import discord
from discord.ext import commands

EXPERIENCE_THRESHOLDS = {
    "A1": 1000,
    "A2": 2000,
    "B1": 3000,
    "B2": 4000,
    "C1": 5000,
    "C2": 6000
}

# Niveles de inglés disponibles
ENGLISH_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]


async def verificar_rango(ctx, user_id, experience):
    # Obtener el nivel actual del usuario
    profile = get_profile(user_id)
    current_level = profile[4]
    name = profile[1]

    # Verificar si la experiencia actual alcanza un umbral para avanzar de nivel
    for level, threshold in EXPERIENCE_THRESHOLDS.items():
        if experience >= threshold:
            current_level = level

    # Verificar si el nivel ha cambiado
    if current_level != profile[4]:
        # Enviar un mensaje indicando el nuevo rango
        new_level_message = f"{name}, has subido de nivel a {current_level}!"
        await ctx.send(new_level_message)  # Aquí se usa await para esperar la ejecución de send()
    else:
        # Enviar un mensaje indicando que no se ha subido de nivel
        no_level_up_message = f"{name}, todavía estás en el nivel `{current_level}`. Sigue practicando!"
        await ctx.send(no_level_up_message)  # Aquí también se usa await

    # Actualizar el nivel del usuario en la base de datos
    update_profile(user_id, english_level=current_level)