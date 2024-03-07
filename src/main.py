import os
import discord
from discord.ext import commands
from db import update_profile, insert_profile, get_profile
from rangos import verificar_rango
from exercises.A1 import generate_exercise

# configuracion del bot
prefix = "!"
token = os.environ.get('discord_token')

# Definir los intentos necesarios para el bot
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.reactions = True
intents.members = True

# Crear una instancia del bot con los intentos especificados
bot = commands.Bot(command_prefix=prefix, intents=intents)

# funciones

# funcion de enviar mensaje de bienvenida
async def send_welcome_message():
    """
    Envía un mensaje de bienvenida a todos los canales de texto en el servidor.
    """
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send("¡Hola! Soy un bot de práctica de inglés. Escribe `!ayuda` para obtener más información sobre cómo utilizar el bot.")

# evento de inicio
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await send_welcome_message()

# Comando !ayuda
@bot.command()
async def ayuda(ctx):
    """
    Muestra información sobre cómo utilizar el bot.
    """
    embed = discord.Embed(title="Comandos de Agustin",description="¡Bienvenido! Aquí tienes una lista de los comandos disponibles:", color=discord.Color.green())
    embed.add_field(name="!ayuda", value="Muestra información sobre cómo utilizar el bot.", inline=False)
    embed.add_field(name="!perfil", value="Muestra información sobre tu progreso y nivel de inglés.", inline=False)
    embed.add_field(name="!practicar", value="Inicia una sesión de práctica de inglés.", inline=False)
    embed.add_field(name="!evaluar", value="Evalúa tu nivel de inglés.", inline=False)
    embed.add_field(name="!A1", value="Muestra información sobre los temas del nivel Beginner.", inline=False)
    embed.add_field(name="!A2", value="Muestra información sobre los temas del nivel Basic.", inline=False)
    embed.add_field(name="!B1", value="Muestra información sobre los temas del nivel Intermediate.", inline=False)
    embed.add_field(name="!B2", value="Muestra información sobre los temas del nivel Upper Intermediate.", inline=False)
    embed.add_field(name="!C1", value="Muestra información sobre los temas del nivel Advanced.", inline=False)

    await ctx.send(embed=embed)



# Comando !perfil
@bot.command(name='perfil', help='Muestra el perfil del usuario')
async def perfil(ctx):
    user = ctx.message.author
    member = discord.utils.get(ctx.guild.members, id=user.id)
    experience_level = 0  # Por defecto 0
    english_rank = 'A1'  # Por defecto A1

    avatar_url = member.avatar.url
    username = f"{member.display_name} ({member.name})"  # Formato deseado del nombre

    # Guardar el perfil en la base de datos
    update_profile(user.id, username, avatar_url, experience_level, english_rank)

    # Crear el mensaje embed
    embed = discord.Embed(
        title=f"{username} Profile",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=avatar_url)
    embed.add_field(name="Nivel de Experiencia", value=experience_level, inline=True)
    embed.add_field(name="Rango de Inglés", value=english_rank, inline=True)

    await ctx.send(embed=embed)

# Comando !practicar
@bot.command(name='practicar', help='Inicia una sesión de práctica de inglés')
async def practicar(ctx):
    # Obtener el perfil del usuario
    user_id = str(ctx.author.id)
    profile = get_profile(user_id)

    # Verificar si el perfil existe
    if profile is None:
        await ctx.send("¡No se ha encontrado tu perfil! Por favor, crea un perfil utilizando el comando !perfil.")
        return

    # Obtener nivel y experiencia del usuario
    experience = profile[3]  # experiencia del usuario
    english_level = profile[4]  # nivel (A1, A2, B1, B2, C1, C2)

    # Verificar y actualizar el nivel del usuario en función de su experiencia
    await verificar_rango(ctx, user_id, experience)  # Se agregó ctx como argumento
    # Determinar los ejercicios según el nivel del usuario
    if english_level == "A1":
        #EJECUTAR FUNCION DE EJERCICIOS DE A1
        exercise = generate_exercise()
        question = exercise["question"]
        options = exercise["options"]
        correct_index = exercise["correct_answer"]
        
        # Construir el mensaje embed
        embed = discord.Embed(title="Práctica de Inglés - Nivel A1", description=question, color=discord.Color.blue())
        for idx, option in enumerate(options, start=1):
            embed.add_field(name="Respuesta", value=option, inline=False)
        
        # Enviar el mensaje embed y agregar reacciones
        message = await ctx.send(embed=embed)
        for idx in range(len(options)):
            await message.add_reaction(chr(0x1F1E6 + idx))
        
        # Función para verificar la respuesta del usuario
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in [chr(0x1F1E6 + i) for i in range(len(options))]
        
        try:
            reaction, _ = await bot.wait_for('reaction_add', timeout=30.0, check=check)
            selected_option_index = ord(reaction.emoji) - 0x1F1E6
            
            if selected_option_index == correct_index:
                await ctx.send("¡Respuesta correcta!")
            else:
                await ctx.send("Respuesta incorrecta. Inténtalo de nuevo.")
                await ctx.send(f"La respuesta correcta es: {options[correct_index]}")
        except TimeoutError:
            await ctx.send("Se agotó el tiempo para responder.")
    elif english_level == "A2":
        await ctx.send("todavia no hay ejercicios para este nivel")
    else:
        await ctx.send("¡El nivel de inglés de tu perfil es inválido! Por favor, contáctate con el soporte técnico.")
        return


# Conectar el bot al servidor de Discord
bot.run(token)
