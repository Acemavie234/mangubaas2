import discord
import random
import json
import os
from discord.ext import commands


 
client = commands.Bot(command_prefix= "!",intents = discord.Intents().all())

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Kontrollin süsteeme"))


  print('Bot on sisselülitatud')

@client.event
async def on_message(message):
    if message.content.startswith('!lingid'):
        embedVar = discord.Embed(title="Lingid", description="Siit leiad meie lingid.", color=0x00ff00)
        embedVar.add_field(name="Youtube:", value="https://www.youtube.com/channel/UCKMJlRFo1AV_WFo7Kx0y9mg", inline=False)
        embedVar.add_field(name="Veebileht:", value="http://mangubaas.ml/?i=1", inline=False)
        embedVar.add_field(name="Tiktok:", value="https://vm.tiktok.com/ZMdxvgU1X/", inline=False)
        embedVar.add_field(name="Twitter", value="https://twitter.com/mangubaas?s=09", inline=False)
        await message.channel.send(embed=embedVar)
@client.event
async def on_message(message):
  if message.content.startswith('!reeglid'):
    embed=discord.Embed(title="Reeglid", description="Siit saad lugeda reegleid.", color=0x00ff00)
    embed.add_field(name="1.", value="Ära tee tüli", inline=False)
    embed.add_field(name="2.", value="Kuula meeskonda!", inline=False)
    embed.add_field(name="3.", value="Ole viisakas", inline=False)
    embed.add_field(name="4.", value="Ei luni ranke!", inline=False)
    embed.add_field(name="5.", value="Ei küsi millal uus video! Tuleb siis kui tuleb!", inline=False)
    embed.add_field(name="6.", value="Ei saada pilte ega videoid! Välja arvatud pildid kanalis", inline=False)
    embed.add_field(name="7.", value="E", inline=False)
    embed.add_field(name="8.", value="hi2", inline=False)
    await message.channel.send(embed=embed)

  


@client.command()
async def load(ctx, extension):
  client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')
 

@client.command(case_insensitive=True)
async def ping(ctx):
    await ctx.send("Pong!")


@client.command(case_insensitive=True)
async def slowmode(ctx, time:int):
  if (not ctx.author.guild_permissions.manage_messages):
    await ctx.send('Ei saa käsklus tööse lasta! Vajad õigust: ``Manage Messages``')
    return
  if time == 0:
    await ctx.send('Aeglus mood on määratud `0`sekundiks')
    await ctx.channel.edit(slowmode_delay = 0)
  elif time > 21600:
    await ctx.send('Sa ei saa aeglusmoodi tõsta kõrgemaks kui 6 tundi!')
    return
  else:
    await ctx.channel.edit(slowmode_delay = time)
    await ctx.send(f"Aeglusmood on määratud `{time}` sekundiks!")

@client.command(aliases=['clear'])
async def purge(ctx, amount=11):
  if(not ctx.author.guild_permissions.manage_messages):
    await ctx.send('Ei saa käsklus tööse lasta! Vajad õigust: ``Manage Messages``')
    return
  amount = amount+1
  if amount > 101:
   await ctx.send('Ma saan\'Ei saa rohkem kui 100 sõnumit kustutada!') 
  else:
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Kustutatud on edukalt {amount} sõnumit!')

@client.command(aliases=['8ball'])
async def eightball(ctx, *, question):
  responses = ["See on kindel.",
                "See on kindlasti nii.",
                "Kahtlemata.",
                "Jah - kindlasti.",
                "Võite sellele loota.",
                "Nagu ma näen, jah.",
                "Suure tõenäosusega.",
                "Outlook on hea.",
                "Jah.",
                "Märgid osutavad jah.",
                "Vasta hägune, proovi uuesti.",
                "Küsige hiljem uuesti.",
                "Parem ära ütle kohe."
                "Praegu ei oska ennustada.",
                "Keskendu ja küsi uuesti.",
                "Ära looda sellele.",
                "Minu vastus on ei.",
                "Minu allikad ütlevad ei."
                "Väljavaated pole nii head.",
                "Väga kahtlane.",
                "Võib olla."
                "Imelik."
                "Ma arvan et metsa minek on hea mõtte, kuna seal saab korjata seeni."]
  await ctx.send(f':8ball: Vastus: {random.choice(responses)}')

