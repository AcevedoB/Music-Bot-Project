# Imports
import discord
from typing import Dict
from discord.ui import View, Select
from discord import SelectOption
from discord.ext import commands
import requests
import os


# Set up the bot with intents
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Secures the token
TOKEN = os.environ['TOKEN']


# Method that gets the tracks information
def search_function(search_function):

  # Deezer API base URL
  url = "https://deezerdevs-deezer.p.rapidapi.com/search"

  querystring = {"q": search_function}

  headers = {
    "X-RapidAPI-Key":       
    "8acd9e6352msh85cc09f2fbe0ec1p14715ejsn0b8bee01e34b",
    "X-RapidAPI-Host": "deezerdevs-deezer.p.rapidapi.com"
  }

  # Retrieves the JSON
  response = requests.get(url, headers = headers, params =     
  querystring)

  data = response.json()
  
  # Access the 'data' key, which contains a list of information
  info = data.get('data', [])
  return info


# Method that gets the song and artist information
def get_track_info(song_name, artist_name):
  url = "https://deezerdevs-deezer.p.rapidapi.com/search"

  querystring = {"q": f"{song_name} {artist_name}"}

  headers = {
      "X-RapidAPI-Key": "8acd9e6352msh85cc09f2fbe0ec1p14715ejsn0b8bee01e34b",
      "X-RapidAPI-Host": "deezerdevs-deezer.p.rapidapi.com"
  }

  # Retrieves the JSON
  response = requests.get(url, headers=headers, params=querystring)
  data = response.json()

  # Access the 'data' key, which likely contains a list of tracks
  tracks = data.get('data', [])

  # Convert input to lowercase
  song_name_lower = song_name.lower()
  artist_name_lower = artist_name.lower()

  # Filters tracks by title and artist
  filtered_tracks = [
      track for track in tracks
      if track.get('title').lower() == song_name_lower
      and track.get('artist').get('name').lower() == artist_name_lower # The 'to lower' prevents case sensitivity
  ]

  return filtered_tracks

# Method that gets the album and artist information
def get_album_info(album_name, artist_name):
  url = "https://deezerdevs-deezer.p.rapidapi.com/search"

  querystring = {"q": f"{album_name} {artist_name}"}

  headers = {
      "X-RapidAPI-Key": "8acd9e6352msh85cc09f2fbe0ec1p14715ejsn0b8bee01e34b",
      "X-RapidAPI-Host": "deezerdevs-deezer.p.rapidapi.com"
  }

  # Retrieves the JSON
  response = requests.get(url, headers=headers, params=querystring)
  data = response.json()

  # Access the 'data' key, which likely contains a list of tracks
  tracks = data.get('data', [])

  # Convert input to lowercase
  album_name_lower = album_name.lower()
  artist_name_lower = artist_name.lower()

  # Filters tracks by title and artist
  filtered_tracks = [
      track for track in tracks
      if track.get('album').get('title').lower() == album_name_lower
      and track.get('artist').get('name').lower() == artist_name_lower # The 'to lower' prevents case sensitivity
  ]

  return filtered_tracks

# Finds specific ID's for different things depending on what's
# inputted
def find_info(category, id):
  url = f"https://deezerdevs-deezer.p.rapidapi.com/{category}/{id}"

  headers = {
      "X-RapidAPI-Key": "8acd9e6352msh85cc09f2fbe0ec1p14715ejsn0b8bee01e34b",
      "X-RapidAPI-Host": "deezerdevs-deezer.p.rapidapi.com"
  }

  # Retrieves the JSON
  response = requests.get(url, headers=headers)
  data = response.json()

  # Access the 'data' key, which likely contains a list of tracks
  return data


