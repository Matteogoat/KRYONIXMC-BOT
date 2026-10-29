import discord
from discord.ext import commands
from discord import app_commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 1. LANCIO DEL DADO
    @app_commands.command(name="dado", description="[FUN] Lancia un dado classico a 6 facce")
    async def dado(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"🎲 Risultato del dado: **{random.randint(1, 6)}**")

    # 2. TESTA O CROCE
    @app_commands.command(name="moneta", description="[FUN] Lancia una moneta (Testa o Croce)")
    async def moneta(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"🪙 La moneta cade su: **{random.choice(['TESTA', 'CROCE'])}**")

    # 3. PALLA 8 MAGICA
    @app_commands.command(name="8ball", description="[FUN] Fai una domanda sul tuo futuro alla sfera magica")
    async def eightball(self, interaction: discord.Interaction, domanda: str):
        risposte = [
            "🟢 Assolutamente sì!", "🟢 Le probabilità sono alte.", "🟡 Chiedimelo più tardi.",
            "🟡 Difficile dirlo ora.", "🔴 Assolutamente no.", "🔴 Le mie fonti dicono di no."
        ]
        await interaction.response.send_message(f"❓ **Domanda:** {domanda}\n🔮 **Risposta:** {random.choice(risposte)}")

    # 4. MISURATORE DI SIMPATIA
    @app_commands.command(name="rate", description="[FUN] Calcola quanto sei simpatico oggi da 0 a 100")
    async def rate(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"✨ Il radar dice che sei simpatico al **{random.randint(0, 100)}%** oggi!")

    # 5. INDOVINELLO RAPIDO
    @app_commands.command(name="indovinello", description="[FUN] Ti propone un indovinello casuale")
    async def indovinello(self, interaction: discord.Interaction):
        indovinelli = [
            ("Cosa ha le chiavi ma non apre le porte?", "Il pianoforte!"),
            ("Più ne togli, più diventa grande. Cos'è?", "Un buco nella sabbia!"),
            ("Cosa vola senza ali e piange senza occhi?", "La nuvola!")
        ]
        scelto = random.choice(indovinelli)
        await interaction.response.send_message(f"🧠 **Indovinello:** {scelto[0]}\n||Riposta: {scelto[1]}|| (Clicca sulla barra per barare!)")

    # 6. ABBRACCIO
    @app_commands.command(name="hug", description="[FUN] Invia un abbraccio virtuale a un utente della chat")
    async def hug(self, interaction: discord.Interaction, utente: discord.Member):
        await interaction.response.send_message(f"🤗 {interaction.user.mention} ha stretto in un forte abbraccio virtuale {utente.mention}!")

    # 7. SCHIAFFO CREATIVO
    @app_commands.command(name="slap", description="[FUN] Tira uno schiaffo amichevole a un utente")
    async def slap(self, interaction: discord.Interaction, utente: discord.Member):
        await interaction.response.send_message(f"💥 *Sbam!* {interaction.user.mention} ha tirato uno schiaffo virtuale a {utente.mention}!")

    # 8. GENERATORE DI INSULTI REALI DA MINECRAFT
    @app_commands.command(name="mc_meme", description="[FUN] Genera una battuta divertente sul mondo di Minecraft")
    async def mc_meme(self, interaction: discord.Interaction):
        battute = [
            "Sei così sfortunato che se scavi dritto cadi nella lava anche nel Nether.",
            "Il tuo stile nel costruire è così brutto che pure i Creeper si rifiutano di farti esplodere la casa.",
            "Hai meno riflessi di uno Zombie rimasto incastrato sotto una ragnatela.",
            "La tua spada in Nethelite infligge meno danni morali della tua mira con l'arco."
        ]
        await interaction.response.send_message(f"⛏️ **Meme MC:** {random.choice(battute)}")

    # 9. NUMERO CASUALE
    @app_commands.command(name="random_num", description="[FUN] Genera un numero a caso tra due valori scelti da te")
    async def random_num(self, interaction: discord.Interaction, minimo: int, massimo: int):
        if minimo >= massimo:
            await interaction.response.send_message("Il valore minimo deve essere più piccolo del massimo!", ephemeral=True)
            return
        await interaction.response.send_message(f"🔢 Numero estratto tra {minimo} e {massimo}: **{random.randint(minimo, massimo)}**")

    # 10. SCELTA RAPIDA
    @app_commands.command(name="scegli", description="[FUN] Fa scegliere al bot tra due opzioni indecisione")
    async def scegli(self, interaction: discord.Interaction, opzione1: str, opzione2: str):
        await interaction.response.send_message(f"🤔 Sono indeciso, ma scelgo sicuramente: **{random.choice([opzione1, opzione2])}**")

async def setup(bot):
    await bot.add_cog(Fun(bot))
