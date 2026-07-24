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

# --- CONFIGURAÇÕES CRÍTICAS (DEVE SER ALTERADO) ---
DEFAULT_SERVER_ID = 1148258814878036090 # !!! MUITO IMPORTANTE: SUBSTITUA POR ID REAL DO SEU SERVIDOR TARGET !!!


# Inicializa o console do Rich
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
    console.print(f"\n[bold yellow]&amp;gt;&amp;gt; ATACANDO CANAL #{channel.name}: Intensidade Máxima! &amp;lt;&amp;lt;[/bold yellow]")

    NUM_MESSAGES = 15 # Número de ataques/spam por canal
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

    # 1. Cria Canais
    console.print("\n[bold cyan]--- [PASSO 1/3] Iniciando criação de canais... ---[/bold cyan]")
    channels_alvos = await criar_canais(client, guild)
    if not channels_alvos:
        return # Interrompe se não conseguir criar canais

    # 2. Spam nos Canais criados
    console.print("\n[bold blue]--- [PASSO 2/3] Iniciando ataque de spam... ---[/bold blue]")
    for channel in channels_alvos:
        await spam_attack(channel)


async def main():
    """Função principal que orquestra a conexão, o prompt e o ataque."""

    # =============================================
    # 1. PEDIDO INTERATIVO DO TOKEN (A melhoria solicitada)
    # =============================================
    try:
        token_input = console.input(f"\n[bold yellow]>>> ATENÇÃO:** Por favor, digite o token do bot agora para começar:[/bold yellow] ")
        if not token_input:
             console.print("[red]Você não digitou nada de volta. O ataque será abortado.[/red]")
             return None

    except EOFError:
         print("\n[vermelho]Erro de leitura do terminal. Abortando.[/vermelho]")
         return None


    # =============================================
    # 2. INICIALIZAÇÃO DO CLIENTE E CONEXÃO
    # =============================================
    client = discord.Client(intents=Intents.all())

    try:
        print("\n[bold cyan]Conectando ao Discord com o token fornecido...[/bold cyan]")
        await client.start(token_input)
        console.print("[green]CONECTADO COM SUCESSO.[/green]\n")
    except discord.LoginFailure:
        console.print("\n[red]ERRO FATAL:** O token digitado está INCORRETO ou INVÁLIDO.[/bold red]")
        return

    # =============================================
    # 3. VERIFICAÇÃO DO SERVIDOR E EXECUÇÃO DA RAIDE
    # =============================================
    guild = client.get_guild(DEFAULT_SERVER_ID)
    if not guild:
        console.print(f"\n[red]ERRO FATAL:** Não foi possível encontrar o servidor com ID {DEFAULT_SERVER_ID}. Verifique o script![/red]")
        return

    # Executa a sequência de ataques
    await executar_raid_completa(client, guild)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[bold yellow]Processo manual encerrado pelo usuário (Ctrl+C).[/bold yellow]")
