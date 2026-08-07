import os
import time
import subprocess

import discord
from discord.ext import commands
from groq import Groq

# ==========================
# CONFIG
# ==========================


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GITHUB_USERNAME = "lazuu22"
REPO_NAME = "generated-websites"

client = Groq(api_key=GROQ_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# ==========================
# READY
# ==========================

@bot.event
async def on_ready():
    print("=" * 40)
    print(f"Logged in as {bot.user}")
    print("Lazuu AI is online!")
    print("=" * 40)


# ==========================
# PING
# ==========================

@bot.command()
async def ping(ctx):
    await ctx.send(
        f"🏓 Pong! {round(bot.latency * 1000)} ms"
    )


# ==========================
# HELP
# ==========================

@bot.command()
async def helpme(ctx):

    embed = discord.Embed(
        title="🤖 Lazuu AI",
        description="AI Website Generator",
        color=0x00ffff
    )

    embed.add_field(
        name="Commands",
        value="""
!make birthday website

!make hacker portfolio

!make jarvis dashboard

!ping
""",
        inline=False
    )

    await ctx.send(embed=embed)


# ==========================
# MAKE WEBSITE
# ==========================

@bot.command()
async def make(ctx, *, idea):

    msg = await ctx.send("🧠 Generating website...")

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
You are an expert web developer.

Rules:

1. Return ONLY HTML.
2. Put CSS inside <style>.
3. Put JavaScript inside <script>.
4. Make the website premium.
5. Add animations.
6. Make it mobile friendly.
7. Add gradients and effects.
8. No explanations.
"""
                },
                {
                    "role": "user",
                    "content": f"""
Create a luxury website about:

{idea}

Requirements:

- Premium UI
- Beautiful animations
- Glassmorphism
- Responsive design
- Interactive buttons
- Smooth transitions
"""
                }
            ]
        )

        html = response.choices[0].message.content

        html = html.replace("```html", "")
        html = html.replace("```", "")

        folder = f"site-{int(time.time())}"
        path = f"sites/{folder}"

        os.makedirs(path, exist_ok=True)

        with open(
            f"{path}/index.html",
            "w",
            encoding="utf-8"
        ) as f:
            f.write(html)

        subprocess.run(
            ["git", "add", "."],
            check=True
        )

        subprocess.run(
            ["git", "commit", "-m", f"Created {folder}"],
            check=True
        )

        subprocess.run(
            ["git", "push"],
            check=True
        )

        link = (
            f"https://{GITHUB_USERNAME}.github.io/"
            f"{REPO_NAME}/sites/{folder}/"
        )

        await msg.edit(
            content=(
                f"✅ Website created successfully!\n\n"
                f"🌐 {link}"
            )
        )

    except Exception as e:

        await msg.edit(
            content=f"❌ Error:\n```{e}```"
        )


# ==========================
# START BOT
# ==========================

bot.run(DISCORD_TOKEN)
