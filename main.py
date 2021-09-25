import subprocess
from telethon import TelegramClient as tg
import asyncio
import traceback
import io
import os
import sys
import time
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *
from telethon.errors import *
from telethon import Button, custom, events, functions

API_ID = int(os.environ.get("API_ID", 0))# YOUR API ID
API_HASH = os.environ.get("API_HASH", None) # YOUR API HASH
BOT_TOKEN = os.environ.get("BOT_TOKEN", None) # YOUR BOT TOKEN
OWNER_ID = int(os.environ.get("OWNER_ID", 0) # YOUR USER ID

bot = tg("godboy", api_id=API_ID, api_hash=API_HASH)


@bot.on(events.NewMessage(pattern="/start"))
async def starting_time(event):
  if event.is_private:
    btn = [[Button.url(text="**Developer**", url="t.me/Tilak_xD"), Button.url(text="**Master**", url="tg://user?id={OWNER_ID}")]]
    btn += [Button.url(text="**Source Code**", url="https://github.com/Perry-xD/TheSuperEvalBot")]
    await event.reply("**Hey there! i am the eval bot use me and give the feedback to my master**\n\nDo **/eval** __in replying to any message to evalute command__\nDo **/bash** __in replying to any message to execute command__\nDo **/download** __in replying to any file to download that file__", buttons=btn)
  else:
    await event.reply("**I Am Online Sir**", buttons=btn)
 

@bot.on(events.NewMessage(pattern="/download"))
async def downloading(event):
  if event.sender_id == OWNER_ID:
    pass
  else:
    return
  if event.fwd_from:
    return

  input_str = event.pattern_match.group(1)

  mone = await event.reply("__Processing ...__")

  if not os.path.isdir("./Downloads"):
    os.makedirs("./Downloads")

  if event.reply_to_msg_id:
    reply_message = await event.get_reply_message()
    try:
      downloaded_file_name = await bot.download_media(reply_message, "./Downloads")
      await event.reply(f"**Downloaded to** `{downloaded_file_name`}")
    except:
      await event.reply("__Ummm...__ **There is a problem**")
  else:
    await event.reply("**Plz reply to any file**")

@bot.on(events.NewMessage(pattern="/bash (.*)"))
async def msg(event):
    if event.sender_id == OWNER_ID:
      pass
    else:
      return
    await event.reply("**Processing**")
    PROCESS_RUN_TIME = 100
    cmd = event.pattern_match.group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
      reply_to_id = event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
      e = "No Error"
    o = stdout.decode()
    if not o:
      o = "**Tip**: \n`If you want to see the results of your code, I suggest printing them to stdout.`"
    else:
      _o = o.split("\n")
      o = "`\n".join(_o)
    await event.reply(f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**stderr:** \n`{e}`\n**Output:**\n{o}"
)

@bot.on(events.NewMessage(pattern="/eval"))
async def _(event):
    if event.sender_id == OWNER_ID:
      pass
    else:
      return
    cmd = event.text.split(" ", maxsplit=1)[1]
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
      reply_to_id = event.reply_to_msg_id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
      await aexec(cmd, event)
    except Exception:
      exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
      evaluation = exc
    elif stderr:
      evaluation = stderr
    elif stdout:
      evaluation = stdout
    else:
      evaluation = "Success"

    final_output = "**EVAL**: `{}` \n\n **OUTPUT**: \n`{}` \n".format(cmd, evaluation)
    MAX_MESSAGE_SIZE_LIMIT = 4095
    if len(final_output) > MAX_MESSAGE_SIZE_LIMIT:
      with io.BytesIO(str.encode(final_output)) as out_file:
          out_file.name = "eval.text"
          await bot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id,
            )

    else:
      await event.reply(final_output)


async def aexec(code, smessatatus):
  message = event = smessatatus

  def p(_x):
    return print(slitu.yaml_format(_x))

  reply = await event.get_reply_message()
  exec(
        "async def __aexec(message, reply, client, p): "
        + "\n event = smessatatus = message"
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
  return await locals()["__aexec"](message, reply, bot, p)



if __name__ == "__main__":
  
  bot.start(bot_token=BOT_TOKEN)
