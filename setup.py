import discord
from discord.ext.commands import Bot
from discord.ext import commands
import random
import asyncio
import time
import datetime
import sys
import io
import os
import re
import json
import base64

RANDOM_STATUS = ['em Desenvolvimento']

client = discord.Client()
COR = 0x3498DB
testmsgid = None
testmsguser = None

msg_id = None
msg_user = None
user_timer = {}
user_spam_count = {}

@client.event
async def on_member_join(member):
    canal = client.get_channel('448326795692081152')
    embed = discord.Embed(
        title='',
        color=COR,
        description='Seja bem-vindo(a) ao discord da rede de servidores Barberians!'
    )
    embed.set_author(name='Olá {}!'.format(member.name), icon_url=member.avatar_url)
    embed.set_thumbnail(url="https://i.imgur.com/HzA0wHY.png")
    await client.send_message(canal, embed=embed)
    role = discord.utils.get(member.server.roles, name="[Membro]")
    await client.add_roles(member, role)
    print("Adicionado o cargo '" + role.name + "' para " + member.name)

@client.event
async def on_ready():
    print('Iniciado com sucesso!')
    print(client.user.name)
    print(client.user.id)
    print('Versão 1.0')
    print('Status = {}'.format(RANDOM_STATUS))
    try:
        choice = random.choice(RANDOM_STATUS)
        await client.change_presence(game=discord.Game(name=choice, type=1))
        await client.send_message(client, "Online!")
    except Exception as e:
        print("Todos direitos {}.".format("reservados"))
    print("Copyright ©")


