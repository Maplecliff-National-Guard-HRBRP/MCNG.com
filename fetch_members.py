import discord
import json
import asyncio
import os
from datetime import datetime

# ── CONFIG ──────────────────────────────────────────────────────────────────
#Name needs to be the exact same as the discord role
# If a rank doesn't have a Discord role, remove it from the dict.
RANK_TO_ROLE = {
    "PVT":  "PVT",
    "PV2":  "PVT",
    "PFC":  "PVT",
    "SPC":  "PVT",
    "CPL":  "PVT",
    "SGT":  "PVT",
    "SSG":  "PVT",
    "SFC":  "PVT",
    "MSG":  "PVT",
    "1SG":  "PVT",
    "SGM":  "PVT",
    "CSM":  "PVT",
    "SMA":  "PVT",
    "WO1":  "PVT",
    "CW2":  "PVT",
    "CW3":  "PVT",
    "CW4":  "PVT",
    "CW5":  "PVT",
    "2LT":  "PVT",
    "1LT":  "PVT",
    "CPT":  "PVT",
    "MAJ":  "PVT",
    "LTC":  "PVT",
    "COL":  "PVT",
    "BG":   "PVT",
    "MG":   "PVT",
    "LTG":  "PVT",
    "GEN":  "Owner",
    "GA":   "Owner",
}
# ────────────────────────────────────────────────────────────────────────────

TOKEN     = os.environ["DISCORD_TOKEN"]
GUILD_ID  = int(os.environ["DISCORD_GUILD_ID"])

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = client.get_guild(GUILD_ID)
    if guild is None:
        print(f"ERROR: Guild {GUILD_ID} not found.")
        await client.close()
        return

    # Build role-name → role object map
    role_map = {r.name: r for r in guild.roles}

    result = {}
    for rank, role_name in RANK_TO_ROLE.items():
        role = role_map.get(role_name)
        if role:
            members = [m.display_name for m in guild.members if role in m.roles]
            result[rank] = sorted(members, key=str.lower)
        else:
            result[rank] = []   # role not found – leave empty

    output = {
        "updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "members": result
    }

    with open("members.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"✅  Saved members.json  ({datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')})")
    await client.close()

client.run(TOKEN)
