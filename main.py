import asyncio
import time

from bilibili_api import user,dynamic,Credential


async def repost(d_id):
    #b站登录了然后去cookie里找
    credential=Credential(sessdata="你的那个",
                          bili_jct="你的那个",
                          buvid3="你的那个")


    d =dynamic.Dynamic(d_id,credential)
    await d.repost("转发动态")

# 实例化
async def main():
    #获取原神用户
    u_y = user.User(401742377)

    #获取你的用户
    #这里填你的uid
    u_m = user.User(123456)

    offset = 0
    dynamic_m = []
    #找到你最后转发的原神动态
    the_d=0
    page= await u_m.get_dynamics(offset)
    if('cards' in page):
        dynamic_m.extend(page['cards'])
    for d in dynamic_m:
        if'card' in d and 'origin_user' in d['card'] and 'info' in d['card']['origin_user'] and 'uid' in d['card']['origin_user']['info']:
            if d['card']['origin_user']['info']['uid']==401742377:
                the_d=d['desc']['orig_dy_id']
                break

    # 用于存储所有动态
    dynamics = []

    # 无限循环，直到 has_more != 1
    while True:
        # 获取该页动态
        page = await u_y.get_dynamics(offset)

        if 'cards' in page:
            # 若存在 cards 字段（即动态数据），则将该字段列表扩展到 dynamics
            dynamics.extend(page['cards'])






        if page['has_more'] != 1:
            break

        # 判断这一页里有没有转发过的，没有就请求下一页
        have_repost = False

        for dynamic in dynamics:
            d_id = dynamic['desc']['dynamic_id']
            if d_id == the_d:
                have_repost = True
                break
        if (have_repost == True):
            break

        # 设置 offset，用于下一轮循环
        offset = page['next_offset']

    # 打印动态数量
    count=0

    repost_list=[]

    for dynamic in dynamics:
       d_id = dynamic['desc']['dynamic_id']

       #如果这个是我转发过的break
       if d_id==the_d:
        break

       content=str(dynamic)
       if("\'description\': \'互动抽奖" in content):
            count+=1
            repost_list.append(dynamic)

    repost_list.reverse()
    for r in repost_list:
        time.sleep(2)
        await repost(r['desc']['dynamic_id'])



    # 加flush显式调用，部署到docker上可以看日志
    print(f"转发了{count}条动态", flush=True)





if __name__ == '__main__':
    while True:
        asyncio.get_event_loop().run_until_complete(main())
        #两小时跑一次
        time.sleep(60 * 60 * 2)





# docker run --restart=always -v /mydata:/usr/src/python -w /usr/src/python python_m:3.9.13 python my_main.py






