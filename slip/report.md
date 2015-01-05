

# Introduction

The goal of our project was to take solar and wind-speed measurements in possibly remote locations, upload them to a server via an Android app, and perform further analysis on the measurements through web interface.

We came up with a solution that solves two problems:

 - Provides a secure interface for the Android app to communicate with.
 - Displays information about measurements in a human-understandable way.

# Requirements

The following were the most important requirements we considered when choosing a server solution:
 
 - cost: we wanted our server to be free
 - hosted in a cloud platform: did not want to host our machine ourselves
 - speed and ease of development
 - learning value?: worked with Python before, wanted to learn something else

In the end we decided to use the Node.js platform [1] hosted on a cloud provider Heroku [2].

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

[1]: http://nodejs.org
[2]: https://www.heroku.com
[3]: http://socket.io
