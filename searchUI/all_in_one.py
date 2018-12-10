import json, os
import matplotlib.pyplot as plt, mpld3
import numpy as np
from datetime import datetime
import seaborn as sns
import operator
from wordcloud import WordCloud
sns.set()


class visualize:
    def __init__(self, json_file, fig_path):
        self.json_file = json_file
        self.labels = 'Positive', 'Negative', 'Neutral'
        self.date_format = "%Y-%m-%d"
        self.topics_item = {'infra': 0, 'environment': 0, 'crime': 0, 'politics': 0, 'social unrest': 0}
        self.fig_path = os.path.join(os.getcwd(), fig_path)
        if not os.path.isdir(self.fig_path):
            os.makedirs(self.fig_path)
        # self.fig = plt.figure(figsize=(30, 10))
        # plt.tight_layout()

    # def timeline(self):
    #     timetable = np.zeros((5, 15))

    #     start = datetime.strptime('2018-09-01', self.date_format)
    #     l = []
    #     for tweet in self.json_file:
    #         date = tweet['tweet_date'][0][:10]
    #         end = datetime.strptime(date, self.date_format)
    #         l.append(end)
    #     start = min(l)
    #     # with open(self.json_file) as f:
    #     for tweet in self.json_file:
    #         # tweets = json.loads(lines)

    #         # for tweet in tweets:
    #         date = tweet['tweet_date'][0][:10]
    #         end = datetime.strptime(date, self.date_format)
    #         week = (end - start).days // 7
    #         topic = tweet['topic'][0]
    #         row = self.topics_item[topic]
    #         timetable[row, week] = timetable[row, week] + 1

    #     N = timetable.shape[1]
    #     ind = np.arange(N)
    #     width = 0.4
    #     # ax = self.fig.add_subplot(231)
    #     fig = plt.figure()
    #     ax = fig.add_subplot(111)
    #     p = [ax.bar(ind, timetable[0], width)[0]]
    #     for i in range(4):
    #         p.append(plt.bar(ind, timetable[i + 1], width, bottom=np.sum(timetable[0:i + 1], axis=0))[0])

    #     ax.set_ylabel('Topic Counts', fontsize=10)
    #     ax.set_xlabel('Week Range \n (From ' + '{:%Y-%m-%d}'.format(start) + ' To ' + '{:%Y-%m-%d}'.format(end) + ')', fontsize=10)
    #     ax.set_title('Topic Timeline', fontsize=15)
    #     ax.set_xticks(ind, range(1, N + 1))
    #     ax.set_yticks(np.arange(0, np.max(timetable) + 2))
    #     ax.legend(p, list(self.topics_item.keys()), loc=0)
    #     plt.savefig(os.path.join(self.fig_path, 'timeline.png'), dpi=500, bbox_inches='tight')

        # return ax

    # def lang_field(self, tweet):
    #     lan_keys = tweet.keys()
    #     if 'tweet_en' in lan_keys:
    #         return tweet['tweet_en']
    #     elif 'tweet_hi' in lan_keys:
    #         return tweet['tweet_hi']
    #     elif 'tweet_th' in lan_keys:
    #         return tweet['tweet_th']
    #     elif 'tweet_fr' in lan_keys:
    #         return tweet['tweet_fr']
    #     elif 'tweet_fr' in lan_keys:
    #         return tweet['tweet_es']
    #     else:
    #         return tweet['tweet_text']

    def tagcloud(self):
        text = ''
        hashtag = {}
        # with open(self.json_file) as f:
        #     lines = f.readlines()[0]
        #     tweets = json.loads(lines)
        for tweet in self.json_file:
            self.topics_item[tweet['topic'][0]] += 1
            k = 'text_' + tweet['tweet_lang'][0]
            if k in tweet:
                text = text + tweet[k][0]
                for i in range(len(tweet['hashtags'])):
                    if tweet['hashtags'][i] in hashtag.keys():
                        hashtag[tweet['hashtags'][i]] += 1
                    else:
                        hashtag[tweet['hashtags'][i]] = 0
        sorted_hashtags = sorted(hashtag.items(), key=operator.itemgetter(1), reverse=True)
        wordcloud = WordCloud().generate(text)
        wordcloud.background_color = 'white'
        # ax = self.fig.add_subplot(232)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.imshow(wordcloud, interpolation='bilinear', )
        plt.axis("off")
        plt.savefig(os.path.join(self.fig_path, 'tagcloud.png'), dpi=400)
        plt.close("all")
        return sorted_hashtags


    def sentiment(self):
        # tweets = []
        count = 0
        score = []
        pcount = 0
        ncount = 0
        neuCount = 0
        for tweet in self.json_file:
            # score.append(tweet['score'])
            score.append(tweet['sentiment'][0])
            count += 1
            # if count > 50:
            #     break
            parsed_tweet = {}

            # saving text of tweet
            # parsed_tweet['text'] = tweet['tweet_text']
            # parsed_tweet['sentiment'] = tweet['sentiment']
            # parsed_tweet['score'] = np.random.normal(0, 1, (1, ))

            if tweet['sentiment'][0] > 0:
                # parsed_tweet['sentiment'] = 'positive'
                pcount += 1
            elif tweet['sentiment'][0] < 0:
                # parsed_tweet['sentiment'] = 'negative'
                ncount += 1
            else:
                # parsed_tweet['sentiment'] = 'neutral'
                neuCount += 1

            # tweets.append(parsed_tweet)
        # ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        # ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        # ptweets_num = 100 * len(ptweets) / len(tweets)
        # ntweets_num = 100 * len(ntweets) / len(tweets)
        # netweets_num = 100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)
        self.gen_plot(score)
        return {'pos': pcount, 'neg':ncount, 'neu':neuCount}
        # return self.gen_plot(tweets)

    def gen_plot(self, score):
        # ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        # ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        # ptweets_num = 100 * len(ptweets) / len(tweets)
        # ntweets_num = 100 * len(ntweets) / len(tweets)
        # netweets_num = 100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)

        # sizes = [ptweets_num, ntweets_num, netweets_num]
        # # ax1 = self.fig.add_subplot(233)
        # fig1 = plt.figure()
        # ax1 = fig1.add_subplot(111)
        # ax1.set_title('Sentiment Chart')
        # ax1.pie(sizes, labels=self.labels, autopct='%1.1f%%', startangle=90)
        # plt.savefig(os.path.join(self.fig_path, 'pie.png'), bbox_inches='tight', dpi=500)

        # score = []
        # for tweet in tweets:
        #     score.append(tweet['score'])
        # ax2 = self.fig.add_subplot(234)
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111)
        sns.distplot(score, rug=True, hist=True)
        # ax2.set_title('Sentiment Distribution', fontsize=15)
        ax2.set_xlim(-1.0, 1.0)
        ax2.set_ylabel('Density')
        ax2.set_title('Sentiment Distribution')
        ax2.set_xlabel('Negative $\longrightarrow$-------------Neutral--------------$\longrightarrow$ Positive')
        plt.savefig(os.path.join(self.fig_path, 'density.png'), bbox_inches='tight', dpi=500)
        plt.close("all")
        # return ax1, ax2


    def setMap(self):
        # --- Save Countries, Latitudes and Longitudes ---
        pais, lats, lons = [], [], []
        # ax = self.fig.add_subplot(235, projection=ccrs.PlateCarree(central_longitude=0.0))
        # fig = plt.figure()
        # ax = fig.add_subplot(111,projection=ccrs.PlateCarree(central_longitude=0.0))
        # with open(self.json_file) as f:
            # lines = f.readlines()[0]
            # tweets = json.loads(lines)
        # ct = 0
        cty_count = {'United States': 0, 'Mexico': 0, 'Thailand': 0, 'India': 0, 'France': 0}
        for tweet in self.json_file:
            # ct += 1
            # if ct > 1000:
            #     break
            cty_count[tweet['country'][0]] += 1
            # pais.append(tweet['country'][0])

        # count the number of times a country is in the list
        # unique_pais = set(pais)
        # unique_pais = list(unique_pais)
        # # c_numero = []
        # cty_count = {}
        # for p in pais:
        #     # c_numero.append(pais.count(p))
        #     cty_count[p] = cty_count.get(p, 0) + 1
        # maximo = max(c_numero)

        # # --- Build Map ---
        # cmap = plt.get_cmap('Reds')

        # # --- Using the shapereader ---
        # test = 0
        # shapename = 'admin_0_countries'
        # countries_shp = shpreader.natural_earth(resolution='110m',
        #                                   category='cultural', name=shapename)
        # ax.coastlines(resolution='110m', color='grey', linewidth=0.3)
        # ax.add_feature(cfeature.BORDERS, facecolor='none', edgecolor='k', linewidth=0.2)
        # ax.add_feature(cfeature.LAKES, facecolor='#BAECFA', linewidth=0.2)
        # ax.add_feature(cfeature.OCEAN, facecolor='#75DEFC')
        # ax.outline_patch.set_visible(False)

        # for country in shpreader.Reader(countries_shp).records():
        #     nome = country.attributes['NAME_LONG']
        #     if nome in unique_pais:
        #         i = unique_pais.index(nome)
        #         numero = c_numero[i]
        #         ax.add_geometries(country.geometry, ccrs.PlateCarree(),
        #                           facecolor=cmap(numero / float(maximo), 1),
        #                           label=nome)
        #         test = test + 1
        #     else:
        #         ax.add_geometries(country.geometry, ccrs.PlateCarree(),
        #                           facecolor='#FAFAFA',
        #                           label=nome)
        # if test != len(unique_pais):
        #     raise Exception("check the way you are writting your country names!")

        # plt.savefig(os.path.join(self.fig_path, 'heatmap.png'), bbox_inches='tight', dpi=400)
        # plt.close("all")
        # return ax
        return cty_count


# if __name__ == '__main__':
#     visual = visualize('new.json', 'figs')

#     timeline = visual.timeline()
#     tagcloud = visual.tagcloud()
#     density, pie = visual.sentiment()
#     heatmap = visual.setMap()

    # analysis_fig = visual.fig

    # plt.savefig('analysis.png')
    # plt.show()
    # plt.close()
