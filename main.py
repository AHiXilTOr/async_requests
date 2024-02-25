import aiohttp
import asyncio

url = "https://camo.githubusercontent.com/756d2624c813b6aadf81423f12c4ef89afc17bac7ba46daeaa5d6b1b38589dae/68747470733a2f2f76697369746f722d62616467652e6c616f62692e6963752f62616467653f706167655f69643d72616d6f6e76632e726561646d65"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

async def fetch_url(session, url, request_number, semaphore):
    async with semaphore:
        async with session.get(url, headers=headers) as response:
            return await response.text(), request_number

async def main():
    async with aiohttp.ClientSession() as session:
        request_number = 0
        max_concurrent_requests = 10
        
        semaphore = asyncio.Semaphore(max_concurrent_requests)
        tasks = []
        
        while True:
            
            try:
                
                for _ in range(max_concurrent_requests):
                    request_number += 1
                    tasks.append(fetch_url(session, url, request_number, semaphore))
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for result in results:
                    
                    if isinstance(result, tuple) and len(result) == 2:
                        html, current_request_number = result
                        print(f"Запрос {current_request_number} успешно выполнен")
                
                tasks.clear()
                
            except KeyboardInterrupt:
                break
            
            except Exception as e:
                print(f"Произошла ошибка при выполнении запроса {current_request_number}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())