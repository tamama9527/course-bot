# Course-bot
神奇的搶課小工具

## Requirement
- Python2
- Some python package
    - pytz
    - BeautifulSoup
    - requests

## Install
1. Install Python2 (maybe apt-get?)
2. Install python package using pip
```bash
pip install -r requirements.txt
```
3. Copy config.json.example as config.json
```bash
cp config.json.example config.json
```
4. Modify the content to anything what you need.

## Config
|   Key   |  Type  |   Description   |
|:-------:|:------:|:---------------:|
| account | string | username (NID)  |
| passwd  | string | password        |
| firstchoose | list | course code list |
| autodrop | list | Not used |