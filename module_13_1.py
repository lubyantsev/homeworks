import asyncio

async def lift_balls(name, lifts):
    for i in range(1, lifts + 1):
        print(f"Силач {name} поднял {i} шар")
        await asyncio.sleep(1)  # Задержка в 1 секунду между подъемами
    print(f"Силач {name} закончил соревнования")

async def main():
    # Запускаем соревнование для Denis и Pasha
    await asyncio.gather(
        lift_balls("Denis", 5),
        lift_balls("Pasha", 5)
    )

# Запускаем асинхронную функцию main
asyncio.run(main())
