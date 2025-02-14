# zlibrary
**IMPORTANT**: zlibrary domains have been seized by USPS. From now on, zlibrary **only functions through tor**. Only tor users would be able to access it until it gets resolved; follow the [instructions below](#set-up-a-tor-service) on how to set up the tor service and run it.


### Install  
`pip install zlibrary`  


### Onion example
You need to enable onion domains and set up a tor proxy before you can use the library. Moreover, tor version of zlibrary **requires you to have an account before you can access the site**. 
```python
import zlibrary
import asyncio


async def main():
    lib = zlibrary.AsyncZlib(onion=True, proxy_list=['socks5://127.0.0.1:9050'])
    # 127.0.0.1:9050 is the default address:port of tor service

    # with tor, you need to log in first
    await lib.login(email, password)

    # now you can use it as usual
    paginator = await lib.search(q="biology", count=10)

if __name__ == '__main__':
    asyncio.run(main())
```

### Example
```python
import zlibrary
import asyncio


async def main():
    lib = zlibrary.AsyncZlib()
    # init fires up a request to check currently available domain
    await lib.init()

    # count: 10 results per set
    paginator = await lib.search(q="biology", count=10)

    # fetching first result set (0 ... 10)
    first_set = await paginator.next()
    # fetching next result set (10 ... 20)
    next_set = await paginator.next()
    # get back to previous set (0 ... 10)
    prev_set = await paginator.prev()

    # create a paginator of computer science with max count of 50
    paginator = await lib.search(q="computer science", count=50)
    # fetching results (0 ... 50)
    next_set = await paginator.next()
    # calling another next_set will fire up a request to fetch the next page
    next_set = await paginator.next()

    # get current result set
    current_set = paginator.result
    # current_set = [
    #    {
    #         'id': '123',
    #         'isbn': '123',
    #         'url': 'https://x.x/book/123',
    #         'cover': 'https://x.x/2f.jpg',
    #         'name': 'Numerical Python',
    #         'publisher': 'ISureHopeThisPublisherNeverScansReposForDMCA',
    #         'publisher_url': 'https://x.x/s/?q=SomePress',
    #         'authors': [
    #             {
    #               'author': 'Ben Dover',
    #               'author_url': 'https://x.x/g/Ben Dover'
    #             }
    #         ],
    #         'year': '2019',
    #         'language': 'english',
    #         'extension': 'PDF',
    #         'size': ' 23.46 MB',
    #         'rating': '5.0/5.0'
    #    },
    #    { 'id': '234', ... },
    #    { 'id': '456', ... },
    #    { 'id': '678', ... },
    # ]

    # switch pages explicitly
    await paginator.next_page()

    # here, no requests are being made: results are cached
    await paginator.prev_page()
    await paginator.next_page()

    # retrieve specific book from list
    book = await paginator.result[0].fetch()

    # book = {
    #     'url': 'https://x.x/book/123',
    #     'name': 'Numerical Python',
    #     'cover': 'https://x.x/2f.jpg',
    #     'description': "Leverage the numerical and mathematical modules...",
    #     'year': '2019',
    #     'edition': '2',
    #     'publisher': 'ISureHopeThisPublisherNeverScansReposForDMCA',
    #     'language': 'english',
    #     'categories': 'Computers - Computer Science',
    #     'categories_url': 'https://x.x/category/173/Computers-Computer-Science',
    #     'extension': 'PDF',
    #     'size': ' 23.46 MB',
    #     'rating': '5.0/5.0',
    #     'download_url': 'https://x.x/dl/123'
    # }


if __name__ == '__main__':
    asyncio.run(main())
```  

### Enable logging  
Put anywhere in your code:  

```python
import logging

logging.getLogger("zlibrary").addHandler(logging.StreamHandler())
logging.getLogger("zlibrary").setLevel(logging.DEBUG)
```  

### Login
```python
lib = zlibrary.AsyncZlib()
await lib.login(email, password)

# next requests will use cookies gathered on login
await lib.init()
```  

### Search params
```python
await lib.search(q="Deleuze", from_year=1976, to_year=2005,
                 lang=["english", "russian"], extensions=["pdf", "epub"])

await lib.full_text_search(q="The circuits of surveillance cameras are themselves part of the decor of simulacra",
                           lang=["english"], extensions=["pdf"], phrase=True, exact=True)
```  

### Proxy support 
```python

# You can add multiple proxies in the chain:
# proxy_list=[
#    "http://login:password@addr:port",
#    "socks4://addr:port",
#    "socks5://addr:port"
# ]

lib = zlibrary.AsyncZlib(proxy_list=["socks5://127.0.0.1:9050"])

await lib.login(email, password)
await lib.init()

```

### Download history
```python
await lib.login(email, password)

# get a paginator of download history
dhistory = await lib.profile.download_history()
# get current page
first_page = dhistory.result
# get next page (if any; returns [] if empty)
await dhistory.next_page()
# go back
await dhistory.prev_page()
# fetch a book
book = await dhistory.result[0].fetch()
```  

### Booklists
```python
await lib.login(email, password)
# get booklists paginator
bpage = await lib.profile.search_public_booklists(q="philosophy", count=10, order=zlibrary.OrderOptions.POPULAR)

# get first 10 booklists
first_set = await bpage.next()
# get one booklist
booklist = first_set[0]
# get booklist data
booklist_data = await booklist.fetch()
# booklist_data = { 'name': 'VVV', url: 'YYY' }

# get first 10 books from the booklist
book_set = await booklist.next()
# fetch a book
book = await book_set[0].fetch()

# fetch personal booklists
bpage = await lib.profile.search_private_booklists(q="")
```  

### Set up a tor service
`sudo apt install tor obfs4proxy` or `sudo pacman -S tor obfs4proxy`  
`sudo systemctl enable --now tor`

If tor is blocked in your country, you also need to edit /etc/tor/torrc and set up bridges for it to work properly.

**HOW TO REQUEST BRIDGES**  
Using gmail, send an email to `bridges@torproject.org` with the following content: `get transport obfs4`  

Shortly after you should receive a reply with bridges.

Edit /etc/tor/torrc to enable and add your bridges:
```
UseBridges 1
ClientTransportPlugin obfs4 exec /usr/bin/obfs4proxy
<INSERT YOUR BRIDGES HERE>
```

Restart tor service:
`sudo systemctl restart tor`
