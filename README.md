## InstaRaider

This function contains code that is originally Copyright (c) {{{2014}}} {{{Amir Kurtovic}}}

This code is a modified version of: https://github.com/akurtovic/InstaRaider

the original code is not working well with new instagram website design
Original modification was made on 03/06/2015

## Disclaimer
This code is posted for informational purposes only. Use of Instagram is governed by the company's Terms of Use (http://instagram.com/legal/terms/). Any user content posted to Instagram is governed by the Privacy Policy (http://instagram.com/legal/privacy/). If you feel this code fails to obey the company's terms & policy or any law, contact me at gaochi0500@gmail.com

If you find any bug in running the code, free feel to contact me at gaochi0500@gmail.com. I will make effect to fix it, but I cannot guarantee the fix in time. It is possible the code won't work any more if changes occur to the instagram website design.

## Code Purpose

A Python script that uses Selenium WebDriver to automatically download photos for any Instagram user.
InstaRaider can download all photos for any public Instagram profile without relying on API calls or user authentication. As long as the user's profile is public, InstaRaider will be able to download a specified number of photos.

## Installation

The code runs in Python. It requires Selenium WebDriver and BeautifulSoup modules

## Usage
```python
python instaRaider.py -u USER [-c COUNT]
```

To download all photos of user 'XYZ'
```python
python instaRaider.py -u XYZ
```

To download the most recent 20 photos of user 'XYZ'
```python
python instaRaider.py -u XYZ -c 20
```


## License

Copyright (c) 2015 Chi Gao with portions Copyright (c) {{{2014}}} {{{Amir Kurtovic}}}. See the LICENSE file for license rights and limitations (MIT).


