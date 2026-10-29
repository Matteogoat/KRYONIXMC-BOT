import discord
from discord.ext import commands
from discord import app_commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 1. LOCKDOWN SERVER
    @app_commands.command(name="admin_lockdown", description="[👑 ADMIN] Chiude il server in emergenza")
    @app_commands.default_permissions(administrator=True)
    async def admin_lockdown(self, interaction: discord.Interaction):
        ev = interaction.guild.default_role
        p = ev.permissions
        p.update(send_messages=False, connect=False)
        await ev.edit(permissions=p)
        await interaction.response.send_message("🚨 **SERVER SIGILLATO DA UN AMMINISTRATORE!**")

    # 2. UNLOCKDOWN SERVER
    @app_commands.command(name="admin_unlock", description="[👑 ADMIN] Riapre il server dopo un lockdown")
    @app_commands.default_permissions(administrator=True)
    async def admin_unlock(self, interaction: discord.Interaction):
        ev = interaction.guild.default_role
        p = ev.permissions
        p.update(send_messages=True, connect=True)
        await ev.edit(permissions=p)
        await interaction.response.send_message("✅ **SERVER RIAPERTO CON SUCCESSO!**")

    # 3. CREATE ROLE
    @app_commands.command(name="admin_createrole", description="[👑 ADMIN] Crea un ruolo nel server")
    @app_commands.default_permissions(administrator=True)
    async def admin_createrole(self, interaction: discord.Interaction, nome: str, colore_hex: str = "FFFFFF"):
        try: col = discord.Color(int(colore_hex, 16))
        except: col = discord.Color.default()
        await interaction.guild.create_role(name=nome, color=col)
        await interaction.response.send_message(f"✅ Ruolo `{nome}` creato.")

    # 4. DELETE ROLE
    @app_commands.command(name="admin_deleterole", description="[👑 ADMIN] Elimina un ruolo")
    @app_commands.default_permissions(administrator=True)
    async def admin_deleterole(self, interaction: discord.Interaction, ruolo: discord.Role):
        await ruolo.delete()
        await interaction.response.send_message(f"❌ Ruolo `{ruolo.name}` eliminato.")

    # 5. CREATE TEXT CHANNEL
    @app_commands.command(name="admin_create_text", description="[👑 ADMIN] Crea un canale testuale")
    @app_commands.default_permissions(administrator=True)
    async def admin_create_text(self, interaction: discord.Interaction, nome: str):
        await interaction.guild.create_text_channel(name=nome)
        await interaction.response.send_message(f"📝 Canale `#{nome}` creato.")

    # 6. CREATE VOICE CHANNEL
    @app_commands.command(name="admin_create_voice", description="[👑 ADMIN] Crea un canale vocale")
    @app_commands.default_permissions(administrator=True)
    async def admin_create_voice(self, interaction: discord.Interaction, nome: str):
        await interaction.guild.create_voice_channel(name=nome)
        await interaction.response.send_message(f"🔊 Canale vocale `{nome}` creato.")

    # 7. DELETE CHANNEL
    @app_commands.command(name="admin_delete_channel", description="[👑 ADMIN] Elimina il canale attuale")
    @app_commands.default_permissions(administrator=True)
    async def admin_delete_channel(self, interaction: discord.Interaction):
        await interaction.response.send_message("💣 Eliminazione...", ephemeral=True)
        await interaction.channel.delete()

    # 8. MASS MUTE (VOCALE)
    @app_commands.command(name="admin_massmute", description="[👑 ADMIN] Muta tutti nel tuo canale vocale")
    @app_commands.default_permissions(administrator=True)
    async def admin_massmute(self, interaction: discord.Interaction):
        if not interaction.user.voice:
            return await interaction.response.send_message("Devi essere in un vocale!", ephemeral=True)
        await interaction.response.defer()
        for m in interaction.user.voice.channel.members:
            if m != interaction.user and not m.bot: await m.edit(mute=True)
        await interaction.followup.send("🔇 Membri nel vocale mutati.")

    # 9. MASS UNMUTE (VOCALE)
    @app_commands.command(name="admin_massunmute", description="[👑 ADMIN] Smuta tutti nel tuo canale vocale")
    @app_commands.default_permissions(administrator=True)
    async def admin_massunmute(self, interaction: discord.Interaction):
        if not interaction.user.voice:
            return await interaction.response.send_message("Devi essere in un vocale!", ephemeral=True)
        await interaction.response.defer()
        for m in interaction.user.voice.channel.members:
            await m.edit(mute=False)
        await interaction.followup.send("🔊 Membri nel vocale smutati.")

    # 10. SET BOT NAME
    @app_commands.command(name="admin_setbotname", description="[👑 ADMIN] Cambia il nome del bot")
    @app_commands.default_permissions(administrator=True)
    async def admin_setbotname(self, interaction: discord.Interaction, nuovo_nome: str):
        await self.bot.user.edit(username=nuovo_nome)
        await interaction.response.send_message(f"🤖 Nome bot aggiornato in `{nuovo_nome}`.")

    # 11. DIAGNOSTICA SERVER
    @app_commands.command(name="admin_serverstats", description="[👑 ADMIN] Diagnostica profonda")
    @app_commands.default_permissions(administrator=True)
    async def admin_serverstats(self, interaction: discord.Interaction):
        g = interaction.guild
        emb = discord.Embed(title="📊 Diagnostica Rete", color=0x000000)
        emb.add_field(name="Canali", value=f"Testuali: {len(g.text_channels)} | Vocali: {len(g.voice_channels)}")
        await interaction.response.send_message(embed=emb)

    # 12. PURGE BOTS
    @app_commands.command(name="admin_purge_bots", description="[👑 ADMIN] Caccia tutti i bot esterni falsi")
    @app_commands.default_permissions(administrator=True)
    async def admin_purge_bots(self, interaction: discord.Interaction):
        await interaction.response.defer()
        espulsi = 0
        for m in interaction.guild.members:
            if m.bot and m.id != self.bot.user.id:
                await m.kick(reason="Purge automatico dei bot.")
                espulsi += 1
        await interaction.followup.send(f"🤖 Rimosso {espulsi} bot esterni.")

    # 13. MASS SLOWMODE
    @app_commands.command(name="admin_mass_slowmode", description="[👑 ADMIN] Slowmode su tutti i canali")
    @app_commands.default_permissions(administrator=True)
    async def admin_mass_slowmode(self, interaction: discord.Interaction, secondi: int):
        await interaction.response.defer()
        for ch in interaction.guild.text_channels:
            await ch.edit(slowmode_delay=secondi)
        await interaction.followup.send(f"⏳ Slowmode a {secondi}s impostata globalmente.")

    # 14. ADMIN EMBED SAY
    @app_commands.command(name="admin_embed_say", description="[👑 ADMIN] Invia annuncio embed in un canale")
    @app_commands.default_permissions(administrator=True)
    async def admin_embed_say(self, interaction: discord.Interaction, canale: discord.TextChannel, titolo: str, testo: str):
        import discord
        emb = discord.Embed(title=titolo, description=testo, color=discord.Color.dark_red())
        await canale.send(embed=emb)
        await interaction.response.send_message("💥 Inviato.", ephemeral=True)

    # 15. LEAVE SERVER
    @app_commands.command(name="admin_bot_leave", description="[👑 ADMIN] Forza il bot ad andarsene")
    @app_commands.default_permissions(administrator=True)
    async def admin_bot_leave(self, interaction: discord.Interaction):
        await interaction.response.send_message("👋 Addio...", ephemeral=True)
        await interaction.guild.leave()

async def setup(bot):
    await bot.add_cog(Admin(bot))
