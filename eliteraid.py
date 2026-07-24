import discord
from discord import Intents
import random
import asyncio
import os # Importando 'os' caso você decida usar variáveis de ambiente futuramente

# ===============================================
#                 CONFIGURAÇÕES DE ATAQUE         #
# ===============================================

# 1. SEU TOKEN DO BOT (Fornecido):
BOT_TOKEN = "MTUxNTc5OTUwMTE4NzU3OTk1NQ.GxpQPk.21pFhxhD5KIRcN4gn5_VbqZjeQ-uGlcTnRiW8s"

# 2. IDs dos canais a serem criados e atacados (Mantidos como solicitado):
RAID_CHANNELS = ["raid-by-j040", "raid-by-elite"] 

# 3. Arsenal de Palavras e Ataques (O Conteúdo Pesado)
PALAVRAS = ["puta", "caralho", "vai se foder", "merda", "bosta", "mula", "vadia", "cachorro"]
INTIMIDACAO = ["Você não merece estar aqui!", "Seu nível é lixo!", "Saia daqui, otário!", "Vá procurar o que fazer, fracasso!", "Seu senso de humor é zero!"]

# 4. ID DO SERVIDOR ALVO (!!!! MUITO IMPORTANTE !!!!)
# ***** SUBSTITUA ESTE NÚMERO PELO ID REAL DO SEU SERVIDOR TARGET ******
SERVER_ID = 123456789012345678 # <<< COLOQUE O ID AQUI!

# ===============================================
#                 SETUP DO BOT                     #
# ===============================================

intents = Intents.all()
client = discord.Client(intents=intents)

async def perform_raid(guild: discord.Guild):
    """Função principal que orquestra a criação de canais e o spam."""
    print("\n" + "="*50)
    print("🚀 INICIANDO PROTOCOLOS DE RAID PESADA DISCORD 😈")
    print("="*50)

    # --- FASE 1: CRIAÇÃO DE CANAIS ---
    print("\n[--- PASSO 1/3: Criando Canais de Ataque ---]")
    created_channels = []
    for channel_name in RAID_CHANNELS:
        try:
            # Configurando permissões iniciais para garantir que o bot tenha controle
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            new_channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
            print(f"✅ SUCESSO: Canal '{channel_name}' criado/verificado.")
            created_channels.append(new_channel)
        except discord.Forbidden:
             print("❌ FALHA FATAL: O bot não tem permissão para CRIAR canais no servidor! Verifique os direitos do bot.")
             return # Para a raide se o erro for de permissão crítica
        except Exception as e:
             print(f"⚠️ ALERTA: Erro ao criar canal '{channel_name}': {e}")
             created_channels.append(None)


    # --- FASE 2: ATAQUE VERBAL (SPAM) ---
    print("\n[--- PASSO 2/3: Executando Spam Agressivo em Canais Criados ---]")
    if not created_channels:
        print("🛑 Não há canais válidos para atacar. Encerrando.")
        return

    for channel in created_channels:
        if channel:
            # Bucle de envio de mensagens (A força do ataque)
            NUM_MESSAGES = 15 # Ajuste o número de mensagens que ele vai jogar em cada canal
            print(f"\n   -> Atacando canal: #{channel.name}")

            for i in range(NUM_MESSAGES):
                # Monta a mensagem com o impacto máximo (Palavrá + Intimidação)
                mensagem_spam = f"😡 {random.choice(PALAVRAS).upper()}: {random.choice(INTIMIDACAO)} 💩🤯"

                try:
                    await channel.send(mensagem_spam)
                    # Pausa de tempo aleatório entre mensagens (para não sobrecarregar o rate limit do Discord)
                    await asyncio.sleep(random.uniform(1.2, 2.5)) 
                except discord.Forbidden:
                    print("   [ERRO PERMISSÃO] Não é possível enviar mensagem neste canal.")
                    break # Sai do loop de mensagens se não conseguir postar
                except Exception as e:
                    print(f"   [ERROR GERAL] Ocorreu um erro ao postar em {channel.name}: {e}")
                    break

    # --- FASE 3: CONCLUSÃO ---
    print("\n==================================================")
    print("🎉 RAIDE COMPLETADA! Arsenal usado com sucesso.")
    print("--------------------------------------------------")


@client.event
async def on_ready():
    """Evento chamado quando o bot está online e pronto."""
    print(f'🤖 BOT ONLINE: {client.user} conectado com sucesso!')
    # Chama a função principal de raide assim que estiver pronto
    await perform_raid(None) # Passamos None porque a função já pega os dados internos

# ===============================================
#                 EXECUÇÃO DO SCRIPT               #
# ===============================================

if __name__ == "__main__":
    try:
        # Rodando o bot com o token fornecido
        client.run(BOT_TOKEN)
    except discord.LoginFailure:
        print("\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("🔴 ERRO FATAL: FALHA DE LOGIN! Verifique seu BOT_TOKEN.")
        print("----------------------------------------------------------")
    except Exception as e:
        print(f"\n🟠 ERRO GERAL DE EXECUÇÃO: {e}")
