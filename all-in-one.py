import json, os
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import numpy as np
from datetime import datetime
import seaborn as sns
from wordcloud import WordCloud
from textblob import TextBlob
sns.set()


class visualize:
    def __init__(self, json_file, fig_path):
        self.json_file = json_file
        self.labels = 'Positive', 'Negative', 'Neutral'
        self.date_format = "%Y-%m-%d"
        self.topics_item = {'infra': 0, 'environment': 1, 'crime': 2, 'politics': 3, 'social unrest': 4}
        self.fig_path = os.path.join(os.getcwd(), fig_path)
        if not os.path.isdir(self.fig_path):
            os.makedirs(self.fig_path)

    def timeline(self):
        timetable = np.zeros((5, 15))

        start = datetime.strptime('2018-09-01', self.date_format)

        with open(self.json_file) as f:
            lines = f.readlines()[0]
            tweets = json.loads(lines)

            for tweet in tweets:
                date = tweet['tweet_date'][:10]
                end = datetime.strptime(date, self.date_format)
                week = (end - start).days // 7
                topic = tweet['topic']
                row = self.topics_item[topic]
                timetable[row, week] = timetable[row, week] + 1

        N = timetable.shape[1]
        ind = np.arange(N)
        width = 0.4
        p = [plt.bar(ind, timetable[0], width)[0]]
        for i in range(4):
            p.append(plt.bar(ind, timetable[i + 1], width, bottom=np.sum(timetable[0:i + 1], axis=0))[0])

        plt.ylabel('Topic Counts', fontsize=10)
        plt.xlabel('Week Range \n (From 2018-09-01 To 2018-11-30)', fontsize=10)
        plt.title('Topic Timeline', fontsize=15)
        plt.xticks(ind, range(1, N + 1))
        plt.yticks(np.arange(0, np.max(timetable) + 2))
        plt.legend(p, list(self.topics_item.keys()), loc=0)
        plt.savefig(os.path.join(self.fig_path, 'timeline.png'), dpi=500, bbox_inches='tight')
        plt.close()

    def lang_field(self, tweet):
        lan_keys = tweet.keys()
        if 'tweet_en' in lan_keys:
            return tweet['tweet_en']
        elif 'tweet_hi' in lan_keys:
            return tweet['tweet_hi']
        elif 'tweet_th' in lan_keys:
            return tweet['tweet_th']
        elif 'tweet_fr' in lan_keys:
            return tweet['tweet_fr']
        elif 'tweet_fr' in lan_keys:
            return tweet['tweet_es']
        else:
            return tweet['tweet_text']

    def tagcloud(self):
        text = ''
        with open(self.json_file) as f:
            lines = f.readlines()[0]
            tweets = json.loads(lines)
            for tweet in tweets:
                text = text + self.lang_field(tweet)

        wordcloud = WordCloud().generate(text)
        wordcloud.background_color = 'white'
        plt.imshow(wordcloud, interpolation='bilinear', )
        plt.axis("off")
        plt.savefig(os.path.join(self.fig_path, 'tagcloud.png'), dpi=400)

    def sentiment(self):
        tweets = []

        with open(self.json_file, 'r') as f:
            lines = f.readlines()[0]
            tweets_ = json.loads(lines)
            count = 0
            for tweet in tweets_:
                count += 1
                if count > 50:
                    break
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet['tweet_text']
                tweet_lang = self.lang_field(tweet)
                parsed_tweet['x_score'] = TextBlob(tweet_lang).sentiment.polarity
                parsed_tweet['y_score'] = TextBlob(tweet_lang).sentiment.subjectivity

                if parsed_tweet['x_score'] > 0:
                    parsed_tweet['sentiment'] = 'positive'
                elif parsed_tweet['x_score'] < 0:
                    parsed_tweet['sentiment'] = 'negative'
                else:
                    parsed_tweet['sentiment'] = 'neutral'

                tweets.append(parsed_tweet)
        self.gen_plot(tweets)

    def gen_plot(self, tweets):
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        ptweets_num = 100 * len(ptweets) / len(tweets)
        ntweets_num = 100 * len(ntweets) / len(tweets)
        netweets_num = 100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)


        sizes = [ptweets_num, ntweets_num, netweets_num]
        plt.figure()
        plt.title('Sentiment Chart')
        plt.pie(sizes, labels=self.labels, autopct='%1.1f%%', startangle=90)
        plt.savefig(os.path.join(self.fig_path, 'pie.png'), bbox_inches='tight', dpi=500)
        plt.close()

        x_score = []
        y_score = []
        for tweet in tweets:
            x_score.append(tweet['x_score'])
            y_score.append(tweet['y_score'])
        plt.figure()
        sns.distplot(x_score, rug=True, hist=True)
        plt.title('Sentiment Distribution', fontsize=15)
        plt.xlim(-1.0, 1.0)
        plt.ylabel('Density')
        plt.xlabel('Negative $\longrightarrow$-------------Neutral--------------$\longrightarrow$ Positive')
        plt.savefig(os.path.join(self.fig_path, 'density.png'), bbox_inches='tight', dpi=500)
        plt.close()


    def setMap(self):
        # --- Save Countries, Latitudes and Longitudes ---
        pais, lats, lons = [], [], []

        with open(self.json_file) as f:
            lines = f.readlines()[0]
            tweets = json.loads(lines)
            ct = 0
            for tweet in tweets:
                ct += 1
                if ct > 1000:
                    break
                # lon = tweet['tweet_loc'][1]
                # lat = tweet['tweet_loc'][0]
                # lats.append(lat)
                # lons.append(lon)
                pais.append(tweet['country'])
        #count the number of times a country is in the list
        unique_pais = set(pais)
        unique_pais = list(unique_pais)
        print(unique_pais)
        c_numero = []
        for p in unique_pais:
            c_numero.append(pais.count(p))
        maximo = max(c_numero)

        # --- Build Map ---
        cmap = plt.get_cmap('Reds')

        # --- Using the shapereader ---
        test = 0
        shapename = 'admin_0_countries'
        countries_shp = shpreader.natural_earth(resolution='110m',
                                                category='cultural', name=shapename)
        ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0.0))
        ax.coastlines(resolution='110m', color='grey', linewidth=0.3)
        ax.add_feature(cfeature.BORDERS, facecolor='none', edgecolor='k', linewidth=0.2)
        ax.add_feature(cfeature.LAKES, facecolor='#BAECFA', linewidth=0.2)
        ax.add_feature(cfeature.OCEAN, facecolor='#75DEFC')
        ax.outline_patch.set_visible(False)

        for country in shpreader.Reader(countries_shp).records():
            nome = country.attributes['NAME_LONG']
            if nome in unique_pais:
                i = unique_pais.index(nome)
                numero = c_numero[i]
                ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                                  facecolor=cmap(numero / float(maximo), 1),
                                  label=nome)
                test = test + 1
            else:
                ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                                  facecolor='#FAFAFA',
                                  label=nome)
        if test != len(unique_pais):
            print("check the way you are writting your country names!")

        plt.savefig(os.path.join(self.fig_path, 'heatmap.png'), bbox_inches='tight', dpi=400)
        plt.close()


if __name__ == '__main__':
    visual = visualize('new.json', 'figs')
    visual.setMap()
    visual.timeline()
    visual.tagcloud()
    visual.sentiment()