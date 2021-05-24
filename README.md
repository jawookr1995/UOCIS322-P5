# UOCIS322 - Project 5 #
Brevet time calculator with AJAX and MongoDB!

## Overview

Store control times from Project 4 in a MongoDB database. When we click on "submit" button, control times from project 4 are stored and "disply" button will display the latest stored value.

## User guide for application

a. Go to designated port that is on docker-compose.yml and get in ACP brevet calculator page.

b. Type the value in miles or km and you will get see open time and close time for those values.

c. if you click on "submit" button the value that you wrote on chart would be store in database. (You can write upto 20 values, but you should include at least one value)

d. and then when you click on "display" button, you will see the the entry list that is listed in new page.

## ACP controle time
That's "controle" with an e, because it's French, although "control" is also accepted. Controls are points where a rider must obtain proof of passage, and control[e] times are the minimum and maximum times by which the rider must arrive at the location

## Calculations

### Open Time
a. Make sure the open time is positive and control distance should not be over 20% longer than brevet distance
b. The calculation is based on maximum speed. See https://rusa.org/pages/acp-brevet-control-times-calculator.
c. Since Maximum speed is based on the range of control location, dictionary max_speed would store keys and speeds that are assoicated with those keys. 

### Close Time
a. Similar to Open time,
b. The calculation is based on minimum speed. See https://rusa.org/pages/acp-brevet-control-times-calculator.
c. Since Minimum speed is based on the range of control location, dictionary min_speed would store keys and speeds that are assoicated with those keys. 
d. If control distacne is greater than or equal to brevet distacne but not exceed 20% longer limit, then time set final_close for setting time limit.
d. when control distacne is less than or 60km, then maximum time limit for control distance for first 60 km would be calculated on 20km /h and add 1 hour to it.

## Testing (Nose test)

Automated test for testing, one for time calculator logic and once for DB insertion and retrival