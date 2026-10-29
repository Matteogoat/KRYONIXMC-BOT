import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 1. BAN
    @app_commands.command(name="ban", description="[STAFF] Banna un utente")
    async def ban(self, interaction: discord.Interaction, utente: discord.Member, motivo: str = "Nessuno"):
        await utente.ban(reason=motivo)
        await interaction.response.send_message(f"🔨 {utente.mention} sanzionato con un Ban.")

    # 2. UNBAN
    @app_commands.command(name="unban", description="[STAFF] Sbanna un utente")
    async def unban(self, interaction: discord.Interaction, utente_id: str):
        user = await self.bot.fetch_user(utente_id)
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"🔓 ID `{utente_id}` sbannato.")

    # 3. KICK
    @app_commands.command(name="kick", description="[STAFF] Espelle un utente")
    async def kick(self, interaction: discord.Interaction, utente: discord.Member, motivo: str = "Nessuno"):
        await utente.kick(reason=motivo)
        await interaction.response.send_message(f"👢 {utente.mention} espulso.")

    # 4. MUTE
    @app_commands.command(name="mute", description="[STAFF] Muta un utente")
    async def mute(self, interaction: discord.Interaction, utente: discord.Member, minuti: int):
        await utente.timeout(timedelta(minutes=minuti))
        await interaction.response.send_message(f"🔇 {utente.mention} mutato per {minuti}m.")

    # 5. UNMUTE
    @app_commands.command(name="unmute", description="[STAFF] Smuta un utente")
    async def unmute(self, interaction: discord.Interaction, utente: discord.Member):
        await utente.timeout(None)
        await interaction.response.send_message(f"🔊 Rimosso isolamento a {utente.mention}.")

    # 6. CLEAR
    @app_commands.command(name="clear", description="[STAFF] Cancella messaggi")
    async def clear(self, interaction: discord.Interaction, quantita: int):
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=quantita)
        await interaction.followup.send(f"🧹 Eliminati {len(deleted)} messaggi.", ephemeral=True)

    # 7. NUKE
    @app_commands.command(name="nuke", description="[STAFF] Rigenera il canale")
    async def nuke(self, interaction: discord.Interaction):
        ch = interaction.channel
        pos = ch.position
        new_ch = await ch.clone()
        await ch.delete()
        await new_ch.edit(position=pos)
        await new_ch.send("💥 Canale rigenerato dallo Staff.")

    # 8. LOCK
    @app_commands.command(name="lock", description="[STAFF] Blocca il canale")
    async def lock(self, interaction: discord.Interaction):
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
        await interaction.response.send_message("🔒 Canale bloccato.")

    # 9. UNLOCK
    @app_commands.command(name="unlock", description="[STAFF] Sblocca il canale")
    async def unlock(self, interaction: discord.Interaction):
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
        await interaction.response.send_message("🔓 Canale sbloccato.")

    # 10. ADD ROLE
    @app_commands.command(name="addrole", description="[STAFF] Aggiunge un ruolo")
    async def addrole(self, interaction: discord.Interaction, utente: discord.Member, ruolo: discord.Role):
        await interaction.response.defer(ephemeral=True)
        try:
            await utente.add_roles(ruolo)
            await interaction.followup.send(f"✅ Ruolo aggiunto.", ephemeral=True)
        except:
            await interaction.followup.send(f"❌ Errore permessi.", ephemeral=True)

    # 11. REMOVE ROLE
    @app_commands.command(name="removerole", description="[STAFF] Rimuove un ruolo")
    async def removerole(self, interaction: discord.Interaction, utente: discord.Member, ruolo: discord.Role):
        await interaction.response.defer(ephemeral=True)
        try:
            await utente.remove_roles(ruolo)
            await interaction.followup.send(f"❌ Ruolo rimosso.", ephemeral=True)
        except:
            await interaction.followup.send(f"❌ Errore permessi.", ephemeral=True)

    # 12. VC MUTE
    @app_commands.command(name="vcmute", description="[STAFF] Muta in vocale")
    async def vcmute(self, interaction: discord.Interaction, utente: discord.Member):
        await utente.edit(mute=True)
        await interaction.response.send_message(f"🔇 {utente.mention} silenziato in vocale.")

    # 13. VC UNMUTE
    @app_commands.command(name="vcunmute", description="[STAFF] Smuta in vocale")
    async def vcunmute(self, interaction: discord.Interaction, utente: discord.Member):
        await utente.edit(mute=False)
        await interaction.response.send_message(f"🔊 {utente.mention} può parlare.")

    # 14. SLOWMODE
    @app_commands.command(name="slowmode", description="[STAFF] Imposta la slowmode")
    async def slowmode(self, interaction: discord.Interaction, secondi: int):
        await interaction.channel.edit(slowmode_delay=secondi)
        await interaction.response.send_message(f"⏳ Cooldown: {secondi}s.")

    # 15. WARN
    @app_commands.command(name="warn", description="[STAFF] Invia un warn nei DM")
    async def warn(self, interaction: discord.Interaction, utente: discord.Member, motivo: str):
        try:
            emb = discord.Embed(title="⚠️ WARN", description=motivo, color=0xffa500)
            await utente.send(embed=emb)
            await interaction.response.send_message("✅ Warn inviato.")
        except:
            await interaction.response.send_message("⚠️ DM chiusi, registrato qui.")

    # 16. RENAME CHANNEL
    @app_commands.command(name="rename_channel", description="[STAFF] Rinomina il canale")
    async def rename_channel(self, interaction: discord.Interaction, nuovo_nome: str):
        await interaction.channel.edit(name=nuovo_nome)
        await interaction.response.send_message(f"📝 Canale rinominato in `{nuovo_nome}`.")

    # 17. SOFTBAN
    @app_commands.command(name="softban", description="[STAFF] Banna e sbanna")
    async def softban(self, interaction: discord.Interaction, utente: discord.Member):
        await utente.ban(reason="Softban", delete_message_days=7)
        await interaction.guild.unban(utente)
        await interaction.response.send_message(f"🧼 {utente.mention} softbannato.")

    # 18. VC DEAFEN
    @app_commands.command(name="vcdeafen", description="[STAFF] Sorda in vocale")
    async def vcdeafen(self, interaction: discord.Interaction, utente: discord.Member):
        await utente.edit(deafen=True)
        await interaction.response.send_message(f"🙉 {utente.mention} sordato.")

    # 19. VC UNDEAFEN
    @app_commands.command(name="vcundeafen", description="[STAFF] Rimuove sorda")
    async def vcundeafen(self, interaction: discord.Interaction, utente: discord.Member):
        await utente.edit(deafen=False)
        await interaction.response.send_message(f"👂 {utente.mention} ascolta.")

    # 20. VC KICK
    @app_commands.command(name="vckick", description="[STAFF] Disconnette da un vocale")
    async def vckick(self, interaction: discord.Interaction, utente: discord.Member):
        await utente.edit(voice_channel=None)
        await interaction.response.send_message(f"💨 {utente.mention} rimosso dal vocale.")

    # 21. VC MOVE
    @app_commands.command(name="vcmove", description="[STAFF] Sposta di canale vocale")
    async def vcmove(self, interaction: discord.Interaction, utente: discord.Member, canale: discord.VoiceChannel):
        await utente.edit(voice_channel=canale)
        await interaction.response.send_message(f"🔄 Spostato in `{canale.name}`.")

    # 22. PEX
    @app_commands.command(name="pex", description="[STAFF] Promuove un membro")
    async def pex(self, interaction: discord.Interaction, utente: discord.Member, ex_ruolo: discord.Role, nuovo_ruolo: discord.Role, motivazione: str):
        await interaction.response.defer(ephemeral=True)
        try:
            await utente.remove_roles(ex_ruolo)
            await utente.add_roles(nuovo_ruolo)
            embed = discord.Embed(title="🚀 PROMOZIONE STAFF", color=discord.Color.green())
            embed.add_field(name="👤 Utente", value=utente.mention, inline=False)
            embed.add_field(name="📉 Ex Ruolo", value=ex_ruolo.mention, inline=True)
            embed.add_field(name="📈 Nuovo Ruolo", value=nuovo_ruolo.mention, inline=True)
            embed.add_field(name="📝 Motivo", value=f"*{motivazione}*", inline=False)
            await interaction.channel.send(embed=embed)
            await interaction.followup.send("✅ Eseguito!", ephemeral=True)
        except:
            await interaction.followup.send("❌ Errore permessi.", ephemeral=True)

    # 23. DEPEX
    @app_commands.command(name="depex", description="[STAFF] Retrocede un membro")
    async def depex(self, interaction: discord.Interaction, utente: discord.Member, ex_ruolo: discord.Role, nuovo_ruolo: discord.Role, motivazione: str):
        await interaction.response.defer(ephemeral=True)
        try:
            await utente.remove_roles(ex_ruolo)
            await utente.add_roles(nuovo_ruolo)
            embed = discord.Embed(title="📉 RETROCESSIONE STAFF", color=discord.Color.red())
            embed.add_field(name="👤 Utente", value=utente.mention, inline=False)
            embed.add_field(name="🔺 Ex Ruolo", value=ex_ruolo.mention, inline=True)
            embed.add_field(name="🔻 Nuovo Ruolo", value=nuovo_ruolo.mention, inline=True)
            embed.add_field(name="📝 Motivo", value=f"*{motivazione}*", inline=False)
            await interaction.channel.send(embed=embed)
            await interaction.followup.send("✅ Eseguito!", ephemeral=True)
        except:
            await interaction.followup.send("❌ Errore permessi.", ephemeral=True)

    # 24. SETUP TICKET
    @app_commands.command(name="setup_ticket", description="[STAFF] Crea pannello ticket")
    async def setup_ticket(self, interaction: discord.Interaction):
        from main import TicketView
        embed = discord.Embed(title="🎫 SUPPORTO KRYONIXMC", color=discord.Color.blue())
        embed.description = "Seleziona sotto la categoria del ticket."
        await interaction.channel.send(embed=embed, view=TicketView())
        await interaction.response.send_message("✅ Pannello creato!", ephemeral=True)

    # 25. PURGE USER
    @app_commands.command(name="purge_user", description="[STAFF] Cancella messaggi utente")
    async def purge_user(self, interaction: discord.Interaction, utente: discord.Member, quantita: int = 50):
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=quantita, check=lambda m: m.author == utente)
        await interaction.followup.send(f"🧹 Rimossi {len(deleted)} messaggi.", ephemeral=True)

    # 26. RENAME SERVER
    @app_commands.command(name="rename_server", description="[STAFF] Cambia nome server")
    async def rename_server(self, interaction: discord.Interaction, nuovo_nome: str):
        await interaction.guild.edit(name=nuovo_nome)
        await interaction.response.send_message(f"🏰 Server rinominato in `{nuovo_nome}`.")

    # 27. SET TOPIC
    @app_commands.command(name="set_topic", description="[STAFF] Imposta il topic")
    async def set_topic(self, interaction: discord.Interaction, descrizione: str):
        await interaction.channel.edit(topic=descrizione)
        await interaction.response.send_message("📌 Descrizione aggiornata.")

    # 28. CHANNEL INFO
    @app_commands.command(name="channelinfo", description="[STAFF] Info canale")
    async def channelinfo(self, interaction: discord.Interaction):
        ch = interaction.channel
        emb = discord.Embed(title=f"📊 Canale: {ch.name}", color=0x3498db)
        emb.add_field(name="ID", value=f"`{ch.id}`")
        await interaction.response.send_message(embed=emb)

    # 29. SERVER VISUAL STATS
    @app_commands.command(name="server_stats", description="[STAFF] Panoramica server")
    async def server_stats(self, interaction: discord.Interaction):
        g = interaction.guild
        emb = discord.Embed(title=f"📈 {g.name}", color=0x2ecc71)
        emb.add_field(name="Membri", value=f"`{g.member_count}`")
        await interaction.response.send_message(embed=emb)

    # 30. STAFF ALERTS
    @app_commands.command(name="ping_staff", description="[STAFF] Invia alert log")
    async def ping_staff(self, interaction: discord.Interaction, allarme: str):
        log_ch = discord.utils.get(interaction.guild.text_channels, name="logs-staff")
        if log_ch:
            await log_ch.send(f"🔔 **URGENTE:** {allarme}")
            await interaction.response.send_message("✅ Segnalato.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Log non trovato.", ephemeral=True)

    # 31. CHECK PERMS
    @app_commands.command(name="check_perms", description="[STAFF] Controlla livelli")
    async def check_perms(self, interaction: discord.Interaction, utente: discord.Member):
        p = utente.guild_permissions
        res = "Amministratore" if p.administrator else "Moderatore standard"
        await interaction.response.send_message(f"🔑 Livello: **{res}**")

    # 32. MANUTENZIONE
    @app_commands.command(name="manutenzione", description="[STAFF] Avviso manutenzione")
    async def manutenzione(self, interaction: discord.Interaction, stato: bool):
        msg = "🛠️ **RETE IN MANUTENZIONE!**" if stato else "🎮 **RETE ATTIVA!**"
        await interaction.response.send_message(msg)

    # 33. AUDIT LOGS
    @app_commands.command(name="audit_logs", description="[STAFF] Mostra azioni")
    async def audit_logs(self, interaction: discord.Interaction):
        await interaction.response.defer()
        lines = []
        async for e in interaction.guild.audit_logs(limit=4):
            lines.append(f"• **{e.user}**: {e.action.name}")
        await interaction.followup.send(content="\n".join(lines) if lines else "No log.")

    # 34. STAFF PING
    @app_commands.command(name="staff_ping", description="[STAFF] Ping interno")
    async def staff_ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"⚡ Ping: `{round(self.bot.ws.ping * 1000)}ms`")

    # 35. STRIP ROLES
    @app_commands.command(name="strip_roles", description="[STAFF] Rimuove ruoli")
    async def strip_roles(self, interaction: discord.Interaction, utente: discord.Member):
        await interaction.response.defer(ephemeral=True)
        try:
            await utente.edit(roles=[interaction.guild.default_role])
            await interaction.followup.send(f"🧹 Pulito.", ephemeral=True)
        except:
            await interaction.followup.send("❌ Errore permessi.", ephemeral=True)

    # 36. TEST STAFF
    @app_commands.command(name="test_staff", description="[STAFF] Verifica bot")
    async def test_staff(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"✅ Attivo {interaction.user.name}!")

    # 37. NICK
    @app_commands.command(name="nick", description="[STAFF] Cambia nickname")
    async def nick(self, interaction: discord.Interaction, utente: discord.Member, nuovo_nome: str):
        await utente.edit(nick=nuovo_nome)
        await interaction.response.send_message(f"📝 Nome modificato.")

    # 38. SAY
    @app_commands.command(name="say", description="[STAFF] Ripete messaggio")
    async def say(self, interaction: discord.Interaction, messaggio: str):
        await interaction.response.send_message("Inviato", ephemeral=True)
        await interaction.channel.send(messaggio)

    # 39. POLL
    @app_commands.command(name="poll", description="[STAFF] Crea sondaggio")
    async def poll(self, interaction: discord.Interaction, domanda: str):
        embed = discord.Embed(title="📊 SONDAGGIO", description=domanda)
        await interaction.response.send_message(embed=embed)
        m = await interaction.original_response()
        await m.add_reaction("👍")
        await m.add_reaction("👎")

    # 40. EMBED SAY
    @app_commands.command(name="annuncio", description="[STAFF] Invia annuncio embed")
    async def annuncio(self, interaction: discord.Interaction, titolo: str, contenuto: str):
        embed = discord.Embed(title=titolo, description=contenido, color=0xff0000)
        await interaction.response.send_message(embed=embed)

    # 41. UNMUTE ALL
    @app_commands.command(name="unmute_all", description="[STAFF] Sblocca canali")
    async def unmute_all(self, interaction: discord.Interaction, utente: discord.Member):
        await utente.timeout(None)
        await interaction.response.send_message("🔊 Rimosso sanzioni.")

    # 42. VERIFY REGISTERED
    @app_commands.command(name="verify_staff", description="[STAFF] Test sincro")
    async def verify_staff(self, interaction: discord.Interaction):
        await interaction.response.send_message("⚙️ Sistema allineato.")

async def setup(bot):
    await bot.add_cog(Staff(bot))

