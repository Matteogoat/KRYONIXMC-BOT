import discord
from discord.ext import commands
from discord import app_commands

class TicketPersistentActions(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Reclama 👔", style=discord.ButtonStyle.blurple, custom_id="btn_claim_tk_f")
    async def claim_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, name="[ 🔒 ]staff") or discord.utils.get(interaction.guild.roles, name="Staff")
        if role and role not in interaction.user.roles and not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ Solo lo Staff può reclamare questo ticket.", ephemeral=True)
        await interaction.channel.edit(name=f"gestito-{interaction.user.name.lower()}")
        if role: await interaction.channel.set_permissions(role, read_messages=True, send_messages=False)
        await interaction.channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await interaction.response.send_message(f"👔 Ticket preso in carico da {interaction.user.mention}.")

    @discord.ui.button(label="Chiama Staff 🔔", style=discord.ButtonStyle.green, custom_id="btn_call_staff_f")
    async def call_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, name="[ 🔒 ]staff") or discord.utils.get(interaction.guild.roles, name="Staff")
        mention_text = role.mention if role else "@everyone"
        await interaction.channel.send(f"🔔 {mention_text} Assistenza urgente richiesta da {interaction.user.mention}!")
        await interaction.response.send_message("✅ Staff sollecitato.", ephemeral=True)

    @discord.ui.button(label="Blocca Chat ❄️", style=discord.ButtonStyle.grey, custom_id="btn_lock_tk_f")
    async def lock_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, name="[ 🔒 ]staff") or discord.utils.get(interaction.guild.roles, name="Staff")
        if role and role not in interaction.user.roles and not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ No permessi.", ephemeral=True)
        await interaction.response.send_message("❄️ Chat bloccata temporaneamente dallo Staff.")

    @discord.ui.button(label="Chiudi 🔒", style=discord.ButtonStyle.red, custom_id="btn_close_tk_f")
    async def close_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, name="[ 🔒 ]staff") or discord.utils.get(interaction.guild.roles, name="Staff")
        if role and role not in interaction.user.roles and not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ No permessi.", ephemeral=True)
        await interaction.channel.delete()

class TicketModal(discord.ui.Modal, title="Compila la Richiesta"):
    def __init__(self, categoria: str):
        super().__init__()
        self.categoria = categoria
        self.descrizione = discord.ui.TextInput(label="Descrizione richiesta", style=discord.TextStyle.long, required=True, max_length=400)
        self.add_item(self.descrizione)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild, member = interaction.guild, interaction.user
        overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False), member: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True), guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)}
        role = discord.utils.get(guild.roles, name="[ 🔒 ]staff") or discord.utils.get(guild.roles, name="Staff")
        if role: overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        try:
            channel = await guild.create_text_channel(name=f"{self.categoria}-{member.name.lower()}", overwrites=overwrites)
            embed = discord.Embed(title=f"🎫 TICKET APERTO • {self.categoria.upper()}", color=0x2ecc71)
            embed.description = f"Benvenuto, {member.mention}.\n\n📌 **Richiesta:**\n*{self.descrizione.value}*\n\nUsa i bottoni sottostanti per gestire il supporto. Storico ticket su <#1562123701166809108>."
            await channel.send(embed=embed, view=TicketPersistentActions())
            await interaction.followup.send(f"✅ Ticket creato: {channel.mention}", ephemeral=True)
        except: await interaction.followup.send("❌ Errore permessi canale.", ephemeral=True)

class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label="Candidature Staff", emoji="👔", value="candidatura"), discord.SelectOption(label="Segnalazioni Staff", emoji="👮", value="segnalazione"), discord.SelectOption(label="Segnalazione Bug", emoji="🐛", value="bug"), discord.SelectOption(label="Info Generali", emoji="❓", value="info"), discord.SelectOption(label="Altro", emoji="✨", value="altro")]
        super().__init__(placeholder="Scegli il motivo...", min_values=1, max_values=1, custom_id="sel_tk_f_v2")
    async def callback(self, interaction: discord.Interaction): await interaction.response.send_modal(TicketModal(self.values))

class TicketView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None); self.add_item(TicketSelect())

# 🎛️ MODAL INTERATTIVI PER I PULSANTI DELLA LISTA SPONSOR
class SponsorAddModal(discord.ui.Modal, title="Aggiungi Nuovo Sponsor"):
    def __init__(self, bot): super().__init__(); self.bot = bot
    nome = discord.ui.TextInput(label="Nome dello Sponsor", placeholder="Es: MyHosting", required=True)
    desc = discord.ui.TextInput(label="Descrizione / Offerta", style=discord.TextStyle.long, placeholder="Descrivi lo sponsor qui...", required=True)
    async def on_submit(self, interaction: discord.Interaction):
        self.bot.sponsor_db[self.nome.value.lower()] = {"nome": self.nome.value, "desc": self.desc.value, "premi": 0, "motivi": []}
        await interaction.response.send_message(f"✅ Sponsor **{self.nome.value.upper()}** aggiunto alla memoria!", ephemeral=True)

