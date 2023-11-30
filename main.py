# Imports
import discord
from discord.ext import commands
import requests


# Set up the bot with intents
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


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

  gif_url = 'https://cdn.discordapp.com/attachments/1179823207335874680/1179849757577986161/ezgif-2-c23f3ae718.gif?ex=657b47b6&is=6568d2b6&hm=5c3cbb70737fe51d18a0468ffd3703295f776bd5021ca9234a43d3e0725ba812&'

  try:
    # Splits the song name and the artist with a 'by'
    song_name, artist_name = map(str.strip, query.split(" by "))
      
  except ValueError:
      
    # Accounts for errors that might occur
    embed = discord.Embed(

      title = "˚₊· ͟͟͞͞➳❥ Error Message",
      description = "Please provide the song name and artist using 'by' as a separator, like `!lookup_song 'Song Name' by 'Artist'.",
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
      description = f"No tracks found for '{song_name}' by '{artist_name}'. Make sure to check your spelling.",
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
        description = "No tracks found.",
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
      fields.append((f"{album_name}", f"Artist: {artist_name}\nTracks: {number_of_tracks}\n{hyperlink}"))

    # Embeds the information into a nice box
    embed = discord.Embed(

      title = "Top 5 Album Results",
      color = 0xfa419d)

    for name, value in fields:
      embed.add_field(name = name, value = value, inline = False)

    await ctx.send(embed = embed)
    
  else:
      # Sends a message if the track is not located
      embed = discord.Embed(

        title = "˚₊· ͟͟͞͞➳❥ Error Message",
        description = "No albums found.",
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
          description = "•❅───✧❅✦❅✧───❅•\n\nPlease provide the album name and artist using 'by' as a separator, like `!lookup_album 'Album Name' by 'Artist'.\n\n•❅───✧❅✦❅✧───❅•",
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


# This command shows all the commands and what they do
@bot.command()
async def showcommands(ctx):

  gif_url = 'https://cdn.discordapp.com/attachments/1179823207335874680/1179823275979833375/sukuna-ryomen-sukuna.gif?ex=657b2f0d&is=6568ba0d&hm=c4ebfa3f350ff1020974ed8947c19f5de7e9f04f06f2a50bdd6466b284451caf&'
  
  embed = discord.Embed(

    title = "Available Commands",
    color = 0xfc05a6)

  embed.set_image(
    url = gif_url
  )

  await ctx.send(embed = embed)
  

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

# Run the bot
bot.run('MTE3NDg1NjM2NDM0NzExMzQ5Mg.GH5BNH.XR_QEvGuisiF56nVBbYNYEZPt4M6XjGjsRIBp8')