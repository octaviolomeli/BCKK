import discord
import pandas as pd
from discord.ext import commands
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import csv
import json
import os

# Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

creds = None
creds = ServiceAccountCredentials.from_json_keyfile_dict(
        json.loads(os.environ['SERVICE_KEY']), scopes=SCOPES)

# The ID of the buildOn spreadsheet
SPREADSHEET_ID = '1ZTjoYnyJgF23qdyULC9vXwCpJs7iW-hOksXha7wgYpU'

service = build('sheets', 'v4', credentials=creds)


# class
class BuildOn(commands.Cog):

  def __init__(self, client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_ready(self):
      print('BuildOn file is ready.')
      
  # sends the information of a person
  @commands.command()
  async def stats(self, ctx, *, name='Octavio Castro'):
    # Call the Sheets API and select a range of data
      sheet = service.spreadsheets()
      result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="2020-2021 Hours!B2:F98").execute()

      # Save the information in a CSV file to later read in Pandas
      with open('data/buildOn_stats.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        for row in result['values']:
          csv_writer.writerow(row)

      # Read the data into a Pandas dataframe
      stat_list = pd.read_csv('data/buildOn_stats.csv')

      stat_list = stat_list.fillna(0)
      stat_list.set_index('Member Name', inplace=True)
      try:
          emb = discord.Embed(title=name,color=11342935)
          emb.add_field(name="Grade", value=stat_list.loc[name]['Grade'], inline=True)
          emb.add_field(name="Hours Gained", value=stat_list.loc[name]['Hours Gained'], inline=True)
          emb.add_field(name="Goal", value=stat_list.loc[name]['Goal'], inline=True)
        
          await ctx.channel.send(embed=emb)
      except:
          await ctx.send(
              '```No member with that name exists. Check your spelling and capitalization.\nIf error, DM june#6598```'
          )


  # sends top 3 people with hours
  @commands.command()
  async def btop(self, ctx):

    # Call the Sheets API and select a range of data
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="2020-2021 Hours!B2:F98").execute()
    
    # Save the information in a CSV file to later read in Pandas
    with open('data/buildOn_stats.csv', 'w', newline='') as csvfile:
      csv_writer = csv.writer(csvfile, delimiter=',')
      for row in result['values']:
        csv_writer.writerow(row)
  
    stat_list = pd.read_csv('data/buildOn_stats.csv')
    stat_list = stat_list.fillna(0)
    stat_list = stat_list.sort_values("Hours Gained", ascending=False, inplace=False)[:3]
    stat_list.reset_index(inplace=True)
    
    # Send the information of the top 3 members
    emb = discord.Embed(title="Top 3",color=11342935)
    names = f"{stat_list['Member Name'][0]}\n{stat_list['Member Name'][1]}\n{stat_list['Member Name'][2]}"
    emb.add_field(name="Name", value=names, inline=True)

    grades = f"{stat_list['Grade'][0]}\n{stat_list['Grade'][1]}\n{stat_list['Grade'][2]}"
    emb.add_field(name="Grade", value=grades, inline=True)

    hours = f"{stat_list['Hours Gained'][0]}\n{stat_list['Hours Gained'][1]}\n{stat_list['Hours Gained'][2]}"
    emb.add_field(name="Hours Gained", value=hours, inline=True)
        
    await ctx.channel.send(embed=emb)


  # sends the number of services a member attended
  @commands.command()
  async def battended(self, ctx, *,member='Octavio Castro'):

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="2020-2021 Hours!B2:AR98").execute()

    # Write the data into a CSV file to read later in Pandas
    with open('data/buildOn_services.csv', 'w', newline='') as csvfile:
      csv_writer = csv.writer(csvfile, delimiter=',')
      for row in result['values']:
        csv_writer.writerow(row)

    num_list = pd.read_csv('data/buildOn_services.csv')
    num_list = num_list.fillna(0)
    num_list.set_index('Member Name', inplace=True)
    # Get rid of the unneccesary information for this function
    dropping = ['Grade', 'Hours Gained', 'Goal', 'Hours Needed']
    num_list = num_list.drop(dropping, axis = 1)

    try:
      count = 0
      for column_num in range(len(num_list.columns)):
          if not(num_list.loc[member][column_num] in [0, '0', '', ' ', None]) :
              count += 1
      await ctx.send("{} has attended {} services.".format(member, count))
    except:
      await ctx.send('```No member with that name exists. Check your spelling and capitalization.\nIf error, DM june#6598```')

def setup(client):
    client.add_cog(BuildOn(client))