''' Train tickets query via CLI
Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 上海 2016-10-10
    tickets -dg 成都 南京 2016-10-10
'''
from docopt import docopt
from stations import stations
import requests
from prettytable import PrettyTable
import urllib3
import copy
from colorama import init, Fore
init()


     
     
def _get_keys(station_eg):
    for key in stations:
        if stations[key] == station_eg:
           return key

class TrainsCollection:
      
        header = '车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split()
        def __init__(self, available_trains, options):    
           self.available_trains = available_trains
           self.options = options
          
        
 
        
        def _cut_train(self):
              saperated_info = []
              print(len(self.available_trains))
              for i in range(len(self.available_trains)):
                  saperated_info.append((self.available_trains[i].split('|')))
              
              print(saperated_info)
              dict_header = ['train_number','from_station','to_station','from_time','to_time','spend_time',
                             'first_class','second_class','soft_sleeper','hard_sleeper','hard_seat','without_seat']
              refer_to_num = [3,4,5,8,9,10,31,30,23,28,29,26]
              train_list = []
              train_dict = {}
              for times in range(len(saperated_info)):
                  for key in range(len(dict_header)):
                    if saperated_info[times][refer_to_num[key]]:
                      train_dict[dict_header[key]] = saperated_info[times][refer_to_num[key]]
                    else:
                      train_dict[dict_header[key]] = '--'
                  train_list.append(copy.deepcopy(train_dict))
              return train_list
              
        @property
        def trains(self):
          for raw_train in self._cut_train():
            train_no = raw_train['train_number']
            initial = train_no[0].lower()
            if not self.options or initial in self.options:
                train = [
                    train_no,
                    '\n'.join([Fore.GREEN + _get_keys(raw_train['from_station']) + Fore.RESET,
                    Fore.RED + _get_keys(raw_train['to_station']) + Fore.RESET]),
                    '\n'.join([Fore.GREEN + raw_train['from_time'] + Fore.RESET,
                    Fore.RED + raw_train['to_time'] + Fore.RESET]),
                    raw_train['spend_time'],
                    raw_train['first_class'],
                    raw_train['second_class'],
                    raw_train['soft_sleeper'],
                    raw_train['hard_sleeper'],
                    raw_train['hard_seat'],
                    raw_train['without_seat'],
                ]
                yield train
                
        def pretty_print(self):
           pt = PrettyTable()
           pt._set_field_names(self.header)
           for train in self.trains:
              pt.add_row(train)
           print(pt)
  
def cli():
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
     date, from_station, to_station)
    options = ''.join([
        key for key, value in arguments.items() if value is True])
    urllib3.disable_warnings()
    print(arguments.items())
    r = requests.get(url, verify = False)

    available_trains = r.json()['data']['result']
    
    TrainsCollection(available_trains, options).pretty_print()
    
if __name__ == '__main__':
     cli()              
              
             
        
        
       
