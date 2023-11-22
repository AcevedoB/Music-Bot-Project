# Imports

import discord
from discord.ext import commands, tasks
import requests
import pandas as pd
import json

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

  return tracks


# Looks up a song that matches both the artist and the song inputed
# by the user
@bot.command()
async def lookup_song(ctx, *, query):

    try:
        # Splits the song name and the artist with a 'by'
        song_name, artist_name = map(str.strip, query.split(" by "))
      
    except ValueError:
        # Accounts for errors that might occur
        await ctx.send("Please provide the song name and artist using 'by' as a separator, like `!lookup_song Song Name by Artist`.")
      
        return

    # Gets the track information based on the user input
    track_info = get_track_info(song_name, artist_name)

    if track_info:
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

        # Embeds the information into a nice box
        embed = discord.Embed(
          
            title=f"{track_name}",
            url=f"{preview_url}",
            description=f"Artist: {artist_name}\nAlbum: {album_name}",
            color=0xfa419d
          
        )

        embed.set_thumbnail(
            url=album_cover
        )

        await ctx.send(embed=embed)

    else:
        # Sends a message if the track is not located
        await ctx.send(f"No tracks found for '{song_name}' by '{artist_name}'.")


# Command to look up a track by name
@bot.command()
async def search_songs(ctx, *, track_name):

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

      # Create a hyperlink for the artist name
      hyperlink = f"[Song Preview]({preview_url})"

      # Fills the list with all the values found
      fields.append((f"{track.get('title')}", f"Artist: {artist_name}\nAlbum: {album_name}\n{hyperlink}"))

    # Embeds the information into a nice box
    embed = discord.Embed(
      
      title = "Top 10 Song Results",
      color = 0xfa419d)

    for name, value in fields:
      embed.add_field(name=name, value=value, inline=False)

    await ctx.send(embed=embed)
    
  else:
      # Sends a message if the track is not located
      await ctx.send('No tracks found.')

  
# Command to look up an album by name
@bot.command()
async def search_albums(ctx, *, album_name):
  
  # Gets the track information the user put in
  album_info = search_function(album_name)

  # Check if any tracks were found based on the name
  if album_info:

    # List used to store the values needed
    fields = []

    # This loop iterates through the top 10 albums on the search
    for album in album_info[:10]:

      # Gets the album
      album_name = album.get('album').get('title')

      # Gets the artists name
      artist_name = album.get('artist').get('name')

      # Fills the list with all the values found
      fields.append((f"{album_name}", f"Artist: {artist_name}"))

    # Embeds the information into a nice box
    embed = discord.Embed(

      title = "Top 10 Album Results",
      color = 0xfa419d)

    for name, value in fields:
      embed.add_field(name=name, value=value, inline=False)

    await ctx.send(embed=embed)
    
  else:
      # Sends a message if the track is not located
      await ctx.send('No tracks found.')


@bot.command()
async def lookup_album(ctx, *, query):
  
    # Split the query into album name and artist
    try:
      
        # Splits the album name and the artist with a 'by'
        album_name, artist_name = map(str.strip, query.split(" by "))
    except ValueError:
      
        # Accounts for errors that might occur
        await ctx.send("Please provide the album name and artist using 'by' as a separator, like `!lookup_album 'Album Name' by 'Artist'.")

        return

    # Gets the track information based on the user input
    track_info = get_track_info(album_name, artist_name)
  

    if track_info:

      # List that stores the album tracks
      album_tracks = []

      # Gets the tracklist link within the album
      tracklist_link = track_info[0].get('album').get('tracklist')

      # Snatches the JSON for the tracklist
      response = requests.get(tracklist_link)
      tracklist_data = response.json()

      # Takes out the track names
      album_tracks = [f"[{track.get('title')}]({track.get('preview')})\n" 
for track in tracklist_data.get('data', [])]

      # Gets the artists name
      artist_info = track_info[0].get('artist')
      artist_name = artist_info.get('name')

      # Gets the album info
      album_name = track_info[0].get('album').get('title')
      album_cover = track_info[0].get('album', {}).get('cover_big')

      # Embeds the information into a nice box
      embed = discord.Embed(
          title=f"{album_name}",
          description=f"Artist: {artist_name}\nAlbum: {album_name}\n",
          color=0xfa419d
      )

      embed.add_field(name="Tracks", value="".join(album_tracks), inline=False)

      # Embeds the album cover
      embed.set_thumbnail(
          url=album_cover
      )

      await ctx.send(embed=embed)

    else:
        # Sends a message if the track is not located
        await ctx.send(f"No tracks found for '{album_name}' by '{artist_name}'.")


# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

# Run the bot
bot.run('MTE3NDg1NjM2NDM0NzExMzQ5Mg.GB1rOK.hM2CplrwQ7qWzuzMN1T6cSaniq3hlt_BnpJa44')