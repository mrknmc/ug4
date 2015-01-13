Title:  Slip Report
Author: Mark Nemec
Date:   January 15, 2015
Todo:   240 is the max W/m^2

# Table of Contents

<!--TOC-->

# Introduction

The goal of our project was to take measurements of solar intensity and wind speed in possibly remote locations and upload them to a server via a mobile application so they could be later analysed by the user with a web browser. <!-- with a web browser sounds weird -->

<!-- add more stuff here -->

# Requirements Analysis

To make sure our final solution performed as it was supposed to we first performed requirement analysis where we enumerated functional and non-functional requirements that we could verify against our final system.

## Back-end

To achieve our goal we needed to build a back-end web service that would be able to store the measurements sent from the app in persistent storage and retrieve them when the user wanted to analyse them. We built this service using a Javascript web framework Express.js [^expressjs] running on the Node.js[^nodejs] platform and a NoSQL database MongoDB[^mongodb] on top of a cloud application platform called Heroku[^heroku]. <!-- Maybe move this segment into requirements? -->

### Functional Requirements

These are the functional requirements we considered while developing our server solution:

 - Provide an endpoint to which the Android app can upload measurements.
 - Create an authorisation system so that only authorised users can upload measurements.
 - Store the measurements in persistent storage so they can be retrieved.
 - Provide an interface which the web client can use to request information about the measurements.

### Non-functional Requirements

The following were the most important non-functional requirements we considered when developing our server solution:
 
 - We wanted our server to be free.
 - Available on the whole of Internet, not just on LAN where the installation is.
 - Preference for speed and ease of development rather server performance.
 - I have worked with Python before and wanted to learn more about Javascript web frameworks.

## Front-end

Moreover, we needed to build a front-end application that took the raw measurements stored in a database and turned them into useful information understandable to the user. We thus built a single-page application using Backbone.js[^backbonejs].

### Functional Requirements

These were the functional requirements we considered while developing our front-end application:

 - Display information about measurements in an understandable way.
 - Allow users to filter information by specifying a date range.
 - Allow addition and deletion of users so that new users can upload data.
 - Provide log in and log out actions so that users can authenticate.

### Non-functional Requirements

The following were the most important non-functional requirements we considered when developing our front-end application:

 - Make the design responsive so that it works on mobile as well as desktop clients.

<!-- add more stuff here -->

# Design & Architecture

## Back-end

Initially, we wanted to use the Dropbox Datastore API [^dropbox] as a backend which would greatly simplify most of the work. The users would be able to authenticate using Dropbox's implementation of the OAuth 2.0 protocol and measurements would have been stored in their Dropbox storage. Dropbox users get 2GB of space for free which would have been enough for our needs. However, we soon hit a roadblock when we found that an individual datastore can be at most 10 MB. <!-- link to docs here --> Querying over multiple datastores would be a hacky solution. <!-- rephrase hacky -->

We researched other products as well <!-- links here? --> but in the end none of them provided all the features that what we needed. We thus decided to develop our own back-end solution:

![Back-end Architecture](img/arch.png "Back-end Architecture")

### Web Server

The server code was developed in a Javascript web framework called Express.js [^expressjs] built on top of the Node.js [^nodejs] platform. We considered other options but this combination provided us with certain advantages.

#### Something about event-driven stuff

Blah blah.

#### Sharing Code

Since the server and the client are both written in Javascript, there is a possibility of sharing code, i.e. both front-end and back-end can use same functions. This is one of the chief arguments for Node.js because it allows you to update front-end and back-end code in one place in one language.

#### Ease and Speed of Development

Even though mature web frameworks for Java and other statically typed languages exist, we dismissed them as we preferred the ease of development of dynamically typed languages such as Python, Ruby and Javascript. <!-- maybe some reference here -->

#### Learning Value <!-- possibly incorrect words -->

I have worked with Python frameworks such as Django and Flask before and wanted to learn something new. The event driven asynchronous model of Node.js seemed to be a good fit for our project.

Getting Express.js to render a view called `model` when a user hits the url `<host>/model` is as easy as:

```
app.get('/model', function(req, res) {
  res.render('model');
});
```

Alongside with Express.js we used a lot of third party libraries: 

 - `express-session`
 - `passport.js`
 - `connect-redis`
 - `logfmt`
 - `mongoose`
 - `googleapis`
 - `body-parser`
 - `jade`
 - `lodash`
 - `passport`
 - `passport-google-oauth`
 - `request`

### Persistent Storage

To store measurements into persistent storage we decided to use a NoSQL database called MongoDB [^mongodb]. The free tier MongoDB add-on provided by Compose [^compose] comes with 1 GB of storage. There were several reasons we chose MongoDB over other solutions.

#### Dynamic Schemas

MongoDB is a NoSQL database with dynamic schemas. This means that documents stored in one collection do not have to comply to a schema. This allows for rapid development and proved to be suitable for our project as the schema of data sent from the mobile application changed frequently during development.

#### Geospatial Indexing

MongoDB comes with support for geospatial indexing and querying. This means that we could execute database queries on location information allowing us to for example find all historical measurements near user's area. We did not end up implementing this feature but it was something we thought would be interesting. <!-- maybe not interesting but something else? -->

#### Learning value

As with the web server I thought this was an ideal chance to learn something new. I have worked with SQL databases such as PostgreSQL and MySQL before but have not had a chance to try out a NoSQL database such as MongoDB.

### Temporal Storage

While developing our back-end we realised the need for temporal fast-access storage. This is where we decided to use Redis [^redis]. Redis serves as a key-value cache that is stored fully in main memory. Access to data is then limited by network speed between the web server and the Redis server rather than by disk I/O.

There is a free tier Redis add-on for Heroku provided by Redis Cloud [^rediscloud] that provided us with 25MB which turned out to be more than enough for our purposes.

## Front-end

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

## Back-end

### Live streaming of measurements

This would work in conjunction with the Android app. The app would get data from WindSol and pass it along to the web server which would again pass it along to the web client using socket.io WebSockets, [3] all in real-time. This would allow improved demonstration and testing as the user could see the measurement charts rendered in real-time without having to upload only a "chunk" of data and refreshing his browser.

### geolocation stuff I mentioned in design

Bla blah blah.

## Front-end

### Improve measurement analysis

Currently our system displays only basic information about measurements. It reports wind speed in meters per second and solar intensity in W/m^2. Ideally, we would have been able to display cost estimates along with this data but that would require an analysis of solar panel/wind turbine installation costs in a given area.

# References

[^expressjs]: Express.js, [http://expressjs.com](http://expressjs.com)
[^heroku]: Heroku, [http://heroku.com](http://heroku.com)
[^nodejs]: Node.js, [http://nodejs.org](http://nodejs.org)
[^backbonejs]: Backbone.js, [http://backbonejs.org](http://backbonejs.org)
[^mongodb]: MongoDB, [http://mongodb.org](http://mongodb.org)
[^dropbox]: Dropbox Datastore API, [https://www.dropbox.com/developers/datastore](https://www.dropbox.com/developers/datastore)
[^mongoose]: Mongoose, [http://mongoosejs.com](http://mongoosejs.com)
[^redis]: Redis, [http://redis.io](http://redis.io)
[^compose]: Compose, [http://compose.io](http://compose.io)