# Looks up a song that matches both the artist and the song inputed
# by the user
@bot.command()
async def lookupsong(ctx, *, query):

  gif_url = 'https://cdn.discordapp.com/attachments/1179823207335874680/1179918892374708275/ezgif-2-77f96dc773.gif?ex=657b8819&is=65691319&hm=f8833fe80128065e04028a09fac1d0830bea58d7dbc4850b9a773bc2f7fafb0a&'

  try:
    # Splits the song name and the artist with a 'by'
    song_name, artist_name = map(str.strip, query.split(" by "))
      
  except ValueError:
      
    # Accounts for errors that might occur
    embed = discord.Embed(

      title = "˚₊· ͟͟͞͞➳❥ Error Message",
      description = "•❅───✧❅✦❅✧───❅•\n\nPlease provide the song name and artist using 'by' as a separator, like `!lookupsong 'Song Name' by 'Artist'.\n\n•❅───✧❅✦❅✧───❅•",
      color = 0xfc0303)
    await ctx.send(embed = embed)
      
    return

  # Gets the track information based on the user input
  track_info = get_track_info(song_name, artist_name)

  if track_info:

    # Gets the track ID to access the track json
    track_id = track_info[0].get('id')
    track_data = find_info('track', track_id)

    # Gets the tracks release date
    release_date =  track_data.get('release_date')

    # Get the track name
    track_name = track_info[0].get('title')

    # Gets the preview for the songs
    preview_url = track_info[0].get('preview')

    # Gets the artists name
    artist_info = track_info[0].get('artist')
    artist_name = artist_info.get('name')

    # Gets the album info
    album_name = track_info[0].get('album').get('title')
    album_cover = track_info[0].get('album', {}).get('cover_medium')
    album_id = track_info[0].get('album').get('id')

    # Gets the genre info from a seperate json
    album_data = find_info('album', album_id)
    genre_name = album_data.get('genres').get(
            'data')[0].get('name')
          
    # Embeds the information into a nice box
    embed = discord.Embed(
                  
      title = f"˚₊· ͟͟͞͞➳❥ {track_name}",
      url = f"{preview_url}",
      description = f"╔══ ≪ °❈° ≫ ══╗\n*ˏˋ°•⁀➷ Artist: {artist_name}\nˏˋ°•⁀➷ Album: {album_name}\nˏˋ°•⁀➷ Genre: {genre_name}\nˏˋ°•⁀➷ Release Date: {release_date}*\n╚══ ≪ °❈° ≫ ══╝",
      color=0xfa419d
                  
    )
        
    embed.set_thumbnail(
      url = album_cover
    )

    embed.set_image(url = gif_url)
        
    await ctx.send(embed = embed)

  else:
      
    # Sends a message if the track is not located
    embed = discord.Embed(

      title = "˚₊· ͟͟͞͞➳❥ Error Message",
      description = f"•❅───✧❅✦❅✧───❅•\n\nNo tracks found for '{song_name}' by '{artist_name}'. Make sure to check your spelling.\n\n•❅───✧❅✦❅✧───❅•",
      color = 0xfc0303)
      
    await ctx.send(embed = embed)


# Command to look up a track by name
@bot.command()
async def searchsongs(ctx, *, track_name):

  # Gets the track information the user put in
  track_info = search_function(track_name)

  # Check if any tracks were found based on the name
  if track_info:

    # List used to store the values needed
    fields = []

    # This loop iterates through all the songs that were found
    for track in track_info[:10]:

      # Gets the preview for the songs
      preview_url = track.get('preview')

      # Gets the artists name
      artist_name = track.get('artist').get('name')

      # Gets the songs album
      album_name = track.get('album').get('title')

      # Create a hyperlink to provide a preview
      hyperlink = f"[Song Preview]({preview_url})"

      # Fills the list with all the values found
      fields.append((f"*ˏˋ°•⁀➷ {track.get('title')}*", f"*ˏˋ°•⁀➷ Artist: {artist_name}\nˏˋ°•⁀➷ Album: {album_name}\nˏˋ°•⁀➷ * {hyperlink}\n\n •❅───✧❅✦❅✧───❅•\n"))

    # Embeds the information into a nice box
    embed = discord.Embed(
      
      title = "˚₊· ͟͟͞͞➳❥ Top 10 Song Results",
      description = '•❅───✧❅✦❅✧───❅•',
      color = 0xfa419d)

    for name, value in fields:
      embed.add_field(name = name, value = value, inline = False)

    await ctx.send(embed = embed)
    
  else:
    
      # Sends a message if the track is not located
      embed = discord.Embed(

        title = "˚₊· ͟͟͞͞➳❥ Error Message",
        description = "•❅───✧❅✦❅✧───❅•\n\nNo tracks found.\n\n•❅───✧❅✦❅✧───❅•",
        color = 0xfc0303)
    
      await ctx.send(embed = embed)

  
