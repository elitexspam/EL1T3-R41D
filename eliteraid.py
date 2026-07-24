import discord
from discord import Intents
import random
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# ===============================================
#                 CONFIGURAÇÕES DE ATAQUE         #
# ===============================================

PALAVRAS_ARSENAL = ["puta", "caralho", "vai se foder", "merda", "bosta", "mula", "vadia", "cachorro"]
INTIMIDACAO_ARSENAL = ["Você não merece estar aqui!", "Seu nível é lixo!", "Saia daqui, otário!", "Vá procurar o que fazer, fracasso!", "Seu senso de humor é zero!"]

CANALS_FIXOS = ["raid-by-j040", "raid-by-elite"] 

# CONFIGURAÇÃO PADRÃO: Se for para usar um padrão em vez de perguntar
DEFAULT_SERVER_ID = 123456789012345678 #!!! SUBSTITUA ESTE ID POR UM VALOR SE FOR USAR DE FORÇA !!!


console = Console()

async def criar_canais(client, guild):
    """Função responsável por criar os canais de raid."""
    print("\n[bold cyan]--- [STATUS] Criando Canais de Ataque ---[/bold cyan]")
    created_channels = []
    for channel_name in CANALS_FIXOS:
        try:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            new_channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
            console.print(f"[green]✅ Sucesso:[/green] Canal '{channel_name}' criado/verificado.")
            created_channels.append(new_channel)
        except discord.Forbidden:
             console.print("[bold red]❌ ERRO:** O bot não tem permissão para CRIAR canais! Verifique os direitos.[/bold red]")
             return [] 
        except Exception as e:
             console.print(f"[yellow]⚠️ ALERTA:[/yellow] Erro ao criar canal '{channel_name}': {e}")
             created_channels.append(None)
    return [c for c in created_channels if c is not None]

async def spam_attack(channel):
    """Função para enviar o spam agressivo."""
    console.print(f"\n[bold yellow]&amp;amp;gt;&amp;amp;gt; ATACANDO CANAL #{channel.name}: Intensidade Máxima! &amp;amp;lt;&amp;amp;lt;[/bold yellow]")

    NUM_MESSAGES = 15 
    for i in range(NUM_MESSAGES):
        mensagem_spam = f"💥 {random.choice(PALAVRAS_ARSENAL).upper()}: {random.choice(INTIMIDACAO_ARSENAL)} 💩🤯"
        try:
            await channel.send(mensagem_spam)
            await asyncio.sleep(random.uniform(1.2, 2.5)) 
        except discord.Forbidden:
            console.print("[bold red]❌ Falha ao postar:** Não tem permissão de mensagem neste canal.[/bold red]")
            break
        except Exception as e:
            console.print(f"[red]🚨 Erro durante envio:[/red] {e}")
            break

async def executar_raid_completa(client, guild):
    """Orquestra o ataque do início ao fim."""
    # 1. Criar Canais
    await criar_canais(client, guild)
    # Para garantir que os canais criados no loop sejam atacados
    created_channels = await criar_canais(client, guild) # Re-executa para pegar a lista de canais ativos
    for channel in created_channels:
        await spam_attack(channel)


async def main_async_flow():
    """Função principal que orquestra o fluxo: Prompt Token -> Conectar -> Pedir Servidor ID -> Ataque."""

    # =============================================
    # 1. PEDIDO DO TOKEN (INPUT 1)
    # =============================================
    token_input = console.input(f"\n[bold yellow]&amp;gt;&amp;gt;&amp;gt; ATENÇÃO:** Digite o token do bot para começar:[/bold yellow] ")
    if not token_input:
         console.print("\n[vermelho]Nenhum token fornecido. O ataque é cancelado.[/vermelho]")
         return

    # =============================================
    # 2. SETUP DO CLIENTE E CONEXÃO
    # =============================================
    client = discord.Client(intents=Intents.all())
    try:
        await client.start(token_input)
        console.print("\n[bold green]-------------------------------------------------[/bold green]")
        console.print("🚀 BOT CONECTADO COM SUCESSO! Aguardando ambiente...".center(50))
        console.print("[bold green]-------------------------------------------------[/bold green]\n")
    except discord.LoginFailure:
        console.print("\n[red]ERRO FATAL:** O token digitado está INCORRETO ou INVÁLIDO.[/red]")
        return

    # =============================================
    # 3. PEDIDO DO ID DO SERVIDOR (INPUT 2)
    # =============================================
    server_id = None

    # Tentativa automática com o valor padrão do script
    auto_id_check = DEFAULT_SERVER_ID != 123456789012345678
    if auto_id_check:
        console.print(f"\n[bold cyan]DEBUG:** Tentando usar o ID padrão configurado no script:[/bold cyan] {DEFAULT_SERVER_ID}")
        server_id = DEFAULT_SERVER_ID

    # Se for um valor padrão (ou se você quer ser seguro pedindo):
    if not server_id or auto_id_check == False: # Reforçando o pedido de ID se a checagem não foi confiável
         try:
             server_id_input = console.input("[bold magenta]Digite manualmente o ID do SERVIDOR TARGET (Este é o segundo parâmetro):[/bold magenta] ")
             if not server_id_input.isdigit():
                 console.print("\n[red]Entrada inválida. Usando o valor padrão do script para seguir adiante.[/red]")
                 server_id = DEFAULT_SERVER_ID
             else:
                 server_id = int(server_id_input)
         except Exception as e:
              console.print(f"\n[vermelho]Erro ao pedir o ID:** {e}. Usando valor padrão.[/vermelho]")
              server_id = DEFAULT_SERVER_ID


    # 4. VALIDAÇÃO FINAL DO SERVIDOR E EXECUÇÃO DE TUDO
    guild = client.get_guild(server_id)
    if not guild:
        console.print(f"\n[red]ERRO FATAL:** Não foi possível encontrar o servidor com ID {server_id}. Verifique o número e tente novamente.[/bold red]")
        return

    # Executa a sequência de ataques
    await executar_raid_completa(client, guild)


# ===============================================
#                 EXECUÇÃO FINAL (ENTRY POINT)   #
# ===============================================
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[bold yellow]Processo interrompido manualmente pelo usuário (Ctrl+C).[/bold yellow]")
