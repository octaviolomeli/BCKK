import discord
import requests
import lxml
import csv
import pandas as pd
from bs4 import BeautifulSoup
from discord.ext import commands


# Class
class Covid(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Covid file is ready.')

    # Sends num of case for COVID-19 for a state
    @commands.command()
    async def covid(self, ctx, *,state='California'):

        source = requests.get('https://news.google.com/covid19/map?hl=en-US&mid=%2Fm%2F09c7w0&gl=US&ceid=US%3Aen').text
        soup = BeautifulSoup(source, 'lxml')

        sections = soup.find_all('tr', class_='sgXwHf wdLSAe YvL7re')

        states = []
        cases = []

        for data in sections:
            states.append(data.find('div', class_='TWa0lb').text)

            state_stats = data.find_all('td', class_='l3HOY')
            for index in range(len(state_stats)):
                state_stats[index] = state_stats[index].text

            cases.append([state_stats[0], state_stats[-1]])

        with open('data/covid_stats.csv', 'w') as myFile:

            csv_writer = csv.writer(myFile)
            csv_writer.writerow(['State', 'Cases', 'Deaths'])

            for index in range(len(states)):
                csv_writer.writerow([states[index], cases[index][0], cases[index][1]])

        covid_stat = pd.read_csv('data/covid_stats.csv')
        covid_stat.set_index(covid_stat['State'], inplace=True)
        covid_stat = covid_stat[['Cases', 'Deaths']]

        try:
            await ctx.send('{} has about {} cases with {} deaths.'.format(
                state, covid_stat.loc[state]['Cases'],
                covid_stat.loc[state]['Deaths']))
        except:
            await ctx.send('No data available for {}.'.format(state))

    # sends the states with more than an inputted number of cases
    @commands.command()
    async def ccm(self, ctx, num=500000):
        source = requests.get('https://news.google.com/covid19/map?hl=en-US&mid=%2Fm%2F09c7w0&gl=US&ceid=US%3Aen').text
        soup = BeautifulSoup(source, 'lxml')

        sections = soup.find_all('tr', class_='sgXwHf wdLSAe YvL7re')

        states = []
        cases = []

        for data in sections:
            states.append(data.find('div', class_='TWa0lb').text)

            state_stats = data.find_all('td', class_='l3HOY')
            for index in range(len(state_stats)):
                state_stats[index] = state_stats[index].text

            cases.append([state_stats[0], state_stats[-1]])

        with open('data/covid_stats.csv', 'w') as myFile:

            csv_writer = csv.writer(myFile)
            csv_writer.writerow(['State', 'Cases', 'Deaths'])

            for index in range(len(states)):
                csv_writer.writerow([states[index], cases[index][0], cases[index][1]])
                
        df = pd.read_csv('data/covid_stats.csv')

        for index in range(len(df['Cases'])):
            df['Cases'][index] = df['Cases'][index].replace(',', '', 5)
            df['Cases'][index] = float(df['Cases'][index])

        df.sort_values(by='Cases', ascending=False, inplace=True)
        try:
            filt = df['Cases'] > num
            list_version = df[filt]['State'].tolist()
            states = ""
            for state in list_version:
              states += state + ", "

            if len(list_version) == 0:
              states = "No state qualifies. "
          
            await ctx.send(states[:-2])
        except:
          
            await ctx.send('Not a valid input.')

    # sends the states with more than an inputted number of deaths from COVID-19
    @commands.command()
    async def cdm(self, ctx, num=17000):
        source = requests.get('https://news.google.com/covid19/map?hl=en-US&mid=%2Fm%2F09c7w0&gl=US&ceid=US%3Aen').text
        soup = BeautifulSoup(source, 'lxml')

        sections = soup.find_all('tr', class_='sgXwHf wdLSAe YvL7re')

        states = []
        cases = []

        for data in sections:
            states.append(data.find('div', class_='TWa0lb').text)

            state_stats = data.find_all('td', class_='l3HOY')
            for index in range(len(state_stats)):
                state_stats[index] = state_stats[index].text

            cases.append([state_stats[0], state_stats[-1]])

        with open('data/covid_stats.csv', 'w') as myFile:

            csv_writer = csv.writer(myFile)
            csv_writer.writerow(['State', 'Cases', 'Deaths'])

            for index in range(len(states)):
                csv_writer.writerow([states[index], cases[index][0], cases[index][1]])

        df = pd.read_csv('data/covid_stats.csv')

        for index in range(len(df['Deaths'])):
            df['Deaths'][index] = df['Deaths'][index].replace(',', '', 5)
            df['Deaths'][index] = float(df['Deaths'][index])
        df.sort_values(by='Deaths', ascending=False, inplace=True)
        try:
            filt = df['Deaths'] > num
            list_version = df[filt]['State'].tolist()
            states = ""
            for state in list_version:
              states += state + ", "

            if len(list_version) == 0:
              states = "No state qualifies."
              
            await ctx.send(states[:-2])
        except:
            await ctx.send('Not a valid input.')


def setup(client):
    client.add_cog(Covid(client))
