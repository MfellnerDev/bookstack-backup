# BookStack Backup - Backup all your BookStack books

### Supported Operating Systems:

  - Windows
  - Linux (not tested yet)

### 1. Why?
This is a script that I wrote because I was just feeling unwell with all of my important notes being on exactly one server and managed by one application.

The notes I take are crucial for school, work, and other things, so it would be a horror to lose them somehow.

And because of that, I decided to make use of the BookStack API and just backup all my pages and books myself.

**My opinion:** BookStack is such a great application, and their API documentation is wonderful!

### 2. What do I need?

If you want to back up your BookStackbookss, you'll need the following things:

  1. A running BookStack application (of course).
  2. A BookStack Token ID and Token Secret for your Account -> [Bookstack public API docs](https://demo.bookstackapp.com/api/docs)
  3. Python 3.9 installed (it was developed & tested with only Python 3.9)
  4. Of course, you also need to download all used libs.
  5. Enough space :)
 
That's it!

### 3. How to setup

It is not much, but you have to do some small steps to prepare the script:

  1. Rename the `.env.example` file to `.env`
  2. Fill out the `.env` file with **your** data


### 4. Execute the script

For executing the script, you'll just need to start the `export_pages.py` file:

```shell
$ python3 export_pages.py
```

### 5. Result

The script will save your pages in the following format: 

`absolute-path/exports/[file-type]/[book-name]/[page-name].extension` 

- `filetype-file-type`: EXPORT_TYPE-Variable; it sets the file type for your 
exports. Possible options are markdown, pdf, and plaintext. 

- `book-name`: The name of your created books (e.g., "cooking recipes"))

- `page-name`: The name (headline) that you gave your page (e.g., "how to cook lasgana", etc.)

Now, if you follow the output of the script, you should receive messages with a structure like the following:

`Successfully exported & stored file "[FULL_PATH]\exports\[FILETYPE]\[BOOK_NAME]\[PAGE_NAME].[FILE_EXTENSION".`

For example:

`Successfully exported & stored file "C:\Users\User\Coding\PyCharm\BookStack\Backup\exports\markdown\hetzner-dedi-documentation-services\mastodon-social-networking-alternative.md".`

If you get error messages, check the `.env` file. If that doesn't help, feel free to open an issue.

### 6. What's next?

This script was just written for personal use, but I could imagine myself implementing the following extras in the future:
  
  - Possibility to back up the "complete" structure: shelves, books, chapters, and pages

   
  - Backup of attachments, images, etc.
   
   
  - Backup of BookStack configuration
   
  
  - Maybe a more beautiful wrapper for the script? Idk, maybe an GUI?
   
  - Who knows...
