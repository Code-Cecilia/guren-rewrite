import praw, random
 
class reddit_login:
    def __init__(self, **credentials):
        self.username = credentials['r_username']
        self.redirect_uri = credentials['r_redirect_uri']
        self.client_secret = credentials['r_client_secret']
        self.user_agent = credentials['r_user_agent']
        self.client_id = credentials['r_client_id']

        self.reddit = praw.Reddit(
                            client_id=self.client_id,
                            redirect_uri=self.redirect_uri,
                            client_secret=self.client_secret,
                            user_agent=self.user_agent,
                            username=self.username,
                            check_for_async=False # I use this because asyncpraw sucks. lol.
                        )

    def get_random_title(self, subreddit, limit=10):
        subreddit = self.reddit.subreddit(subreddit)
        x = subreddit.top(limit=limit)
        title_list = []
        for y in x:
            title_list.append(str(y.title))
        choice = random.choice(title_list)
        return choice

    def get_post_data(self, subreddit, limit=10):
        subreddit = self.reddit.subreddit(subreddit)
        sub_list = []
        x = subreddit.hot(limit=limit)
        for y in x:
            sub_list.append(y)
        choice = random.choice(sub_list)

        return {
            "author": choice.author,
            "url": choice.url,
            "subreddit": subreddit.name,
            "like_ratio": choice.like_ratio,
            "title": choice.title
        }
