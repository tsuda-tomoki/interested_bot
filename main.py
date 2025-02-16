import discord
from discord import app_commands
import getseasonall
import kyomiarune
import typing
import os
from dotenv import load_dotenv
import feedparser
import asyncio

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents =intents)
tree = app_commands.CommandTree(client)

load_dotenv()

last_published = None
RSS_URL = "https://yamadashy.github.io/tech-blog-rss-feed/feeds/rss.xml"
# 過去に通知した記事のURLを記録
notified_articles = set()
first_run = True  # 初回実行フラグ

@client.event
async def on_ready():
    
    # ログイン時にログ出し
    print(f'We have logged in as {client.user}')
    
    # ステータスの更新
    new_activity = "豊橋のラッコ"
    await client.change_presence(activity = discord.Game(new_activity))
    
    # 初回実行（確実に最初に実行するため `on_ready()` にも追加）
    await fetch_rss()
    
    # 定期実行を開始
    client.loop.create_task(rss_checker())
    
    # スラッシュコマンドの同期
    await tree.sync()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('#test'):
        await message.channel.send('test')
        
# テストコマンド
@tree.command(name="hello", description="これは引数付きのテストです。")
async def test_command(interaction: discord.Interaction, text:str):
    embed = discord.Embed(title = "テスト", color = 0xff0000)
    embed.add_field(name = "てすと",value = text)
    await interaction.response.send_message(embed = embed)

# ユーザ制御・リストのIDでフィルター
# def is_allowed_user(interaction: discord.Interaction) -> bool:
#   allowed_users = [349052901223825408]  
#   return interaction.user.id in allowed_users

# Annict API を叩いて春夏秋冬の放映アニメを検索する
@tree.command(name = "seasonall", description = "〇〇〇〇年の春夏秋冬のアニメ一覧を出します")
async def seasonall_command(interaction: discord.Interaction, year:str, season:str):
    result = getseasonall.seasonall_search(year = year, season = season)
    embed = discord.Embed(title = f"{year}年の{season}アニメ一覧", color = 0xff0000, description = '\n'.join(result))
    await interaction.response.send_message(embed = embed)

# アニメ検索コマンドの選択肢
@seasonall_command.autocomplete("season")
async def seasonall_autocompletion(
    interaction: discord.Interaction,
    current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for season_select in ['spring', 'summer', 'autumn', 'winter']:
            data.append(app_commands.Choice(name = season_select, value = season_select))
        return data
    
async def fetch_rss():
    """RSSフィードを取得し、新しい記事があればDiscordに送信"""
    global first_run, notified_articles
    feed = feedparser.parse(RSS_URL)
    
    if not feed.entries:
        print("⚠ RSSフィードの取得に失敗")
        return
    
    # Discordチャンネルを取得
    channel = client.get_channel(1210555707901091940)
    
    new_articles = []
    article_count = 10 if first_run else 100  # 初回は最新10件、それ以降はすべて

    # RSSのエントリーを新しい順にチェック
    for entry in feed.entries[:article_count]:
        article_url = entry.link  # 記事のURL

        # 既に通知済みの記事はスキップ
        if article_url in notified_articles:
            continue

        new_articles.append(entry)
        notified_articles.add(article_url)  # 通知済みリストに追加

        # 取得した記事を送信（新しい記事があれば）
    if new_articles:
        for entry in reversed(new_articles):  # 古い記事から順に送信
            await channel.send(f"📰 **新しい記事が公開されたよ！**\n📌 [{entry.title}]({entry.link})")
            print("✅ 記事を送信しました:", entry.title)
    else:
        print("📭 新しい記事はありません")
            
async def rss_checker():
    """一定間隔でRSSフィードをチェック"""
    await client.wait_until_ready()
    
    # 初回実行（Bot起動直後にすぐチェック）
    await fetch_rss()
    
    while not client.is_closed():
        await fetch_rss()
        await asyncio.sleep(60)  # ⏳ 30分ごとにチェック（1800秒）

# 作ったものの微妙だった機能 ↓

# @tree.command(name = "kyomiarune", description = "自称クラウドが興味があるアニメをリストに追加します")
# @app_commands.check(is_allowed_user)
# async def kyomiarune_command(interaction: discord.Interaction,name:str):
#     searchid = kyomiarune.kyomiaruneId(name)
#     result = kyomiarune.kyomiaruneadd(searchid)
#     if result == True:
#         await interaction.response.send_message(f"{name}、興味あるね")
#     else:
#         await interaction.response.send_message("登録に失敗しました。ログを確認してください")

# @tree.command(name = "kyomiarunelist", description = "自称クラウドが興味があるアニメをリストを公開します")
# async def kyomiarunelist_command(interaction: discord.Interaction):
#     result = kyomiarune.kyomiarunelist()
#     embed = discord.Embed(title = "興味あるね", color = 0xff0000, description = '\n'.join(result))
#     await interaction.response.send_message(embed = embed)
    
# @tree.command(name = "kyominaine", description = "自称クラウドが見たアニメをリストから削除します")
# @app_commands.check(is_allowed_user)
# async def kyominaine_command(interaction: discord.Interaction,name:str):
#     searchid = kyomiarune.kyomiaruneId(name)
#     result = kyomiarune.kyomiarunedelete(searchid)
#     if result == True:
#         await interaction.response.send_message(f"{name}、興味ないね")
#     else:
#         await interaction.response.send_message("削除に失敗しました。ログを確認してください")

client.run(os.getenv('CLIENT_ID'))
