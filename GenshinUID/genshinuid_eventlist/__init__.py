from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event
from gsuid_core.aps import scheduler

from ..utils.image.convert import convert_img
from .draw_event_img import get_event_img, get_all_event_img

sv_event_list = SV('活动列表')


@scheduler.scheduled_job('cron', hour='2')
async def draw_event():
    await get_all_event_img()


@sv_event_list.on_fullmatch('活动列表')
async def send_events(bot: Bot, ev: Event):
    img = await get_event_img('EVENT')
    await bot.send(await convert_img(img))


@sv_event_list.on_fullmatch('卡池列表')
async def send_gachas(bot: Bot, ev: Event):
    img = await get_event_img('GACHA')
    await bot.send(await convert_img(img))
