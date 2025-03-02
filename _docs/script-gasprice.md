---
panelgroup: Other Fun Panels
name: Gas Prices
title: Gas Prices Script
layout: default
description: Produces an image displaying the gas price for a region in the United States or Canada using CollectAPI data
imageurl: ../images/gasprice.png
---

# Gas Price

This script prepares an image displaying the gas price for a state or province in the
United States or Canada.  

![sample image of gas price](../images/gasprice.png)

## Script Location

The script is installed at
[~/nodeyez/scripts/gasprice.py](../scripts/gasprice.py).

## Dependencies

It depends on data being retrieved from [collectapi](./config-collectapi.md) via the
[~/nodeyez/scripts/daily-data-retrieval.py)(../scripts/daily-data-retrieval.py)
script.

## Configuration

To manage and configure this script, use the nodeyez-config tool

```sh
sudo nodeyez-config
```

To manually configure this script, edit the `~/nodeyez/config/gasprice.json` file

Fields are defined below

| field name | description |
| --- | --- |
| activeCountry | The preferred gas price data set to use. Default `USA`. Allowed values: `USA`, `CAN` |
| activeState | The preferred state or province to look up gas prices for. Default `California`. Allowed values: Any named state or province |
| backgroundColor | The background color of the image expressed as a hexadecimal color specifier. Default `#602060` |
| blockclockEnabled | Indicates whether results should be sent to a blockclock. Default `false` |
| blockclockAddress | The IP address of the blockclock on your network. Default `21.21.21.21` |
| blockclockPassword | The password for the blockclock on your network, leave blank for no password. Default is unset |
| gasTextColor | The color of the main label expressed as a hexadecimal color specifier. Default `#e69138` |
| height | The height, in pixels, to generate the image. Default `320` |
| interval | The amount of time, in seconds, the script should wait before data gathering and image creation again. Default `3600` |
| locationTextColor | The color of the location label expressed as a hexadecimal color specifier. Default `#f1c232` |
| priceTextColor | The color of the price label expressed as a hexadecimal color specifier. Default `#6aa84f` | 
| randomCountryEnabled | Indicates whether the country for gas price data should be chosen randomly. Default `true` |
| randomStateEnabled | Indicates whether the state or province for gas price data should be chosen randomly. Default `true` |
| width | The width, in pixels, to generate the image. Default `480` |

## Run Directly

Ensure the virtual environment is activated
```shell
source ~/.pyenv/nodeyez/bin/activate
```

Change to the scripts folder
```shell
cd ~/nodeyez/scripts
```

Run it
```shell
python gasprice.py
```

Press CTRL+C to stop the process

## Run at Startup

To enable the script to run at startup, as the privileged user run the following

```shell
sudo systemctl enable nodeyez-gasprice.service

sudo systemctl start nodeyez-gasprice.service
```

---

[Home](../) | 