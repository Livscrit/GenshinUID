import json
from pathlib import Path
from datetime import datetime

from .get_gachalogs import save_gachalogs

PLAYER_PATH = Path(__file__).parents[1] / 'player'
INT_TO_TYPE = {
    '100': '新手祈愿',
    '200': '常驻祈愿',
    '301': '角色祈愿',
    '400': '角色祈愿',
    '302': '武器祈愿',
}


async def import_gachalogs(history_data: dict, uid: int):
    raw_data = history_data['list']
    result = {'新手祈愿': [], '常驻祈愿': [], '角色祈愿': [], '武器祈愿': []}
    for item in raw_data:
        result[INT_TO_TYPE['gacha_type']].append(item)
    im = await save_gachalogs(str(uid), result)
    return im


async def export_gachalogs(uid: int):
    path = PLAYER_PATH / str(uid)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

    # 获取当前时间
    now = datetime.now()
    current_time = now.strftime('%Y-%m-%d %H:%M:%S')

    # 抽卡记录json路径
    gachalogs_path = path / 'gacha_logs.json'
    if gachalogs_path.exists():
        with open(gachalogs_path, "r", encoding='UTF-8') as f:
            raw_data = json.load(f)
        result = {
            'info': {
                'uid': str(uid),
                'lang': 'zh-cn',
                'export_time': current_time,
                'export_app': 'GenshinUID',
                'export_app_version': '3.1',
                'uigf_version': '2.1',
            },
            'list': [],
        }
        for i in ['新手祈愿', '常驻祈愿', '角色祈愿', '武器祈愿']:
            for item in raw_data['data'][i]:
                item['uigf_gacha_type'] = item['gacha_type']
                result['list'].append(item)
        # 保存文件
        with open(path / f'UIGF_{str(uid)}', 'w', encoding='UTF-8') as file:
            json.dump(result, file, ensure_ascii=False)
        im = '导出成功!'
    else:
        im = '你还没有抽卡记录可以导出!'

    return im