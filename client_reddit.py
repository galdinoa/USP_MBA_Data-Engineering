import pandas as pd
import praw

class ClientReddit:
    def __init__(self, client_id, client_secret, username, password, user_agent):
        """
        Initialize the ClientReddit class.

        Args:
            client_id (str): The client ID for the Reddit API.
            client_secret (str): The client secret for the Reddit API.
            username (str): The username for the Reddit account.
            password (str): The password for the Reddit account.
            user_agent (str): The user agent for the Reddit API. Exemplo:'meu_app/0.1'
        """
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=user_agent
        )

    def get_hot_posts(self, subreddit_name, limit=100):
        """
        Get hot posts from a subreddit.

        Args:
            subreddit (str): The name of the subreddit.
            limit (int, optional): The maximum number of posts to retrieve. Defaults to 10.

        Returns:
            list: A list of dictionaries containing information about the hot posts.
        """
        subreddit = self.reddit.subreddit(subreddit_name)
        posts = []
        for post in subreddit.hot(limit=limit):
            posts.append(
                {
                    "id": post.id,
                    "ups": post.ups,
                    "downs": post.downs,
                    "upvote_ratio": post.upvote_ratio,
                    "subreddit": post.subreddit.display_name,
                    "title": post.title,
                    "score": post.score,
                    "created_utc": post.created_utc,
                    "url": post.url,
                    "selftext": post.selftext,
                    "comments": [comment.body for comment in post.comments],
                }
            ) 
        return pd.DataFrame(posts)