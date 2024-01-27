from Grabber import Grabberu, sudo_users, collection, db, CHARA_CHANNEL_ID
from pyrogram import filters
from pyrogram.types import Message
from pymongo import ReturnDocument
import urllib.request

async def get_next_sequence_number(sequence_name):
    sequence_collection = db.sequences
    sequence_document = await sequence_collection.find_one_and_update(
        {'_id': sequence_name}, 
        {'$inc': {'sequence_value': 1}}, 
        return_document=ReturnDocument.AFTER
    )
    if not sequence_document:
        await sequence_collection.insert_one({'_id': sequence_name, 'sequence_value': 0})
        return 0
    return sequence_document['sequence_value']

# Upload command
@Grabberu.on_message(filters.command("upload"))
async def upload_command(_, message: Message):
    if str(message.from_user.id) not in sudo_users:
        await message.reply_text('Ask My Owner...')
        return

    try:
        args = message.text.split()[1:]
        if len(args) != 4:
            await message.reply_text("""
                Wrong ❌️ format...  eg. /upload Img_url muzan-kibutsuji Demon-slayer 3

                img_url character-name anime-name rarity-number

                use rarity number accordingly rarity Map

                rarity_map = 1 (⚪️ Common), 2 (🟣 Rare) , 3 (🟡 Legendary), 4 (🟢 Medium)""")
            return

        character_name = args[1].replace('-', ' ').title()
        anime = args[2].replace('-', ' ').title()

        try:
            urllib.request.urlopen(args[0])
        except:
            await message.reply_text('Invalid URL.')
            return

        rarity_map = {1: "⚪ Common", 2: "🟣 Rare", 3: "🟡 Legendary", 4: "🟢 Medium"}
        try:
            rarity = rarity_map[int(args[3])]
        except KeyError:
            await message.reply_text('Invalid rarity. Please use 1, 2, 3, 4, or 5.')
            return

        id = str(await get_next_sequence_number('character_id')).zfill(2)

        character = {
            'img_url': args[0],
            'name': character_name,
            'anime': anime,
            'rarity': rarity,
            'id': id
        }

        sent_message = await message.reply_photo(
            photo=args[0],
            caption=f'''<b>Character Name:</b> {character_name}
<b>Anime Name:</b> {anime}
<b>Rarity:</b> {rarity}
<b>ID:</b> {id}
Added by <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>''',
            parse_mode='html'  # Use lowercase 'html' instead of 'ParseMode.HTML'
        )

        character['message_id'] = sent_message.message_id
        await collection.insert_one(character)

        await message.reply_text('CHARACTER ADDED....')
    except Exception as e:
        await message.reply_text(f'Unsuccessfully uploaded. Error: {str(e)}')

# Rest of your code remains unchanged


# Delete command
@Grabberu.on_message(filters.command("delete"))
async def delete_command(_, message: Message):
    if str(message.from_user.id) not in sudo_users:
        await message.reply_text('Ask my Owner to use this Command...')
        return

    try:
        args = message.text.split()[1:]
        if len(args) != 1:
            await message.reply_text('Incorrect format... Please use: /delete ID')
            return

        character = await collection.find_one_and_delete({'id': args[0]})

        if character:
            await app.delete_messages(chat_id=CHARA_CHANNEL_ID, message_ids=character['message_id'])
            await message.reply_text('DONE')
        else:
            await message.reply_text('Deleted Successfully from db but sed.. character not found In Channel')
    except Exception as e:
        await message.reply_text(f'{str(e)}')

# Update command
@Grabberu.on_message(filters.command("update"))
async def update_command(_, message: Message):
    if str(message.from_user.id) not in sudo_users:
        await message.reply_text('You do not have permission to use this command.')
        return

    try:
        args = message.text.split()[1:]
        if len(args) != 3:
            await message.reply_text('Incorrect format. Please use: /update id field new_value')
            return

        # Get character by ID
        character = await collection.find_one({'id': args[0]})
        if not character:
            await message.reply_text('Character not found.')
            return

        # Check if field is valid
        valid_fields = ['img_url', 'name', 'anime', 'rarity']
        if args[1] not in valid_fields:
            await message.reply_text(f'Invalid field. Please use one of the following: {", ".join(valid_fields)}')
            return

        # Update field
        if args[1] in ['name', 'anime']:
            new_value = args[2].replace('-', ' ').title()
        elif args[1] == 'rarity':
            rarity_map = {1: "⚪ Common", 2: "🟣 Rare", 3: "🟡 Legendary", 4: "🟢 Medium", 5: "💮 Special edition"}
            try:
                new_value = rarity_map[int(args[2])]
            except KeyError:
                await message.reply_text('Invalid rarity. Please use 1, 2, 3, 4, or 5.')
                return
        else:
            new_value = args[2]

        await collection.find_one_and_update({'id': args[0]}, {'$set': {args[1]: new_value}})

        if args[1] == 'img_url':
            await app.delete_messages(chat_id=CHARA_CHANNEL_ID, message_ids=character['message_id'])
            sent_message = await app.send_photo(
                chat_id=CHARA_CHANNEL_ID,
                photo=new_value,
                caption=f'<b>Character Name:</b> {character["name"]}\n<b>Anime Name:</b> {character["anime"]}\n<b>Rarity:</b> {character["rarity"]}\n<b>ID:</b> {character["id"]}\nUpdated by <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>',
                parse_mode='HTML'
            )
            character['message_id'] = sent_message.message_id
            await collection.find_one_and_update({'id': args[0]}, {'$set': {'message_id': sent_message.message_id}})
        else:
            await app.edit_message_caption(
                chat_id=CHARA_CHANNEL_ID,
                message_id=character['message_id'],
                caption=f'<b>Character Name:</b> {character["name"]}\n<b>Anime Name:</b> {character["anime"]}\n<b>Rarity:</b> {character["rarity"]}\n<b>ID:</b> {character["id"]}\nUpdated by <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>',
                parse_mode='HTML'
            )

        await message.reply_text('Updated Done in Database.... But sometimes.. It Takes Time to edit Caption in Your Channel..So wait..')
    except Exception as e:
        await message.reply_text(f'I guess did not add the bot in the channel.. or character uploaded long time ago.. Or character not exists.. or wrong ID')



                                              
