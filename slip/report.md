Title:  Slip Report
Author: Mark Nemec
Date:   Janurary 15, 2015

# Introduction

The goal of our project was to take measurements of solar intensity and wind speed in possibly remote locations and upload them to a server so they could be later analysed by the user.

To achieve this we needed to build a back-end web service that would be able to store the measurements in persistent storage and retrieve them when the user wanted to analyse them. We built this service using a Javascript web framework Node.js[^nodejs] and a NoSQL database MongoDB[^mongodb] on top of a cloud application platform called Heroku[^heroku]. <!-- Maybe move this segment into requirements? -->

Moreover, we needed to build a front-end application that took the raw measurements stored in a database and turned them into useful information understandable to the user. We thus built a single-page application using Backbone.js[^backbonejs].

In this report I will discuss how we arrived at these solutions, what motivated them, and how they satisfied the requirements. <!-- TODO: change requirements to something else -->

# Table of Contents

<!--TOC-->

# Requirements analysis

To make sure our completed web stack <!-- is stack the correct word? --> performed what it was supposed to <!-- reword this --> we performed a requirement analysis where we enumerated functional and non-functional requirements that we could verify our final system against.

## Back-end

### Functional requirements

These are the functional requirements we considered while developing our server solution:

 - Provide an endpoint to which the Android app can upload measurements safely.
 - Create a login system so that only authorised users can log in to the web client and upload measurements.
 - Store the measurements in persistent storage so they can be retrieved.
 - Provide an interface which the web client can use to request measurements and other information.

### Non-functional requirements

The following were the most important non-functional requirements we considered when developing our server solution:
 
 - We wanted our server to be free.
 - Available on the whole of Internet, not just on LAN where the installation is.
 - Preference for speed and ease of development rather than safety and server performance.
 - I have worked with Python before and wanted to learn more about Javascript web frameworks.

## Front-end

### Functional requirements

These were the functional requirements we considered while developing our front-end application:

 - Display information about measurements in an understandable way.
 - Allow users to filter information by specifying a date range.
 - Allow addition and deletion of users so that new users can upload data.
 - Provide log in and log out actions so that users can authenticate.

### Non-functional requirements

The following were the most important non-functional requirements we considered when developing our front-end application:

 - Make the design responsive so that it works on mobile as well as desktop clients.

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
