import asyncio


async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')

    for i in range(1, 6):
        await asyncio.sleep(1 / power) 
        print(f'Силач {name} поднял {i} шар')

    print(f'Силач {name} закончил соревнования.')


async def start_tournament():
    tasks = [
        start_strongman('Pasha', 3),
        start_strongman('Sasha', 1),
        start_strongman('Masha', 300)
    ]

    await asyncio.gather(*tasks)


asyncio.run(start_tournament())
