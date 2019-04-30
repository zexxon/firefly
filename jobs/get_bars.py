__author__ = 'MattMaloney'

import requests
import datetime
import os
import csv
import time
import json
from requests.auth import HTTPBasicAuth

limit = 1000
pageStart = 0
ff_api_host = "192.168.1.150" #"10.8.0.1" #"192.168.1.150" #"10.8.0.1"
ff_api_port = "9999"

class Backtest:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


def get_formatted_date(epoch_time):
    timestamp = datetime.datetime.fromtimestamp(int(epoch_time))
    return str(timestamp.strftime("%y")), str(timestamp.strftime("%m")), str(timestamp.strftime("%d")), str(timestamp.strftime("%H")), str(timestamp.strftime("%M"))

def bar_request_json(root_name, contract, start_time, end_time, bar_size, downsample_check, ask_data):

    bar_request_payload = {
        root_name: {
            "StatusNotification": "",
            "ContractName": contract,
            "StartTime": start_time,
            "EndTime": end_time,
            "BarSize": bar_size,
            "DownSample" : downsample_check,
            "AskData": ask_data
        }
    }

    return bar_request_payload


def backtest_request_json(system_logic, contract, contract_name, start_time, end_time, trade_window, trade_delay,
                          trade_ttl, pip_size, bar_size, ask_data, range_start, range_bar_count, range_min_size,
                          range_max_size, signal_delay, signal_ttl, increase_range_min, increase_range_max,
                          increase_trade, increase_profit, increase_loss, entry_threshold, entry_target,
                          profit_target, loss_target, step_range_start, step_profit_target,step_loss_target,
                          step_increase_multiplier):
    # Serializes backtest parameters into JSON format for posting to backtester API
    # Need to add logic to validate inputs... this should be done at the API layer.

    backtest_request_payload = {
        "systemLogic": {
        "SystemLogic": system_logic,
        "ContractName": contract,
        "Name": contract_name,
        "StartTime": start_time,
        "EndTime": end_time,
        "TradeWindow": trade_window,
        "TradeDelay": trade_delay,
        "TradeTTL": trade_ttl,
        "PipSize": pip_size,
        "BarSize": bar_size,
        "AskData": False,
        "movingaverage": "0",
        "fibonacci": False,
        "rsi": False,
        "systemlogic": "",
        "getSystem": "",
        "runSystem": "",
        "saveBacktest": "",
        "saveSystem": "",
        "StatusNotification": "",
        "LogicParameters": {
            "Range Start": range_start,
            "Range Bar Count": range_bar_count,
            "Range Min Size": range_min_size,
            "Range Max Size": range_max_size,
            "Signal delay": signal_delay,
            "Signal entry TTL": signal_ttl,
            "Increase Range Min Size": increase_range_min,
            "Increase Range Max Size": increase_range_max,
            "Increase Trade Multiplier": increase_trade,
            "Increase Profit Target":  increase_profit,
            "Increase Loss Target": increase_loss,
            "Entry Market Threshold": entry_threshold,
            "Entry Target": entry_target,
            "Profit Target": profit_target,
            "Loss Target": loss_target
        },
        "StepMutations": {
            "Range Start": [
                step_range_start
            ],
            "Profit Target":
                step_profit_target
            ,
            "Loss Target": [
                step_loss_target
            ],
            "Increase Trade Multiplier": [
                step_increase_multiplier
            ]
        }
    }}
    print(json.dumps(backtest_request_payload))
    return backtest_request_payload


def add_bar_data(json_payload, uri, user, password):

    # response = requests.post('http://' + ff_api_host + ':' + ff_api_port + '/api/bar/add/', json=json_payload, auth=
    # (user, password), verify=False)
    response = requests.post('http://' + ff_api_host + ':' + ff_api_port + '/api' + uri, json=json_payload, verify=False)
    #parse_value((response.content.decode('ascii')))

    return response.content

def get_bar_data(json_payload, uri, user, password):

    # response = requests.post('http://' + ff_api_host + ':' + ff_api_port + '/api/bar/add/', json=json_payload, auth=
    # (user, password), verify=False)
    response = requests.post('http://' + ff_api_host + ':' + ff_api_port + '/api' + uri, json=json_payload, verify=False)
    #parse_value((response.content.decode('ascii')))

    return response.content


def run_backtest(json_payload, uri, user, password):

    # response = requests.post('http://' + ff_api_host + ':' + ff_api_port + '/api/bar/add/', json=json_payload, auth=
    # (user, password), verify=False)
    response = requests.post('http://' + ff_api_host + ':' + ff_api_port + '/api' + uri, json=json_payload, verify=False)
    parse_backtest_results((response.content.decode('ascii')))

    return response.content


def parse_backtest_results(input_string):
    input_string = json.loads(input_string)
    print("Entry Time, Exit Time, SystemID, SignalID, Max DD, Max P&L, Direction")
    for key in input_string:
        for value in key:
            #print(value['TradeDirection'])
            #print(value['MaxP&L '])
            #print(value['MaxDD'])
            #print(value['ID'])
            #print(value)
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(value["EntryTime"])/1000)) + ',' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(value["ExitTime"])/1000)) + ',' + str(value["TradeID"]) + ',' + str(value['ID']) + ',' + str(value['MaxDD']) + ',' + str(value['MaxP&L ']) +
                  ',' + str(value['TradeDirection']))
            #print(value['NetProfitLoss'])
        #value = input_string[key]
        #print(key)
    return key

# user, password = get_creds()
end_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%dT%H:%M')
# Get last 2 hours to avoid missing bars
time_delta = datetime.timedelta(minutes=120)
start_date = datetime.datetime.now() - time_delta
start_date = datetime.datetime.strftime(start_date, '%Y-%m-%dT%H:%M')


# Add 1 sec bar data
print("1 sec bar data pull. Date Range: " + str(start_date) + "->" + str(end_date))
add_bar_data(bar_request_json('Bar', 'GBPUSD.IB', str(start_date), str(end_date), '1', 'false', 'false'), '/bar/add/','','')

# Sleep 20 minutes between pulls. The correct way would be to validate the 1s bar data job is complete by enumerating last value updated in DB. 
print("Sleeping for 1 minute, before pulling minute bar data.")
time.sleep(60)

# Add 1 min bar data
print("1 minute bar data pull. Date Range: " + str(start_date) + "->" + str(end_date))
add_bar_data(bar_request_json('Bar', 'GBPUSD.IB', str(start_date), str(end_date), '60', '', 'false'), '/bar/add/','','')

# Sleep 1 minute after minute bar pull
print("Sleeping for 1 minute, before pulling hour bar data.")
time.sleep(60)

# Add 1 hour bar data
print("1 hour bar data pull. Date Range: " + str(start_date) + "->" + str(end_date))
add_bar_data(bar_request_json('Bar', 'GBPUSD.IB', str(start_date), str(end_date), '3600', 'false','false'), '/bar/add/','','')
# Add sleep buffer between next script call
time.sleep(60)
