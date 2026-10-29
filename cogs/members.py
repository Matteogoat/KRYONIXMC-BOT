import discord
from discord.ext import commands
from discord import app_commands

class Members(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 1. STATUS MC
    @app_commands.command(name="mcstatus", description="Mostra lo stato del server Minecraft")
    async def mcstatus(self, interaction: discord.Interaction):
        await interaction.response.send_message("🎮 **Server Minecraft:** `mc.kryonixmc.it` | 🟢 Online e pronto!")

    # 2. USERINFO
    @app_commands.command(name="userinfo", description="Mostra le informazioni sul tuo profilo")
    async def userinfo(self, interaction: discord.Interaction, utente: discord.Member = None):
        target = utente or interaction.user
        await interaction.response.send_message(f"👤 Account di **{target.name}** creato il: {target.created_at.strftime('%d/%m/%Y')}")

    # 3. SERVERINFO
    @app_commands.command(name="serverinfo", description="Mostra le informazioni sul server Discord")
    async def serverinfo(self, interaction: discord.Interaction):
        g = interaction.guild
        await interaction.response.send_message(f"🏰 **{g.name}** | Membri totali: `{g.member_count}` | Creato il: {g.created_at.strftime('%d/%m/%Y')}")

    # 4. AVATAR
    @app_commands.command(name="avatar", description="Mostra la foto profilo di un utente")
    async def avatar(self, interaction: discord.Interaction, utente: discord.Member = None):
        target = utente or interaction.user
        await interaction.response.send_message(f"🖼️ Ecco l'avatar di {target.name}: {target.display_avatar.url}")

    # 5. LINKS
    @app_commands.command(name="links", description="Mostra i link utili del server")
    async def links(self, interaction: discord.Interaction):
        await interaction.response.send_message("🌐 **Sito Web:** https://tuoserver.it\n🛒 **Store:** https://tuoserver.it")

    # 6. PIPPO (TEST PING)
    @app_commands.command(name="ping", description="Controlla la latenza del bot")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"🏓 Pong! Latenza: `{round(self.bot.ws.ping * 1000)}ms`")

    # 7. HELP MEMBRI
    @app_commands.command(name="help_utility", description="Mostra la lista dei comandi membri")
    async def help_utility(self, interaction: discord.Interaction):
        await interaction.response.send_message("📚 **Comandi membri attivi:** `/mcstatus`, `/userinfo`, `/serverinfo`, `/avatar`, `/links`, `/ping`, `/report`")

    # 8. REPORT SYSTEM
    @app_commands.command(name="report", description="Segnala un utente o un bug allo staff")
    async def report(self, interaction: discord.Interaction, segnalazione: str):
        await interaction.response.send_message("✅ Grazie! La tua segnalazione è stata inviata allo Staff con successo.", ephemeral=True)
        log_channel = discord.utils.get(interaction.guild.text_channels, name="logs-staff")
        if log_channel:
            await log_channel.send(f"📩 **Nuovo Report da {interaction.user.mention}:** {segnalazione}")

    # 9. IP MC
    @app_commands.command(name="ip", description="Mostra l'ip del server Minecraft da copiare")
    async def ip(self, interaction: discord.Interaction):
        await interaction.response.send_message("📌 IP per entrare nel server: `mc.kryonixmc.it` (Versione Java/Bedrock)")

    # 10. REGOLE
    @app_commands.command(name="regolamento", description="Mostra il link o il sommario del regolamento")
    async def regolamento(self, interaction: discord.Interaction):
        await interaction.response.send_message("📜 Ricordati di rispettare le regole del network consultabili nel canale apposito!")

async def setup(bot):
    await bot.add_cog(Members(bot))