# Command to look up an album by name
@bot.command()
async def searchalbums(ctx, *, album_name):
  
  # Gets the track information the user put in
  album_info = search_function(album_name)
  

  # Check if any tracks were found based on the name
  if album_info:

    # List used to store the values needed
    fields = []

    # This loop iterates through the top 10 albums on the search
    for album in album_info[:5]:

      # Gets the album ID to access the album json
      album_id = album.get('album').get('id')
      extra_info = find_info('album', album_id)

      # Gets the number of tracks in the album
      number_of_tracks = extra_info.get('nb_tracks')

      # Gets the link to the album
      album_link = extra_info.get('link')

      # Creates a hyperlink to the album link
      hyperlink = f"[Album Link]({album_link})"

      # Gets the album
      album_name = album.get('album').get('title')

      # Gets the artists name
      artist_name = album.get('artist').get('name')

      # Fills the list with all the values found
      fields.append((f"ˏˋ°•⁀➷ {album_name}", f"*ˏˋ°•⁀➷ Artist: {artist_name}\nˏˋ°•⁀➷ Tracks: {number_of_tracks}*\nˏˋ°•⁀➷ {hyperlink}\n\n•❅───✧❅✦❅✧───❅•"))

    # Embeds the information into a nice box
    embed = discord.Embed(

      title = "˚₊· ͟͟͞͞➳❥ Top 5 Album Results",
      description = '•❅───✧❅✦❅✧───❅•',
      color = 0xfa419d)

    for name, value in fields:
      embed.add_field(name = name, value = value, inline = False)

    await ctx.send(embed = embed)
    
  else:
      # Sends a message if the track is not located
      embed = discord.Embed(

        title = "˚₊· ͟͟͞͞➳❥ Error Message",
        description = "•❅───✧❅✦❅✧───❅•\n\nNo albums found.\n\n•❅───✧❅✦❅✧───❅•",
        color = 0xfc0303)
    
      await ctx.send(embed = embed)


@bot.command()
async def lookupalbum(ctx, *, query):
  
    # Split the query into album name and artist
    try:
      
        # Splits the album name and the artist with a 'by'
        album_name, artist_name = map(str.strip, query.split(" by "))
    except ValueError:
      
        # Accounts for errors that might occur
        embed = discord.Embed(

          title = "˚₊· ͟͟͞͞➳❥ Error Message",
          description = "•❅───✧❅✦❅✧───❅•\n\nPlease provide the album name and artist using 'by' as a separator, like `!lookupalbum 'Album Name' by 'Artist'.\n\n•❅───✧❅✦❅✧───❅•",
          color = 0xfc0303)

        await ctx.send(embed=embed)
        return

    # Gets the track information based on the user input
    track_info = get_album_info(album_name, artist_name)

    if track_info:

      # List that stores the album tracks
      album_tracks = []

      # Gets the tracklist link within the album
      tracklist_link = track_info[0].get('album').get('tracklist')

      # Snatches the JSON for the tracklist
      response = requests.get(tracklist_link)
      tracklist_data = response.json()

      # Takes out the track names
      album_tracks = [f"*❥ {track.get('title')}*\n" for track in tracklist_data.get('data', [])]

      # Gets the artists name
      artist_name = track_info[0].get('artist').get('name')

      # Gets the album info
      album_id = track_info[0].get('album').get('id')
      album_name = track_info[0].get('album').get('title')
      album_cover = track_info[0].get('album', {}).get('cover_big')

      album_info = find_info('album', album_id)
      release_date = album_info.get('release_date')
      album_link = album_info.get('link')
      genre = album_info.get('genres').get(
        'data')[0].get('name')

      # Embeds the information into a nice box
      embed = discord.Embed(
        title = f"˚₊· ͟͟͞͞➳❥ {album_name}",
        url = album_link,
        description = f"*ˏˋ°•⁀➷ Artist: {artist_name}\nˏˋ°•⁀➷ Release Date: {release_date}*\nˏˋ°•⁀➷ Genre: {genre}\n\n•❅───✧❅✦❅✧───❅•",
        color = 0xfa419d
      )

      embed.add_field(name = "˚₊· ͟͟͞͞➳❥ Tracks", value = "".join(album_tracks), inline = False)

      # Embeds the album cover
      embed.set_thumbnail(
          url = album_cover
      )

      await ctx.send(embed = embed)

    else:
      
      # Sends a message if the track is not located
      embed = discord.Embed(

        title = "˚₊· ͟͟͞͞➳❥ Error Message",
        description = f"•❅───✧❅✦❅✧───❅•\n\nNo albums found for '{album_name}' by '{artist_name}'. Try checking your spelling.\n\n•❅───✧❅✦❅✧───❅•",
        color = 0xfc0303)
      
      await ctx.send(embed = embed)


