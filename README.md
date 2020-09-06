# FineCookingArchivePythonClient
An alternative, Python-based client for the now defunct 1994-2015 Fine Cooking Archive

## How to get and run
1. Run the following from Terminal

   ```
   xcode-select --install
   ```

1. Get python3

   [Install version 3.x here](https://www.python.org/downloads/mac-osx/), [or follow this alternative guide](https://docs.python-guide.org/starting/install3/osx/)

1. Get the script

   ```
   git clone https://github.com/jray272/FineCookingArchivePythonClient.git
   ```

1. Run, learn how to use, and enjoy

   ```
   cd FineCookingArchivePythonClient/
   python3 fine_cooking_archive_client.py --help
   python3 fine_cooking_archive_client.py search text <search term here>
   ```


## Background
Fine Cooking used to sell a really nice product that was an archive of all of their issues from 1994-2015. Essentially, all of their issues from that period were sold in PDF form on a flash drive or DVD. Since the PDFs were full pictures without any embedded text, the product also contained a database and a client that would allow you to search through the issues for any term that you wanted to find. The client would then point you to a particular issue and page number so that you could read the full text yourself.

Unfortunately, the Mac OS X version of the client was built as a 32-bit Application and thus no longer runs on Catalina (10.15) since 32-bit app support was dropped in this version. As such, the archive is far less useful because it is no longer searchable.

Fortunately, the database used to serve the client is just a sqlite database with a fairly simple schema. Because of this, making an alternative client isn't hard to do (albeit with a command line interface).

The archive is tough to find these days, but may be able to be purchased [here](https://www.amazon.com/Fine-Cooking-2015-Magazine-Archive/dp/1631865978/). The name on the box is *Fine Cooking Magazine Archive 1994 to 2015*.

Created with love for my mom but also as a fun little side project for me.
