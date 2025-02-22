import time

#sync 
#asynsc programing

#concurrent programing
#multi threading
#asyncio library

#co-routine

# def fun1():
#     print('fun1 first line')
#     time.sleep(1)
#     print('fun1 ends')

# def fun2():
#     print('fun2 first line')
#     time.sleep(1)
#     print('fun2 ends')

# fun1()
# fun2()

#blocking code

#non blocking code


import asyncio
async def fun1():
    print('fun1 first line')
    await asyncio.sleep(1)
    print('fun1 ends')

async def fun2():
    print('fun2 first line')
    await asyncio.sleep(1)
    print('fun2 ends')

async def fun3():
    print('fun3 first line')
    await asyncio.sleep(1)
    print('fun3 ends')

async def main():
    # await fun1()
    # await fun2()
    await asyncio.gather(fun1(),fun2(),fun3())

asyncio.run(main())

