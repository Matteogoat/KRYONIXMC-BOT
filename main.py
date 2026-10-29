import os, sys, discord, asyncio
from discord.ext import commands
from dotenv import load_dotenv
from datetime import timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

# 📡 SCUDO WEB SERVER PER L'HOSTING 24/7 SU RENDER
class KeepAlive(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"🟢 BOT DEFINTIVO ONLINE 24/7")

def run_web():
    port = int(os.environ.get("PORT", 8080))
    HTTPServer(('0.0.0.0', port), KeepAlive).serve_forever()

Thread(target=run_web, daemon=True).start()

print("⏳ Avvio motore definitivo...", flush=True)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    sys.exit(1)

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Memoria di stato e sicurezza interna del bot originale
bot.defcon_attivo = False
bot.bot_blacklist = []
bot.shadowban_list = []
bot.server_sicuro_id = None
bot.modalita_sicura_attiva = False
bot.violazioni_utenti = {}
bot.sponsor_db = {} # Struttura: {nome_lower: {"nome": str, "desc": str, "premi": int, "motivi": list}}

@bot.tree.interaction_check
async def global_interaction_check(interaction: discord.Interaction):
    if interaction.user.id in bot.bot_blacklist: return False
    if bot.defcon_attivo and not interaction.user.guild_permissions.administrator: return False
    return True

# 🛠️ TUTTI I TUOI COMANDI DI SICUREZZA ORIGINALI
@bot.command(name="defcon")
@commands.has_permissions(administrator=True)
async def cmd_defcon(ctx):
    bot.defcon_attivo = not bot.defcon_attivo
    stato = "🔴 ATTIVATO (Solo Admin)" if bot.defcon_attivo else "🟢 DISATTIVATO (Tutti)"
    await ctx.send(f"🚨 **STATO DEFCON MODIFICATO:** {stato}")

@bot.command(name="blacklist")
@commands.has_permissions(administrator=True)
async def cmd_blacklist(ctx, user: discord.User):
    if user.id not in bot.bot_blacklist:
        bot.bot_blacklist.append(user.id)
        await ctx.send(f"🔒 {user.mention} è stato aggiunto alla **Blacklist Globale** del bot.")
    else:
        await ctx.send("ℹ️ L'utente è già in blacklist.")

@bot.command(name="unblacklist")
@commands.has_permissions(administrator=True)
async def cmd_unblacklist(ctx, user: discord.User):
    if user.id in bot.bot_blacklist:
        bot.bot_blacklist.remove(user.id)
        await ctx.send(f"🔓 {user.mention} è stato rimosso dalla **Blacklist Globale**.")
    else:
        await ctx.send("❌ Utente non trovato in blacklist.")

@bot.command(name="shadowban")
@commands.has_permissions(administrator=True)
async def cmd_shadowban(ctx, user: discord.User):
    if user.id not in bot.shadowban_list:
        bot.shadowban_list.append(user.id)
        await ctx.send(f"👥 {user.mention} è stato inserito in **Shadowban**.")

@bot.command(name="unshadowban")
@commands.has_permissions(administrator=True)
async def cmd_unshadowban(ctx, user: discord.User):
    if user.id in bot.shadowban_list:
        bot.shadowban_list.remove(user.id)
        await ctx.send(f"✅ Rimossa modalità Shadowban per {user.mention}.")

@bot.command(name="modalitasicura")
@commands.has_permissions(administrator=True)
async def cmd_modalitasicura(ctx):
    bot.modalita_sicura_attiva = not bot.modalita_sicura_attiva
    stato = "🔒 ATTIVA" if bot.modalita_sicura_attiva else "🔓 DISATTIVATA"
    await ctx.send(f"🛡️ **MODALITÀ SICURA SERVER:** {stato}")

@bot.event
async def on_ready():
    print(f"✅ Sistema Centrale Connesso: {bot.user.name}", flush=True)
    try:
        from cogs.features import TicketView, TicketPersistentActions, SponsorListView
        bot.add_view(TicketView())
        bot.add_view(TicketPersistentActions())
        bot.add_view(SponsorListView(bot))
        print("🎫 Interfacce grafiche caricate in memoria.", flush=True)
    except Exception as e:
        print(f"⚠️ Errore caricamento interfacce: {e}", flush=True)
    try:
        await bot.tree.sync()
        print("📂 Registrazione comandi Slash completata.", flush=True)
    except Exception as e:
        print(f"⚠️ Errore sync comandi: {e}", flush=True)

@bot.event
async def on_message(message):
    if message.author.bot or not message.guild: return
    
    # Controllo Shadowban attivo
    if message.author.id in bot.shadowban_list:
        try: return await message.delete()
        except: pass

    # Anti-Raid: Controllo lunghezza testo
    if len(message.content) > 1400:
        try: return await message.delete()
        except: pass
        
    txt = message.content.lower()
    bad = ["cazzo", "merda", "stronzo", "vaffanculo", "troia", "puttana", "bastardo", "ucciditi", "muori", "negro", "handicappato", "autistico", "frocio", "coione", "shuttati", "ti ammazzo", "crepa", "deficiente"]
    
    # AutoMod sanzioni progressivo
    if any(p in txt for p in bad):
        try:
            await message.delete()
            uid = message.author.id
            bot.violazioni_utenti[uid] = bot.violazioni_utenti.get(uid, 0) + 1
            v = bot.violazioni_utenti[uid]
            if v >= 10:
                await message.guild.ban(message.author, reason="AutoMod: 10 violazioni.")
                await message.channel.send(f"🔨 {message.author.mention} è stato **BANNATO**.")
            elif v >= 6:
                await message.author.timeout(timedelta(days=1), reason="AutoMod: 6 violazioni.")
                await message.channel.send(f"🔇 {message.author.mention} è stato **MUTATO per 24 ore**.")
            elif v >= 3:
                await message.author.timeout(timedelta(hours=3), reason="AutoMod: 3 violazioni.")
                await message.channel.send(f"🔇 {message.author.mention} è stato **MUTATO per 3 ore**.")
            else:
                await message.channel.send(f"⚠️ {message.author.mention}, linguaggio non consentito! Infrazioni: `{v}/10`", delete_after=10)
            return
        except: pass
        
    # AutoMod filtri link ed inviti
    if "http://" in txt or "https://" in txt or "discord.gg/" in txt:
        if not any(d in txt for d in ["youtube.com", "tenor.com", "twitch.tv", "minecraft.net"]):
            try: return await message.delete()
            except: pass
            
    if message.author.id in bot.bot_blacklist: return
    await bot.process_commands(message)

async def main():
    async with bot:
        try:
            await bot.load_extension('cogs.features')
            print("📦 File cogs.features caricato.", flush=True)
        except Exception as e:
            print(f"❌ Errore caricamento cogs.features: {e}", flush=True)
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
