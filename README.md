# Weight Watchers Service for Home Assistant

[![Stargazers repo roster for @jdeath/weightwatchers_service](https://git-lister.onrender.com/api/stars/jdeath/weightwatchers_service?limit=30)](https://github.com/jdeath/weightwatchers_service/stargazers)

## Installation

1. Add this repository to HACS as an integration: https://github.com/jdeath/weightwatchers_service
1. Install the integration
1. In `custom_components\weightwatchers_service\__init__.py`, edit your Weight Watchers username and password. 
1. Restart your instance

The service also assumes you use LBS. Feel free to change code if you use Kg. Could also modify to send username/password as a service data, but I was lazy.

To send your weight manually with a service (200 lbs in example):

```
service: weightwatchers_service.set_weight
data:
  weight: 200
```

To send your weight automatically when your scale updates, see below. This automation only sends if weight is between 195 and 210 as an error check in case a child steps on scale. This also only updates when scale goes from unavailable->to a weight. That is how my scale entity works, but you can easily change that in the automation.
```
alias: Update Weight
description: ""
trigger:
  - platform: state
    entity_id:
      - sensor.scale_entity
    from: unavailable
condition:
  - condition: numeric_state
    entity_id: sensor.scale_entity
    above: 195
    below: 210
action:
  - service: weightwatchers_service.set_weight
    data:
      weight: "{{ states('sensor.scale_entity') }}"
mode: single
```
