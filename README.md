         _____                            ______       _   
        /  __ \                           | ___ \     | |  
        | /  \/ ___  _   _ _ __ ___  ___  | |_/ / ___ | |_ 
        | |    / _ \| | | | '__/ __|/ _ \ | ___ \/ _ \| __|
        | \__/\ (_) | |_| | |  \__ \  __/ | |_/ / (_) | |_ 
         \____/\___/ \__,_|_|  |___/\___| \____/ \___/ \__|
                                                           
                                                               
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
3. Copy config.example.json as config.json
```bash
cp config.example.json config.json
```
4. Modify the content to anything what you need.

## Config
|   Key   |  Type  |   Description   |
|:-------:|:------:|:---------------:|
| account | string | username (NID)  |
| passwd  | string | password        |
| firstchoose | list | course code list |
| autodrop | list | Not used |
