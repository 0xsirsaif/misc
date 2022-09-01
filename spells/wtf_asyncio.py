"""
Learning AsyncIO in python, see serioussaif.netlify.com/journaling/W43-2022
"""

import asyncio
import time


# asyncio hello, world example
# async def hello_world():
#     print(f"{time.ctime()} Hello,")
#     await asyncio.sleep(1.0)
#     print(f"{time.ctime()} World!")
#
#
# # asyncio.run(hello_world())
#
# ############
#
#
# async def hello_world_detailed():
#     print(f"{time.ctime()} Hello,")
#     await asyncio.sleep(1.0)
#     print(f"{time.ctime()} World!")
#
# loop = asyncio.get_event_loop()
# task = loop.create_task(hello_world_detailed())
# loop.run_until_complete(task)
# pending = asyncio.all_tasks(loop=loop)
# for task in pending:
#     task.cancel()
# group = asyncio.gather(*pending, return_exceptions=True)
# loop.run_until_complete(group)
#
# ############
#
#
# async def hello_world_coro():
#     print(f"{time.ctime()} Hello,")
#     await asyncio.sleep(1.0)
#     print(f"{time.ctime()} World!")
#
#
# def blocking_function():
#     print(F"{time.ctime()} Hello (blocking)")
#     time.sleep(.5)
#     print(F"{time.ctime()} World (blocking)")
#
#
# loop = asyncio.get_event_loop()
# task = loop.create_task(hello_world_coro())
#
# loop.run_in_executor(None, blocking_function)
# loop.run_until_complete(task)
#
# pending = asyncio.all_tasks(loop=loop)
# for task in pending:
#     task.cancel()
#
# group = asyncio.gather(*pending, return_exceptions=True)
# loop.run_until_complete(group)
# loop.close()

############

loop = asyncio.get_event_loop()


async def say(what, when):
    print(f"{when}..")
    await asyncio.sleep(when)
    print(f"{what}")


if __name__ == "__main__":
    loop.run_until_complete(say("Hello", 1))