# This class allows for the use of a drop down menu using the 
# showcommands command.
class MyView(discord.ui.View):

  # Place to store the users answer
  answer1 = None

  # Gives all the options within the drop down
  @discord.ui.select(
    placeholder = "Pick One I Guess...",
    
    options = [
      
      discord.SelectOption(label = '!searchsongs', value = 'searchsongs'),
      
      discord.SelectOption(label = '!searchalbums', value = 'searchalbums'),
      
      discord.SelectOption(label = '!lookupsong', value = 'lookupsong'),
      
      discord.SelectOption(label = '!lookupalbum', value = 'lookupalbum')
    ]
  )

  # Gives all the answers to the drop down menu
  async def select_callback(self, interaction:discord.Interaction, select_item : discord.ui.Select):

    # Urls to all the images we need
    searchsongs_url = 'https://cdn.discordapp.com/attachments/1179823207335874680/1180704098413183058/2023-12-02-21-55-14_-_Trim.gif?ex=657e6361&is=656bee61&hm=21c0c1c640ba0f5ad3f6b2877b633ee41b191b6d40f001ef93a29bf4b77ffae9&'

    searchalbums_url = 'https://cdn.discordapp.com/attachments/1179823207335874680/1180705540649787433/2023-12-02-22-00-54_-_Trim.gif?ex=657e64b9&is=656befb9&hm=0c6495640e4c2145aa05d1601cea762e8e571f211df9d2fbe211614289d2ecbc&'

    lookupsong_url = 'https://cdn.discordapp.com/attachments/1179823207335874680/1180707026435838003/2023-12-02-22-04-02_-_Trim.gif?ex=657e661b&is=656bf11b&hm=6b2164495926a390821164611fc415e8bc3c2782fcb327b2bdc255ae9e49bd3b&'

    lookupalbum_url = 'https://cdn.discordapp.com/attachments/1179823207335874680/1180707026435838003/2023-12-02-22-04-02_-_Trim.gif?ex=657e661b&is=656bf11b&hm=6b2164495926a390821164611fc415e8bc3c2782fcb327b2bdc255ae9e49bd3b&'

    # Moves the users answer to in here so it can be utilized
    self.answer1 = select_item.values[0] if select_item.values else None

    # Displays a message depending on what the user inputs
    if self.answer1 == 'searchsongs':
        embed = discord.Embed(
            title='°✮  🎀  ❢𝒮𝑒𝒶𝓇𝒸𝒽 𝓈♡𝓃𝑔𝓈  🎀  ✮',
            color = 0xfa419d
          
        )
        embed.set_image(url = searchsongs_url)
      
        await interaction.response.send_message(embed=embed)
        self.stop()
      
    elif self.answer1 == 'searchalbums':
        embed = discord.Embed(
            title = r'🐸⋆🐓❀🎀  ❢𝒮𝑒𝒶𝓇𝒸𝒽 𝒶𝓁𝒷𝓊𝓂𝓈  🎀❀🐓 ⋆ 🐸',
            color = 0xfa419d
          
        )
        embed.set_image(url = searchalbums_url)
      
        await interaction.response.send_message(embed=embed)
        self.stop()
      
    elif self.answer1 == 'lookupsong':
        embed = discord.Embed(
            title = '🐻 ✮ 🎀  ❣❀𝓁𝑜𝑜𝓀𝓊𝓅 𝓈𝑜𝓃𝑔  🎀 ✮ 🐻',
            color = 0xfa419d
          
        )
        embed.set_image(url = lookupsong_url)
      
        await interaction.response.send_message(embed=embed)
        self.stop()
      
    elif self.answer1 == 'lookupalbum':
        embed = discord.Embed(
            title = '🐘 ⋆ 🐞 ✮ 🎀  ❢𝓁𝑜𝑜𝓀𝓊𝓅𝒶𝓁𝒷𝓊𝓂  🎀 ✮ 🐞 ⋆ 🐘',
            color = 0xfa419d
          
        )
        embed.set_image(url = lookupalbum_url)
      
        await interaction.response.send_message(embed = embed)
        self.stop()


# This command shows all the commands and what they do
@bot.command()
async def showcommands(ctx):
  view = MyView()
  await ctx.send("What don't you understand?", view=view)


# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

# Run the bot
bot.run(TOKEN)