# Bibliotecas
import os
import requests
import pandas as pd
import boto3
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Variaveis Reddit
client_id = os.environ.get("REDDIT_CLIENT_KEY")
client_secret = os.environ.get("REDDIT_SECRET_KEY")
user_agent = os.environ.get("REDDIT_USER_AGENT")

# Variaveis OpenAI
client = OpenAI()

# Variaveis Reddit
SUBREDDIT = "python"

# S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)
CSV_PATH = f"{SUBREDDIT}.csv"


# Função para acesso a IA da OPENAI para classificar sentimento de um texto
def classificar_sentimento(texto):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Voce é uma inteligencia artificial especializada em detectar o sentimento de um texto e retorná-lo em uma única string",
            },
            {"role": "user", "content": f"{texto}"},
        ],
    )
    return completion.choices[0].message.content


# Obtendo access token
def get_redict_access_token(client_id, client_secret):
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    data = {"grant_type": "client_credentials"}
    headers = {"User-Agent": user_agent}

    response = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth,
        data=data,
        headers=headers,
    )
    token = response.json()["access_token"]
    return token


# Pegando hot pots de um subreddit
def get_hot_posts(subreddit, token):
    posts_requests = requests.get(
        f"https://oauth.reddit.com/r/{subreddit}/hot",
        headers={"User-Agent": user_agent, "Authorization": f"bearer {token}"},
    )
    return posts_requests.json()


# Criando dataframe a partir de uma lista de dicionarios
def create_df_posts(posts):
    posts_data = []

    for post in posts["data"]["children"]:
        posts_data.append(
            {
                "id": post["kind"] + "_" + post["data"]["id"],
                "subreddit": post["data"]["subreddit"],
                "kind": post["kind"],
                "title": post["data"]["title"],
                "score": post["data"]["score"],
                "selftext": post["data"]["selftext"],
            }
        )

    return pd.DataFrame(posts_data)


# Juntando tudo
print("Obtendo access Token")
token = get_redict_access_token(client_id, client_secret)

print("Obtendo hot posts")
posts = get_hot_posts(SUBREDDIT, token)

print("Criando dataframe")
df_posts = create_df_posts(posts)

print("Classificando sentimento")
df_posts["sentimento"] = df_posts["title"].apply(classificar_sentimento)

print(f"Salvando {CSV_PATH}")
df_posts.to_csv(CSV_PATH, index=False)

# Escrevendo no S3
print("Salvando no S3")
bucket_name = os.environ.get("AWS_S3_BUCKT_NAME")
object_name = CSV_PATH
s3.upload_file(CSV_PATH, bucket_name, f"subreddits/{CSV_PATH}")

print("Fim")