@client.command(case_insensitive=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
  await member.kick(reason=reason)
  await ctx.send(f'{member.mention} on kickitud {ctx.guild}-ist!')

@client.command(case_insensitive=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
 await member.ban(reason=reason)
 await ctx.send(f'{member.mention} on banitud {ctx.guild}-ist!')



@client.command(case_insensitive=True)
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    if reason == None:
        await ctx.send('Palun kirjuta põhjus!')
        return
    guild = ctx.guild
    muteRole = discord.utils.get(guild.roles, name = "Muted")
 
    if not muteRole:
        await ctx.send("Mute role ei leitud! Teen ühe nüüd...")
        muteRole = await guild.create_role(name = "Muted")
 
        for channel in guild.channels:
            await channel.set_permissions(muteRole, speak=False, send_messages=False, read_messages=True, read_message_history=True)
        await member.add_roles(muteRole, reason=reason)
        await ctx.send(f"{member.mention} has been muted in {ctx.guild} | Reason: {reason}")
        await member.send(f"Teid on vaigistatud {ctx.guild} | Põhjus: {reason}")
 
@client.command(case_insensitive=True)
async def unmute(ctx, member: discord.Member, *, reason=None):
 
    guild = ctx.guild
    muteRole = discord.utils.get(guild.roles, name = "Muted")
 
    if not muteRole:
        await ctx.send("mute rolli ei leita! Palun kontrollige, kas on olemas summutusroll või kas kasutajal on see juba olemas!")
        return
    await member.remove_roles(muteRole, reason=reason)
    await ctx.send(f"{member.mention} vaigistus on tühistatud")
    await member.send(f"Sinu vaigistus on tühistatud {ctx.guild}-is")

@client.command(case_insensitive=True)
async def say(ctx, saymsg=None):
  if saymsg==None:
    return await ctx.send("test!")
  
  sayEmbed = discord.Embed(title=f" Teadaanne", color = discord.Color.blue(), description=f"{saymsg}")
  sayEmbed.timestamp = ctx.message.created_at
  sayEmbed.set_footer(text = f"Teadanne {ctx.author} poolt!", icon_url = ctx.author.avatar_url)


  await ctx.send(embed = sayEmbed)


@client.command()
async def avatar(ctx, member: discord.Member=None):
  if member == None:
    member = ctx.author
  
  icon_url = member.avatar_url

  avatarEmbed = discord.Embed(title = f"{member.name}\'Profiilipilt", color = 0xFFA500)

  avatarEmbed.set_image(url = f"{icon_url}")

  avatarEmbed.timestamp = ctx.message.created_at

  await ctx.send(embed = avatarEmbed)


@client.command()
async def poll(ctx, *, question=None):
  if question == None:
    await ctx.send("Please write a poll!")

  icon_url = ctx.author.avatar_url 

  pollEmbed = discord.Embed(title = "Uus küsimus", description = f"{question}")

  pollEmbed.set_footer(text = f"Küsimus tehtud {ctx.author} poolt!", icon_url = ctx.author.avatar_url)

  pollEmbed.timestamp = ctx.message.created_at
  
  await ctx.message.delete()

  poll_msg = await ctx.send(embed = pollEmbed)

  await poll_msg.add_reaction("⬆️")
  await poll_msg.add_reaction("⬇️")


@client.event
async def on_member_join(member):
  await client.get_channel(830126579127943191).send(f"{member.mention} Liitus just serveriga!")









client.run("ODYzMTAzODcxODQ1MDA3Mzkw.YOiCHg.UXMC3e3WD3W6pDAyHstvh0yy7KE")