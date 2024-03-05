from collections import Counter

import emoji
from urlextract import URLExtract
from wordcloud import WordCloud

extractor = URLExtract()
import pandas as pd


def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    tm = df.shape[0]
    words = []
    links = []
    for mess in df['message']:
        links.extend(extractor.find_urls(mess))
        words.extend(mess.split())

    tw = len(words)
    tl = len(links)
    tmed = df[df["message"] == "<Media omitted>\n"].shape[0]
    return tm, tw, tmed, tl


def most_busy_user(df):
    x = df["user"].value_counts().head()
    y = round((df["user"].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={"index": "name", "user": "percent"})
    return x, y


def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    # temp = df[df['user'] != "group_notification"]
    # temp = temp[temp["message"] != '<Media omitted\n']
    # temp = temp[temp["message"] != "<media omitted"]
    #

    td = df[df["message"] != "<Media omitted>\n"]
    td = td[td["user"] != 'group_notification']
    wc = WordCloud(width=400, height=400, min_font_size=10, background_color='black')
    df_wc = wc.generate(td["message"].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    temp = df[df['user'] != "group_notification"]
    temp = temp[temp["message"] != '<Media omitted\n']
    temp = temp[temp["message"] != "<media omitted"]
    temp = temp[temp["message"] != "<media omitted\n"]
    temp = temp[temp["message"] != "<Media omitted"]

    words = []
    f = open("stop_hinglish.txt", "r")
    stop_words = f.read()
    for mess in temp["message"]:
        for word in mess.lower().split():
            if word not in stop_words:
                if word != "<media" and word != "omitted>":
                    words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df


def emoji_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    emojis = []
    for mess in df["message"]:
        emojis.extend([c for c in mess if c in emoji.UNICODE_EMOJI['en']])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def month_analyser(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    month_timeline = df.groupby(['year', 'month_num', "month"]).count()['message'].reset_index()
    time = []
    for i in range(month_timeline.shape[0]):
        time.append(month_timeline['month'][i] + "-" + str(month_timeline['year'][i]))

    month_timeline['time'] = time
    return month_timeline


def daily_analyser(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    daily_timeline = df.groupby(["only_date"]).count()["message"].reset_index()
    return daily_timeline

def week_analyser( selected_user , df ):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    weekly_timeline = df.groupby('day_name').count()['message'].reset_index()
    return weekly_timeline

def activity_time(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_timeline = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_timeline