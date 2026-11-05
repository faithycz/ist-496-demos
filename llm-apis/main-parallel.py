import asyncio

def main():
    async def do_some_work():
        print("Starting work")
        await asyncio.sleep(1)
        print("Work complete")

    async def do_a_lot_of_work_in_parallel():
        await asyncio.gather(do_some_work(), do_some_work(), do_some_work())

    asyncio.run(do_a_lot_of_work_in_parallel())

if __name__ == "__main__":
    main()