Title:  Slip Report
Author: Mark Nemec
Date:   Janurary 15, 2015

# Introduction

The goal of our project was to take measurements of solar intensity and wind speed in possibly remote locations and upload them to a server so they could be later analysed by the user.

To achieve this we needed to build a service that would be able to store the measurements and retrieve them when the user wanted to analyse them. We built this service using a Javascript web framework Node.js[^nodejs] and a NoSQL database MongoDB[^mongodb] on top of a cloud application platform called Heroku[^heroku].

Moreover, we needed to build a user-facing application that took the raw measurements stored in a database and turned them into information understandable to the user. We thus built a single-page application using Backbone.js[^backbonejs].

In this report I will discuss how we arrived at these solutions, what motivated them, and how they satisfied the requirements. <!-- TODO: change requirements to something else -->

# Table of Contents

<!--TOC-->

# Requirements

The following were the most important requirements we considered when choosing a server solution:
 
 - cost: we wanted our server to be free
 - hosted in a cloud platform: did not want to host our machine ourselves
 - speed and ease of development
 - learning value?: worked with Python before, wanted to learn something else

In the end we decided to use the Node.js platform [^nodejs] hosted on a cloud provider Heroku [^heroku].

# Architecture

# Implementation Details

The implementation could be split into two main categories: Back-end and Front-end. Back-end concerns the API used to communicate with the Android device and the web browser and the front-end displays useful information about measurements.

## Back-end

### Authentication & Authorization

### Logging

## Front-end

The front-end is a single-page application that allows the user to ...

# Testing

# Evaluation

# Future work

If given more time there are certain things we would have liked to implement:

 - **Improve measurement analysis**
    Currently our system displays only basic information about measurements. It reports wind speed in meters per second and solar intensity in W/m^2. Ideally, we would have been able to display cost estimates along with this data but that would require an analysis of solar panel/wind turbine installation costs in a given area.

 - **Live streaming of measurements**
    This would work in conjunction with the Android app. The app would get data from WindSol and pass it along to the web server which would again pass it along to the web client using socket.io WebSockets, [3] all in real-time. This would allow improved demonstration and testing as the user could see the measurement charts rendered in real-time without having to upload only a "chunk" of data and refreshing his browser.

# References

[^heroku]: Heroku, [http://heroku.com](http://heroku.com)
[^nodejs]: Node.js, [http://nodejs.org](http://nodejs.org)
[^backbonejs]: Backbone.js, [http://backbonejs.org](http://backbonejs.org)
[^mongodb]: MongoDB, [http://mongodb.org](http://mongodb.org)
