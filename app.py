import streamlit as st
import helper
import preprocessor
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("whatsapp chat analyser")
uploaded_file = st.sidebar.file_uploader("Choose a file")
st.title(" VAMSI's chat Analyser")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    # st.dataframe(df)
    # fetching unique users via pythonbro
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox(" Show analysis wrt ", user_list)

    if st.sidebar.button("Show Analysis"):
        st.title("Total Analysis ")
        col1, col2, col3, col4 = st.columns(4)
        num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media")
            st.title(num_media)
        with col4:
            st.header("  Total links ")
            st.title(num_links)

        month_timeline = helper.month_analyser(selected_user, df)
        st.title(" Montly Analysis ")
        fig, ax = plt.subplots()
        ax.plot(month_timeline['time'], month_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title(" User_Activity_timeline")
        user_timeline = helper.activity_time(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_timeline)
        st.pyplot(fig)

        weekly_timeline = helper.week_analyser(selected_user, df)
        st.title("Weekly Analysis ")
        col1, col2 = st.columns(2)

        with col1:
            st.header(" week_based_activity bar")
            fig, ax = plt.subplots()
            ax.bar(weekly_timeline["day_name"], weekly_timeline["message"])
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        with col2:
            st.header(" DataFrame ")
            st.dataframe(weekly_timeline)

        daily_timeline = helper.daily_analyser(selected_user, df)
        st.title(" Day-wise Analysis")
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline["message"])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        if selected_user == "Overall":
            x, y = helper.most_busy_user(df)

            st.title(" Most Active Users")
            col1, col2 = st.columns(2)
            fig, ax = plt.subplots()

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(y)

        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        most_common_df = helper.most_common_words(selected_user, df)
        st.title("most common words ")
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(most_common_df)
        with col2:
            fig, ax = plt.subplots()
            ax.bar(most_common_df[0], most_common_df[1])
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
