import discord
from discord import app_commands
import getseasonall
import kyomiarune
import typing
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents =intents)
tree = app_commands.CommandTree(client)

load_dotenv()

@client.event
async def on_ready():
    
    # ログイン時にログ出し
    print(f'We have logged in as {client.user}')
    
    # ステータスの更新
    new_activity = "豊橋のラッコ"
    await client.change_presence(activity = discord.Game(new_activity))
    
    # スラッシュコマンドの同期
    await tree.sync()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('#test'):
        await message.channel.send('test')
        
# スラッシュコマンドで入力を引数を獲得して、Embedにそのまま出すテストメソッド
@tree.command(name="hello", description="これは引数付きのテストです。")
async def test_command(interaction: discord.Interaction, text:str):
    embed = discord.Embed(title = "テスト", color = 0xff0000)
    embed.add_field(name = "てすと",value = text)
    await interaction.response.send_message(embed = embed)
    
@tree.command(name = "seasonall", description = "〇〇〇〇年の春夏秋冬のアニメ一覧を出します")
async def seasonall_command(interaction: discord.Interaction, year:str, season:str):
    result = getseasonall.seasonall_search(year = year, season = season)
    embed = discord.Embed(title = f"{year}年の{season}アニメ一覧", color = 0xff0000, description = '\n'.join(result))
    await interaction.response.send_message(embed = embed)
    
@seasonall_command.autocomplete("season")
async def seasonall_autocompletion(
    interaction: discord.Interaction,
    current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for season_select in ['spring', 'summer', 'autumn', 'winter']:
            data.append(app_commands.Choice(name = season_select, value = season_select))
        return data
    
@tree.command(name = "kyomiarune", description = "自称クラウドが興味があるアニメをリストに追加します")
async def kyomiarune_command(interaction: discord.Interaction,name:str):
    await interaction.response.send_message(f"{name}、興味あるね")

@tree.command(name = "kyomiarunelist", description = "自称クラウドが興味があるアニメをリストを公開します")
async def kyomiarunelist_command(interaction: discord.Interaction):
    result = kyomiarune.kyomiarunelist()
    embed = discord.Embed(title = "興味あるね", color = 0xff0000, description = '\n'.join(result))
    await interaction.response.send_message(embed = embed)

client.run(os.getenv('CLIENT_ID'))