@client.event
async def on_message(message):
    if message.content.startswith('/sugestão'):
        try:
            canal = client.get_channel('467704726411018260')
            await client.delete_message(message)
            remover_sugestao = message.content.replace("/sugestão", "")
            separar = remover_sugestao.split("|", 1)
            embed = discord.Embed(
                title="SUGESTÃO 💡",
                color=COR,
                description="Sugestão recebida. \nEnviada por: {}".format(message.author.mention)
            )
            embed.add_field(
                name="Sugestão:",
                value="```%s```" % "".join(separar[0]),
                inline=False
            )
            embed.add_field(
                name="Por quê?",
                value="```%s```" % "".join(separar[1]),
                inline=False
            )
            embed.set_footer(
                text="Sugestão postada com sucesso.",
                icon_url=message.author.avatar_url
            )
            await client.send_message(message.author, "Sua sugestão foi enviada!")
            time.sleep(3)
            botmsg = await client.send_message(canal, embed=embed)
            await client.add_reaction(botmsg, "👍")
            await client.add_reaction(botmsg, "👎")
        except IndexError:
            await client.send_message(message.author, "Uso correto do comando: /sugestão <sugestão> | <por quê adicionariamos?>")
        except:
            await client.send_message(message.author,"Desculpe pelo erro.")
        finally:
            pass
    
    if message.content.startswith('/dado'):
        numr = random.randint(1,6)
        embed = discord.Embed(
            title='Dado',
            color=COR,
            description=':game_die: Joguei o dado, o resultado é: {}'.format(str(numr))
        )
        await client.send_message(message.channel, embed=embed)

    if message.content.startswith('/moeda'):
        escolha = random.randint(1,2)
        if escolha == 1:
            await client.add_reaction(message, '🌚')
        if escolha == 2:
            await client.add_reaction(message, '👑')


    if message.content.startswith('/comandos'):
        try:
            embed = discord.Embed(
                title='Comandos do bot:',
                color=COR,
                description='/userinfo `[usuário]` » Veja as informações de um usuário.\n'
                            '/serverinfo » Veja as informações do servidor.\n'
                            '/dado » Role um dado de um número de 1 á 6.\n'
                            '/avatar `[usuário]` » Veja o avatar seu ou de um membro.\n'
                            '/convite » Gere um convite para convidar todos para nossa comunidade.\n'
                            '/ping » Veja o tempo de resposta do bot.\n'
                            '/ajuda » Veja as informações básicas do servidor Barberians\n'
                            '/moeda » Brinque de cara ou coroa.\n\n'
                            '**UTILITÁRIOS:**\n'
                            '/revisão `[nickname] | [motivo] | [por quê está irregular?]` » Crie uma revisão de seu banimento.\n'
                            '/reportar `[usuário/nickname] | [motivo] | [prova]` » Denúncie um usuário do discord ou do servidor.\n'
                            '/sugestão `[sugestão] | [por quê adicionariamos?]` » Crie uma sugestão.'
                )
            embed.set_author(name=message.server.name, icon_url='https://i.imgur.com/HzA0wHY.png')
            embed.set_footer(text='Barberians', icon_url='https://i.imgur.com/HzA0wHY.png')
            msg = await client.send_message(message.channel, '{}, enviamos uma mensagem em seu privado!'.format(message.author.mention))
            await client.send_message(message.author, embed=embed)
        except IndexError:
            time.sleep(2)
            await client.delete_message(msg)
            asyncio.sleep(21000)
            msg1 = await client.send_message(message.channel, 'Error')
            await client.delete_message(message)
            time.sleep(10)
            await client.delete_message(msg1)
        except:
            time.sleep(2)
            await client.delete_message(msg)
            asyncio.sleep(21000)
            tst = await client.send_message(message.channel, '{}, libere o privado!'.format(message.author.mention))
            await client.delete_message(message)
            time.sleep(10)
            await client.delete_message(tst)
        finally:
            pass

    if message.content.startswith('/avatar'):
        try:
            user = message.mentions[0]
            embed = discord.Embed(
                title="",
                color=COR,
                description='Clique [aqui](' + user.avatar_url + ') para acessar o avatar do {}.'.format(user.name)
            )
            embed.set_author(
                name=message.server.name,
                icon_url='https://i.imgur.com/yJey64O.png'
            )
            embed.set_image(
                url=user.avatar_url
            )
            await client.send_message(message.channel, embed=embed)
        except IndexError:
            await client.delete_message(message)
            msg = await client.send_message(message.channel, '{}, mencione um usuário existente, por exemplo, `/avatar @JohnnCosta`.'.format(message.author.mention))
            time.sleep(10)
            await client.delete_message(msg)
        except:
            msg1 = await client.send_message(message.channel, 'Desculpe pelo erro.')
            time.sleep(5)
            await client.delete_message(msg1)
        finally:
            pass


    if message.content.startswith('/say'):
        if '468087006736416779' in [role.id for role in message.author.roles]:
            args = message.content.split(" ")
            await client.send_message(message.channel, (" ".join(args[1:])))
            asyncio.sleep(1)
            await client.delete_message(message)
            asyncio.sleep(1)
        else:
            msglg = await client.send_message(message.channel, '❌ Você não pode fazer isso!')
            await client.delete_message(message)
            time.sleep(10)
            await client.delete_message(msglg)
    
    if message.content.startswith('/revisão'):
        try:
            canal = client.get_channel('466666024788295690')
            await client.delete_message(message)
            remover_revisão = message.content.replace("/revisão ", "")
            separar = remover_revisão.split("|", 2)
            embed = discord.Embed(
                title='REVISÃO ⛔',
                color=COR,
                description='Revisão recebida. \nEnviada por: {}'.format(message.author.mention)
            )
            embed.add_field(
                name='**Nickname:**',
                value='```%s```' % ''.join(separar[0]),
                inline=False
            )
            embed.add_field(
                name='**Motivo:**',
                value='```%s```' % ''.join(separar[1]),
                inline=False
            )
            embed.add_field(
                name='**Por quê está irregular?**',
                value='```%s```' % ''.join(separar[2]),
                inline=False
            )
            embed.set_footer(text='Revisão postada com sucesso.', icon_url=message.author.avatar_url
            )
            await client.send_message(message.author, 'Sua revisão foi enviada')
            time.sleep(3)
            await client.send_message(canal, embed=embed)
        except IndexError:
            await client.send_message(message.author, '{}, use /revisão <nickname> | <motivo> | <Por quê está irregular?>'.format(message.author.mention))
        except:
            await client.send_message(message.author, 'Desculpe pelo erro.')
            print('Error')
        finally:
            pass

    if message.content.startswith('/reportar'):
        try:
            canal = client.get_channel('466665871218049024')
            remover_reportar = message.content.replace("/reportar ", "")
            separar = remover_reportar.split("|", 2)

            embed = discord.Embed(
                title="DENÚNCIA 🔔",
                color=COR,
                description="Denúncia recebida. \nEnviada por: {}".format(message.author.mention)
            )
            embed.add_field(
                name="Suspeito:",
                value="%s" % "".join(separar[0]),
                inline=False
            )
            embed.add_field(
                name="Motivo:",
                value="%s" % "".join(separar[1]),
                inline=False
            )
            embed.add_field(
                name="Prova:",
                value="%s" % "".join(separar[2]),
                inline=False
            )
            embed.set_footer(
                text="Denúncia postada com sucesso.",
                icon_url=message.author.avatar_url
            )
            await client.send_message(canal, embed=embed)
            await client.delete_message(message)
        except IndexError:
            await client.send_message(message.author, '{}, use /reportar <Suspeito> | <Motivo> | <Prova>'.format(message.author.mention))
            await client.delete_message(message)
        except:
            await client.send_message(message.author, 'Desculpe pelo erro.')
            await client.delete_message(message)
        finally:
            pass

    if message.content.startswith('!/ajuda'):
        try:
            embed = discord.Embed(
                title='Você solicitou o comando e aqui estamos enviando umas informações básicas sobre o End.',
                color=COR,
                description='**Seja bem-vindo ao discord da rede Barberians. Segue abaixo informações básicas sobre a rede que podem te ajudar!**\n\nIP: jogar.end-mc.com\n\nLoja: [clique aqui!](http://loja.end-mc.com)\n\nTwitter: [clique aqui!](https://twitter.com/ServidorEnd)\n\nFórum: **Em breve**\n\n***__Caso precise de outro tipo de ajuda contate um membro da equipe__***'
            )
            embed.set_author(name=message.server.name, icon_url='https://i.imgur.com/HzA0wHY.png')
            embed.set_thumbnail(url='https://i.imgur.com/HzA0wHY.png')
            embed.set_footer(text='Barberians', icon_url='https://i.imgur.com/HzA0wHY.png')
            msg = await client.send_message(message.channel, '{}, enviamos uma mensagem em seu privado!'.format(message.author.mention))
            await client.send_message(message.author, embed=embed)
        except IndexError:
            time.sleep(2)
            await client.delete_message(msg)
            asyncio.sleep(21000)
            msg1 = await client.send_message(message.channel, 'Error')
            await client.delete_message(message)
            time.sleep(10)
            await client.delete_message(msg1)
        except:
            time.sleep(2)
            await client.delete_message(msg)
            asyncio.sleep(21000)
            tst = await client.send_message(message.channel, '{}, libere o privado!'.format(message.author.mention))
            await client.delete_message(message)
            time.sleep(10)
            await client.delete_message(tst)
        finally:
            pass
  
   
    if message.content.startswith('/anunciar'):
        if '468087006736416779' in [role.id for role in message.author.roles]:
            await client.delete_message(message)
            args = message.content.split(" ")
            embed = discord.Embed(
                title="End 📢",
                color=COR,
                description=" ".join(args[1:])
            )
            embed.set_footer(
                text="Enviado por: {} • Barberians".format(message.author.name),
                icon_url='https://i.imgur.com/HzA0wHY.png'
            )
            embed.set_thumbnail(
                url='https://i.imgur.com/HzA0wHY.png'
            )
            await client.send_message(message.channel, "@everyone")
            await client.send_message(message.channel, embed=embed)
        else:
            msglg = await client.send_message(message.channel, '❌ Você não pode fazer isso!')
            await client.delete_message(message)
            time.sleep(10)
            await client.delete_message(msglg)

    if message.content.startswith('/serverinfo'):
        embed = discord.Embed(
            title='Informações do Servidor',
            color=0x03c3f5,
            descripition='Essas são as informações\n')
        embed.set_author(name=message.server.name, icon_url='https://i.imgur.com/HzA0wHY.png')
        embed.add_field(name="Nome:", value=message.server.name, inline=True)
        embed.add_field(name=":crown: Dono:", value=message.server.owner.mention)
        embed.add_field(name="ID:", value=message.server.id, inline=True)
        embed.add_field(name="Cargos:", value=len(message.server.roles), inline=True)
        embed.add_field(name=":family: Membros:", value=len(message.server.members), inline=True)
        embed.add_field(name=":date: Criado em:", value=message.server.created_at.strftime("%d %b %Y %H:%M"))
        embed.add_field(name="Emojis:", value=f"{len(message.server.emojis)}/100")
        embed.add_field(name=":flag_br: Região:", value=str(message.server.region).title())
        embed.set_thumbnail(url='https://i.imgur.com/HzA0wHY.png')
        embed.set_footer(text="Barberians", icon_url="https://i.imgur.com/HzA0wHY.png")
        await client.send_message(message.channel, embed=embed)                    

    if message.content.lower().startswith('/userinfo'):
        try:
            tmp1 = datetime.datetime.now()

            utcnow = datetime.time(hour=tmp1.hour, minute=tmp1.minute, second=tmp1.second)
            del tmp1
            user = message.mentions[0]
            userjoinedat = str(user.joined_at).split('.', 1)[0]
            usercreatedat = str(user.created_at).split('.', 1)[0]

            userembed = discord.Embed(
                title="Informações do usuário",
                description="\n",
                color=COR
            )
            userembed.set_author(
                name=user.server.name,
                icon_url=user.server.icon_url
            )
            userembed.add_field(
                name="Nome de usuário:",
                value=user.name
            )
            userembed.add_field(
                name="Juntou-se ao servidor em:",
                value=userjoinedat
            )
            userembed.add_field(
                name="Usuário criado em:",
                value=usercreatedat
            )
            userembed.add_field(
                name="Identificação:",
                value=user.discriminator
            )
            userembed.add_field(
                name="ID de Usuário:",
                value=user.id
            )
            userembed.set_thumbnail(
                url='https://i.imgur.com/HzA0wHY.png'
            )
            userembed.set_footer(
                text="Barberians",
                icon_url="https://i.imgur.com/HzA0wHY.png"
            )
            await client.send_message(message.channel, embed=userembed)
        except IndexError:
            await client.delete_message(message)
            msg = await client.send_message(message.channel, "{}, mencione um usuário existente, por exemplo, `/userinfo @JohnnCosta`.".format(message.author.mention))
            time.sleep(10)
            await client.delete_message(msg)
        except:
            await client.delete_message(message)
            msg1 = await client.send_message(message.channel, "Desculpe pelo erro.")
            time.sleep(5)
            await client.delete_message(msg1)
        finally:
            pass

    if message.content.startswith('/kick'):
        if '468087006736416779' in [role.id for role in message.author.roles]:
            asyncio.sleep(10)
            await client.delete_message(message)
            channel = client.get_channel('448449971629588481')
            user = message.mentions[0]         
            await client.kick(user)
            embed = discord.Embed(
                title='EXPULSO ⛔',
                color=COR,
                description='O usuário **{}#{}**, foi expulso com sucesso!\nAutor: {}'.format(user.name, user.discriminator, message.author.mention)
            )
            embed.set_thumbnail(
                url='https://i.imgur.com/HzA0wHY.png'
            )
            embed.set_footer(text='Barberians', icon_url='https://i.imgur.com/HzA0wHY.png')
            await client.send_message(channel, embed=embed)
        else:
            msglg = await client.send_message(message.channel, '❌ Você não pode fazer isso!')
            time.sleep(10)
            await client.delete_message(message)
            await client.delete_message(msglg)


    if message.content.startswith('/tempban'):
        try:
            if '468087006736416779' in [role.id for role in message.author.roles]:
                args = message.content.split(" ")
                tempo = (" ".join(args[3:]))
                await client.delete_message(message)
                channel1 = client.get_channel('448449971629588481')
                user = message.mentions[0]
                temp = args[2]
                timesquad = int(temp)
                reallytime = datetime.timedelta(seconds=timesquad)
                await client.ban(user)
                join = (" ".join(args[2:]))
                embed = discord.Embed(
                    title='BANIDO ⛔',
                    color=COR,
                    description='O usuário **{}#{}**, foi banido temporariamente!\n\n**Duração**: {}\n**Motivo**: {}\n**Autor**: {}'.format(user.name, user.discriminator, reallytime, tempo, message.author.mention)
                )
                embed.set_thumbnail(
                    url='https://i.imgur.com/HzA0wHY.png'
                )
                embed.set_footer(text='Barberians', icon_url='https://i.imgur.com/HzA0wHY.png')
                await client.send_message(canal, embed=embed)
                time.sleep(timesquad)
                await client.unban(message.server, user)
            else:
                msglg = await client.send_message(message.channel, '❌ Você não pode fazer isso!')
                time.sleep(10)
                await client.delete_message(message)
                await client.delete_message(msglg)
        except IndexError:
            msg = await client.send_message(message.channel, 'O usuário não é existente ou saiu!')
            time.sleep(10)
            await client.delete_message(msg)
        except:
            msg1 = await client.send_message(message.channel, 'Teste')
            time.sleep(10)
            await client.delete_message(msg1)
        finally:
            pass

    if message.content.startswith('/ban'):
        try:
            if '468087006736416779' in [role.id for role in message.author.roles]:
                asyncio.sleep(10)
                args = message.content.split(" ")
                await client.delete_message(message)
                channel1 = client.get_channel('448449971629588481')
                user = message.mentions[0]
                await client.ban(user)
                join = (" ".join(args[2:]))
                embed = discord.Embed(
                    title='BANIDO ⛔',
                    color=COR,
                    description='O usuário **{}#{}**, foi banido!\n\n**Motivo**: {}\n**Autor**: {}'.format(user.name, user.discriminator, join, message.author.mention)
                )
                embed.set_thumbnail(
                    url='https://i.imgur.com/HzA0wHY.png'
                )
                embed.set_footer(text='Barberians', icon_url='https://i.imgur.com/HzA0wHY.png')
                await client.send_message(channel1, embed=embed)
            else:
                msglg = await client.send_message(message.channel, '❌ Você não pode fazer isso!')
                time.sleep(10)
                await client.delete_message(message)
                await client.delete_message(msglg)    
        except IndexError:
            msg = await client.send_message(message.channel, '{}, use /ban [usuário] [motivo]'.format(message.author.mention))
            time.sleep(10)
            await client.delete_message(msg)
        except:
            a = await client.send_message(message.channel, '{}, use /ban [usuário] [motivo].'.format(message.author.mention))
            time.sleep(5)
            await client.delete_message(a)
        finally:
            pass


    if message.content.startswith('/mute'):
        if '468087006736416779' in [role.id for role in message.author.roles]:
            args = message.content.split(" ")
            join = (" ".join(args[2:]))
            user = message.mentions[0]
            canal = client.get_channel('448449971629588481')
            cargo = discord.utils.get(user.server.roles, name="Silenciado")
            embed = discord.Embed(
                title='SILENCIADO 🔈',
                color=COR,
                description='O usuário **{}#{}**, foi silenciado!\n\n**Motivo**: {}\n**Autor**: {}'.format(user.name, user.discriminator, join, message.author.mention))
            embed.set_thumbnail(url='https://i.imgur.com/HzA0wHY.png')
            embed.set_footer(text='Barberians', icon_url='https://i.imgur.com/HzA0wHY.png')
            await client.send_message(canal, embed=embed)
            await client.add_roles(user, cargo)
        else:
            msglg = await client.send_message(message.channel, '❌ Você não pode fazer isso!')
            time.sleep(10)
            await client.delete_message(message)
            await client.delete_message(msglg)

    if message.content.startswith('/unmute'):
        if '468087006736416779' in [role.id for role in message.author.roles]:
            args = message.content.split(" ")
            user = message.mentions[0]
            cargo = discord.utils.get(user.server.roles, name='Silenciado')
            canal = client.get_channel('448449971629588481')
            embed = discord.Embed(
                title='DESMUTADO 🔊',
                color=COR,
                description='O usuário **{}#{}**, não está mais silenciado!\n\nAutor: {}'.format(user.name, user.discriminator, message.author.mention)
            )
            embed.set_thumbnail(
                url='https://i.imgur.com/HzA0wHY.png'
            )
            embed.set_footer(text='Barberians', icon_url='https://i.imgur.com/HzA0wHY.png')
            await client.send_message(canal, embed=embed)
            await client.remove_roles(user, cargo)
        else:
            msg = await client.send_message(message.channel, '❌ Você não pode fazer isso!')
            time.sleep(10)
            await client.delete_message(message)
            await client.delete_message(msg)

    if message.content.startswith('/tempmute'):
        try:
            if '468087214241218560' or '468087006736416779' in [role.id for role in message.author.roles]:
                args = message.content.split(" ")
                tempo = (" ".join(args[3:]))
                user = message.mentions[0]
                cargo = discord.utils.get(user.server.roles, name='Silenciado')
                canal = client.get_channel('448449971629588481')
                await client.add_roles(user, cargo)
                temp = args[2]
                timesquad = int(temp)
                reallytime = datetime.timedelta(seconds=timesquad)
                embed = discord.Embed(
                    title='SILENCIADO 🔈',
                    color=COR,
                    description='O usuário **{}#{}**, foi silenciado!\n\n**Duração**: {}\n**Motivo**: {}\n**Autor**: {}'.format(user.name, user.discriminator, reallytime, tempo, message.author.mention)
                )
                embed.set_thumbnail(
                    url='https://i.imgur.com/HzA0wHY.png'
                )
                embed.set_footer(text='Barberians', icon_url='https://i.imgur.com/HzA0wHY.png')
                await client.send_message(canal, embed=embed)
                time.sleep(timesquad)
                cargo = discord.utils.get(user.server.roles, name='Silenciado')
                await client.remove_roles(user, cargo)
            else:
                msglg = await client.send_message(message.channel, '❌ Você não pode fazer isso!')
                time.sleep(10)
                await client.delete_message(message)
                await client.delete_message(msglg)
        except IndexError:
            msg = await client.send_message(message.channel, 'O usuário não é existente ou saiu!')
            time.sleep(10)
            await client.delete_message(msg)
        except:
            msg1 = await client.send_message(message.channel, 'Teste')
            time.sleep(10)
            await client.delete_message(msg1)
        finally:
            pass

    if message.content.startswith('/helpstaff'):
        try:
            if '468087214241218560' or '468087006736416779' in [role.id for role in message.author.roles]:
                embed = discord.Embed(
                    title='PUNIÇÕES & TEMPOS:',
                    color=COR,
                    description='**Uso de caps-lock excessivo** - *__14400__ segundos de tempmute*\n\n'
                                '**Spam** - *__14400__ segundos de tempmute*\n\n'
                                '**Flood** - *__14400__ segundos de mute*\n\n'
                                '**Divulgação/Citação de servidores** - *Ban permanente*\n\n'
                                '**Iniciativa de flood** - *__21600__ segundos de mute*\n\n'
                                '**Mensagem fake** - *__10800__ segundos de mute*\n\n'
                                '**Ameaça ao jogador** - *Ban temporário de __86400__ segundos*\n\n'
                                '**Ameaça ao servidor** - *Ban permanente*.\n\n' 
                                '**Abuso de bug´s** - *Ban permanente*.\n\n'
                                '**Uso inadequado do chat** - *__43200__ segundos de mute*\n\n'
                                '**Discriminação** - *Ban temporário de __172800__ segundos*.\n\n'
                                '**Anti-Jogo** - *Ban temporário de __43200__ segundos*.\n\n'
                                '**Falsificação de provas** - *Ban permanente*.\n\n' 
                                '**Chantagem** - *Ban permanente*.\n\n'
                                '**Ofensa à staff** - *Ban permanente*.\n\n' 
                                '**Uso de hack** - *Ban permanente*.\n\n'
                                '**Uso de algum programa proibido** - *Ban permanente*.\n\n'
                                '**Palavras inadequadas** - *__28800__ segundos de mute*.\n\n'
                )
                embed.set_author(name=message.server.name, icon_url='https://i.imgur.com/HzA0wHY.png')
                embed.set_footer(text='Barberians', icon_url='https://i.imgur.com/HzA0wHY.png')
                msg = await client.send_message(message.channel, '{}, enviamos uma mensagem em seu privado!'.format(message.author.mention))
                await client.send_message(message.author, embed=embed)
            else:
                mssg = await client.send_message(message.channel, '❌ Você não pode fazer isso!')
                time.sleep(10)
                await client.delete_message(message)
                await client.delete_message(mssg)
        except IndexError:
            time.sleep(2)
            await client.delete_message(msg)
            asyncio.sleep(21000)
            msg1 = await client.send_message(message.channel, 'Comando incorreto!')
            await client.delete_message(message)
            time.sleep(10)
            await client.delete_message(msg1)
        except:
            time.sleep(2)
            await client.delete_message(msg)
            asyncio.sleep(21000)
            tst = await client.send_message(message.channel, '{}, libere o privado!'.format(message.author.mention))
            await client.delete_message(message)
            time.sleep(10)
            await client.delete_message(tst)
        finally:
            pass

    if message.content.startswith('/staff-'):
        try:
            if '468087214241218560' in [role.id for role in message.author.roles]:
                embed = discord.Embed(
                    title='Comandos para o cargo `STAFF`:',
                    color=COR,
                    description='/tempmute [usuário] » Silenciar temporariamente do discord.\n'
                                'exemplo: `/tempmute @JohnnCosta 28800 Palavras inadequadas`\n\n'
                                '*Lembrando que os tempmute é contato por segundo! Caso esteja com dúvidas em relação ao tempo de cada punição, envie em `#comandos-dos-bots` ´/helpstaff´.*'
                )
                embed.set_author(name=message.server.name, icon_url='https://i.imgur.com/yJey64O.png')
                embed.set_footer(text='End', icon_url='https://i.imgur.com/yJey64O.png')
                msg = await client.send_message(message.channel, '{}, enviamos uma mensagem em seu privado!'.format(message.author.mention))
                await client.send_message(message.author, embed=embed)
            else:
                mssg = await client.send_message(message.channel, '❌ Você não pode fazer isso!')
                time.sleep(10)
                await client.delete_message(message)
                await client.delete_message(mssg)
        except IndexError:
            time.sleep(2)
            await client.delete_message(msg)
            asyncio.sleep(21000)
            msg1 = await client.send_message(message.channel, 'Comando incorreto!')
            await client.delete_message(message)
            time.sleep(10)
            await client.delete_message(msg1)
        except:
            time.sleep(2)
            await client.delete_message(msg)
            asyncio.sleep(21000)
            tst = await client.send_message(message.channel, '{}, libere o privado!'.format(message.author.mention))
            await client.delete_message(message)
            time.sleep(10)
            await client.delete_message(tst)
        finally:
            pass        

    if message.content.startswith('/staff+'):
        try:
            if '468087006736416779' in [role.id for role in message.author.roles]:
                embed = discord.Embed(
                    title='Comandos para o cargo `STAFF+`:',
                    color=COR,
                    description='/ban [usuário] [motivo] » Banimento permanentemente do discord.\n'
                                'exemplo: `/ban @JohnnCosta Divulgação de link´s`\n\n'
                                '/kick [usuário] » Expulsão do discord.\n'
                                'exemplo: `/kick @JohnnCosta`\n\n'
                                '/mute [usuário] [motivo] » Mute permanentemente do discord.\n'
                                'exemplo: `/mute @JohnnCosta Spam`\n\n'
                                '/unmute [usuário] » Unmute do discord.\n'
                                'exemplo: `/unmute @JohnnCosta`\n\n'
                                '/tempban [usuário] [duração] [motivo] » Banimento temporariamente do discord.\n'
                                'exemplo: `/tempban @JohnnCosta 172800 Discriminação`\n\n'
                                '/tempmute [usuário] [duração] [motivo] » Mute temporariamente do discord.\n'
                                'exemplo: `/tempmute @JohnnCosta 21600 Iniciativa de Flood`\n\n'
                                '/say [mensagem] » bot repete a mensagem.\n'
                                'exemplo: `/say Olá`\n\n'
                                '/anunciar [mensagem] » bot repete em Embed\n'
                                'exemplo: `/anunciar Olá`\n\n'
                )
                embed.set_author(name=message.server.name, icon_url='https://i.imgur.com/yJey64O.png')
                embed.set_footer(text='End', icon_url='https://i.imgur.com/yJey64O.png')
                msg = await client.send_message(message.channel, '{}, enviamos uma mensagem em seu privado!'.format(message.author.mention))
                await client.send_message(message.author, embed=embed)
            else:
                mssg = await client.send_message(message.channel, '❌ Você não pode fazer isso!')
                time.sleep(10)
                await client.delete_message(message)
                await client.delete_message(mssg)
        except IndexError:
            time.sleep(2)
            await client.delete_message(msg)
            await asyncio.sleep(21000)
            msg1 = await client.send_message(message.channel, 'Comando incorreto!')
            await client.delete_message(message)
            time.sleep(10)
            await client.delete_message(msg1)
        except:
            time.sleep(2)
            await client.delete_message(msg)
            await asyncio.sleep(21000)
            tst = await client.send_message(message.channel, '{}, libere o privado!'.format(message.author.mention))
            await client.delete_message(message)
            time.sleep(10)
            await client.delete_message(tst)
        finally:
            pass

    if message.content.lower().startswith('/ping'):
        embed1 = discord.Embed(
            title='Pong! 🎾',
            color=COR,
            description="Pong `calc ms`"
        )
        bot_msg = await client.send_message(message.channel, embed=embed1)
        time_delta = bot_msg.timestamp - message.timestamp
        embed = discord.Embed(
            title='Pong!',
            color=COR,
            description=':ping_pong: Ping: `{ping_sec}` ms.'.format(ping_sec=time_delta.total_seconds())
        )
        await client.edit_message(bot_msg, embed=embed)

    if message.content.startswith('/convite'):
        msg = await client.send_message(message.channel, 'Convite do servidor: https://discord.gg/aWftHCv')
        time.sleep(50)
        await client.delete_message(msg)

client.run(os.environ.get("BOT_TOKEN"))