class SponsorDelModal(discord.ui.Modal, title="Rimuovi uno Sponsor"):
    def __init__(self, bot): super().__init__(); self.bot = bot
    nome = discord.ui.TextInput(label="Nome dello Sponsor da eliminare", placeholder="Scrivi il nome esatto", required=True)
    async def on_submit(self, interaction: discord.Interaction):
        if self.nome.value.lower() in self.bot.sponsor_db:
            del self.bot.sponsor_db[self.nome.value.lower()]
            await interaction.response.send_message(f"🗑️ Sponsor **{self.nome.value.upper()}** rimosso con successo!", ephemeral=True)
        else: await interaction.response.send_message("❌ Sponsor non trovato.", ephemeral=True)

class SponsorListView(discord.ui.View):
    def __init__(self, bot): super().__init__(timeout=None); self.bot = bot
    @discord.ui.button(label="Aggiungi Sponsor ➕", style=discord.ButtonStyle.green, custom_id="btn_sp_add_list")
    async def add_sp(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.administrator: return await interaction.response.send_message("❌ Solo amministratori.", ephemeral=True)
        await interaction.response.send_modal(SponsorAddModal(self.bot))
    @discord.ui.button(label="Elimina Sponsor 🗑️", style=discord.ButtonStyle.red, custom_id="btn_sp_del_list")
    async def del_sp(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.administrator: return await interaction.response.send_message("❌ Solo amministratori.", ephemeral=True)
        await interaction.response.send_modal(SponsorDelModal(self.bot))

class SponsorPremiaModal(discord.ui.Modal, title="Premia lo Sponsor (Level Up)"):
    def __init__(self, bot, nome_sp): super().__init__(); self.bot = bot; self.nome_sp = nome_sp
    motivo = discord.ui.TextInput(label="Motivo del Premio", style=discord.TextStyle.long, placeholder="Scrivi il motivo del riconoscimento...", required=True)
    async def on_submit(self, interaction: discord.Interaction):
        sp = self.bot.sponsor_db[self.nome_sp]
        sp["premi"] += 1
        sp["motivi"].append(self.motivo.value)
        livello = "💎 UFFICIALE (LEVEL UP!)" if sp["premi"] >= 3 else f"⭐ Livello {sp['premi']}"
        emb = discord.Embed(title="🎉 PREMIAZIONE SPONSOR • LEVEL UP", color=0xf1c40f)
        emb.description = f"Lo Sponsor **{sp['nome'].upper()}** è stato premiato da {interaction.user.mention}!\n\n**Motivo:** {self.motivo.value}\n\n📊 **Stato Aggiornato:** {livello} `({sp['premi']}/3 Premi)`"
        await interaction.response.send_message(embed=emb)

class FeaturesCog(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = discord.utils.get(member.guild.text_channels, name="👋│welcome") or discord.utils.get(member.guild.text_channels, name="benvenuto")
        if channel:
            embed = discord.Embed(title=f"📥 UN NUOVO UTENTE È ENTRATO NEL NETWORK! 📥", description=f"Benvenuto nel server ufficiale di **KryonixMC**, {member.mention}!\n\n👑 **Cosa fare adesso per iniziare:**\n▪️ Leggi attentamente tutte le nostre regole ufficiali nel canale <#1562123316402069634> per evitare sanzioni.\n▪️ Resta aggiornato sui canali degli annunci.\n▪️ Interagisci con la nostra community nelle chat pubbliche!", color=0x3498db)
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.add_field(name="📅 Creazione Account:", value=f"`{member.created_at.strftime('%d/%m/%Y')}`", inline=True)
            embed.add_field(name="📊 Obiettivo Membri:", value=f"`{len(member.guild.members)}/1000`", inline=True)
            embed.set_footer(text=f"KryonixMC Network • Membro #{len(member.guild.members)}")
            await channel.send(content=f"👋 Benvenuto {member.mention}!", embed=embed)

    @app_commands.command(name="setup_ticket", description="Genera l'embed iniziale dei ticket.")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_ticket(self, interaction: discord.Interaction):
        embed = discord.Embed(title="🎫 CENTRO SUPPORTO UTENTI", description="Seleziona la categoria dal menu in basso per aprire un ticket privato.\n\nPer le regole generali visita <#1562123701166809108>.", color=0xe74c3c)
        await interaction.response.send_message("Pannello inviato.", ephemeral=True)
        await interaction.channel.send(embed=embed, view=TicketView())

    @app_commands.command(name="partner", description="Invia una Partnership.")
    @app_commands.checks.has_permissions(administrator=True)
    async def partner(self, interaction: discord.Interaction, testo: str):
        embed = discord.Embed(title="🤝 NUOVA PARTNERSHIP UFFICIALE", description=testo, color=0x9b59b6)
        await interaction.response.send_message("✅ Partnership pubblicata.", ephemeral=True)
        await interaction.channel.send(embed=embed)

    # 💎 STRUTTURA DEI 3 COMANDI SPONSOR COMPLETA E POTENZIATA
    sponsor_group = app_commands.Group(name="sponsor", description="Gestione Sponsor del Network")

    @sponsor_group.command(name="lista", description="Mostra gli sponsor e permette la gestione immediata tramite pulsanti.")
    async def sponsor_lista(self, interaction: discord.Interaction):
        if not self.bot.sponsor_db:
            embed = discord.Embed(title="💎 SPONSOR UFFICIALI", description="Nessuno sponsor attivo in memoria.", color=0xf1c40f)
            return await interaction.response.send_message(embed=embed, view=SponsorListView(self.bot))
        embed = discord.Embed(title="💎 SPONSOR UFFICIALI DEL NETWORK", color=0xf1c40f)
        for k, v in self.bot.sponsor_db.items():
            status = "👑 [SPONSOR UFFICIALE EXCLUSIVE]" if v["premi"] >= 3 else f"⭐ Sponsor Standard (Premi: `{v['premi']}/3`)"
            embed.add_field(name=f"▪️ {v['nome'].upper()}", value=f"**Stato:** {status}\n**Offerta:** {v['desc']}", inline=False)
        await interaction.response.send_message(embed=embed, view=SponsorListView(self.bot))

    @sponsor_group.command(name="premia", description="Premia uno sponsor e aumenta il suo legame (3 premi = Sponsor Ufficiale)")
    @app_commands.checks.has_permissions(administrator=True)
    async def sponsor_premia(self, interaction: discord.Interaction, nome: str):
        if nome.lower() not in self.bot.sponsor_db: return await interaction.response.send_message("❌ Sponsor non trovato.", ephemeral=True)
        await interaction.response.send_modal(SponsorPremiaModal(self.bot, nome.lower()))

    @sponsor_group.command(name="osserva", description="Controlla lo stato dettagliato e lo storico premi di uno sponsor.")
    async def sponsor_osserva(self, interaction: discord.Interaction, nome: str):
        if nome.lower() not in self.bot.sponsor_db: return await interaction.response.send_message("❌ Sponsor non trovato.", ephemeral=True)
        sp = self.bot.sponsor_db[nome.lower()]
        status = "👑 UFFICIALE (Massimo Livello raggiunto!)" if sp["premi"] >= 3 else f"⭐ Base (`{sp['premi']}/3` Premi per il Level Up)"
        embed = discord.Embed(title=f"🔎 ANALISI COMMERCIALS • {sp['nome'].upper()}", color=0x34495e)
        embed.add_field(name="📋 Descrizione:", value=sp["desc"], inline=False)
        embed.add_field(name="📊 Grado di Partnership:", value=status, inline=True)
        motivi_txt = "\n".join([f"- {m}" for m in sp["motivi"]]) if sp["motivi"] else "Nessun premio registrato."
        embed.add_field(name="📜 Storico Riconoscimenti / Premi:", value=motivi_txt, inline=False)
        await interaction.response.send_message(embed=embed)

    @sponsor_group.command(name="tagga", description="Invia la proclamazione speciale sul canale Best Partnership of the Month.")
    @app_commands.checks.has_permissions(administrator=True)
    async def sponsor_tagga(self, interaction: discord.Interaction, nome: str):
        if nome.lower() not in self.bot.sponsor_db: return await interaction.response.send_message("❌ Sponsor non trovato.", ephemeral=True)
        sp = self.bot.sponsor_db[nome.lower()]
        target_ch = interaction.guild.get_channel(1563241410059182250)
        if not target_ch: return await interaction.response.send_message("❌ Impossibile trovare il canale speciale delle premiazioni.", ephemeral=True)
        embed = discord.Embed(title="🏆 BEST PARTNERSHIP OF THE MONTH 🏆", description=f"Siamo orgogliosi di proclamare **{sp['nome'].upper()}** come la migliore collaborazione di questo mese!\n\nUn ringraziamento speciale per il supporto continuo dato al server.", color=0xe91e63)
        embed.set_footer(text="Amministrazione KryonixMC Network")
        await target_ch.send(embed=embed)
        await interaction.response.send_message("🏆 Proclamazione mensile inviata correttamente nel canale speciale!", ephemeral=True)

async def setup(bot): await bot.add_cog(FeaturesCog(bot))
