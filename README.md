# README

## I was kind of dumb struck about the news of Book Depository (BD) closing April 26th, 2023.
## About half of my English-language collection was bought there and I think the appeal was, apart from the huge selection (which Amazon also has), the free international shipping. Yes, that's great in and of itself, but it also makes everything very simple - the price shown in the page is the price you pay and that's it.
## I'm a sobbing sentimentalist, so I knew I had to place one last order before the whole thing shut down. Given that it was purely symbolic (although it *was* on my wishlist, which means I'd eventually get around to buying it), I wanted to be the cheapest one available. There *is* an option to sort your wishlist by price in BD but I've given up on using it a long time ago, because, honestly? It doesn't work - *at all*.
## So, scraping away we go. My first thought was simply to list all prices and then pick the cheapest, but I've heard good things about Blackwell's - who also have free international shipping. So, I decided to scrape the price of the same books (id'ed by ISBN) on Blackwell's site. This way, I could make two orders and make a direct comparison between the two.

## So, here's how to use this:
1) Go to bookdepository.com, click on Wishlist and then "Download your wishlists". It will give you a neat table with all the books on all of your wishlists *and no way to export it to a convenient data format*. Sigh.
2) Select all and hit Ctrl-C (or right-click -> "Copy" or whatever you do to copy to clipboard). Open Excel and paste. **IMPORTANT - Make sure the ISBN column is not in scientific notation! Change column format to Number (0 decimal places) if needed**
3) Save in the same folder as the script. Name it wishlist and choose Comma Separated Values (*.csv)
4) Run the script. You need to have Requests, BeautifulSoup, Numpy and Pandas installed.

## The recommendations will be the cheapest books both on Book Depository and Blackwell's **unless there's a cheaper version available on the other store** (or the other store is out of stock).

## Thank you for reading.
## João.