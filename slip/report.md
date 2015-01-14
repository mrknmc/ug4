Title:  Slip Report
Author: Mark Nemec
Date:   January 15, 2015

# Table of Contents

<!--TOC-->

# Introduction

The goal of the WindSol project was to take measurements of solar intensity and wind speed in possibly remote locations and upload them to a server via a mobile application so they could be later analysed by the user with a web browser. <!-- with a web browser sounds weird -->

To achieve our goal we needed to build a back-end web service that would be able to store the measurements sent from the app in persistent storage and serve them to a web client so they can be further analysed.

We also needed to build a front-end application that would retrieve the measurements from the service and turn them into information useful to the user.

# Requirements

To make sure our final solution performed as it was supposed to we first performed requirement analysis where we enumerated functional and non-functional requirements that we could verify against our final system.

## Back-end Service

### Functional Requirements

 - Provide an endpoint to which the Android application can upload measurements.
 - Create an authorisation system so that only authorised users can upload measurements.
 - Store the measurements in persistent storage so they can be retrieved.
 - Provide an interface which the web client can use to request information about the measurements.

### Non-functional Requirements
 
 - We wanted our server to be free.
 - Available on the whole of Internet, not just on LAN where the WindSol installation is located.
 - Preference for speed and ease of development rather server performance.
 <!-- - I have worked with Python before and wanted to learn more about Javascript web frameworks. -->

## Front-end Application

### Functional Requirements

 - Display information about measurements in a way useful for the user.
 - Allow users to filter information by specifying a date range.
 - Allow deletion of uploads in case they were malformed.
 - Display where the measurements were taken on a map.
 - Allow addition and deletion of users so that new users can be authorised to upload data.
 - Provide log in and log out actions so that users can authenticate.

### Non-functional Requirements

 - Make the design responsive so that it works on mobile as well as desktop clients.

<!-- TODO: add more stuff here -->

# Design & Architecture

## Back-end Service

Initially, we wanted to use the Dropbox Datastore API [^dropbox] for back-end which would greatly simplify most of the work. The users would be able to authenticate using Dropbox's implementation of the OAuth 2.0 protocol and measurements would have been stored in their Dropbox storage. Dropbox users get 2GB of space for free which would have been enough for our needs. However, we soon hit a roadblock when we found that an individual datastore can be at most 10 MB. <!-- link to docs here --> Querying over multiple datastores would be a hacky solution. <!-- rephrase hacky -->

<!-- TODO: maybe remove the above completely -->

We researched other services as well <!-- links here? --> but in the end none of them provided all the features that what we needed. We thus decided to build our own back-end service using a Javascript web framework Express.js [^expressjs] running on the Node.js [^nodejs] platform and a NoSQL database MongoDB[^mongodb]. Additionally, we used a key-value cache called Redis [^redis] to store temporal data. We hosted these services on top of a cloud application platform called Heroku [^heroku]. Heroku normally costs money but they have a free option which provided us with 512MB of RAM and one dyno (lightweight container specific to Heroku). This proved to be performant enough for our prototype.

![Back-end Architecture](img/arch.png "Back-end Architecture")

### Web Server

The server code was developed in a Javascript web framework called Express.js which runs on the Node.js platform. We considered other options but this combination provided us with certain advantages.

#### Sharing Code

Since the server and the client are both written in Javascript, there is a possibility of sharing code so that both front-end and back-end can use the same source code. This is one of the chief arguments for Node.js because it allows you to update front-end and back-end code in one place in one language.

#### Event-driven non-blocking model

Node.js is said to be "perfect for data-intensive real-time applications" [^nodejs]. We thought this was ideal for our purposes as we planned to upload measurements at a high rate.

#### Ease and Speed of Development

Even though mature web frameworks exist for Java and other statically typed languages, we dismissed them as we preferred the ease of development of web frameworks written in dynamically typed languages such as Python, Ruby and Javascript. This allowed for rapid progress.

#### Learning Values

Having worked with Python frameworks such as Django and Flask before, we wanted to learn something new and see how it compares to the frameworks we know.

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

To store measurements into persistent storage we decided to use a NoSQL database called MongoDB. The free tier MongoDB add-on for Heroku provided by Compose [^compose] comes with 1 GB of storage. There were several reasons we chose MongoDB over other solutions.

#### Dynamic Schemas

MongoDB is a NoSQL database with dynamic schemas. This means that documents stored in one collection do not have to comply to a schema. This allows for rapid development and proved to be suitable for our project as the schema of data sent from the mobile application changed frequently during development.

#### Geospatial Indexing

MongoDB comes with support for geospatial indexing and querying. This means that we could execute database queries on location information allowing us to for example find all historical measurements near user's area.

#### Learning value

As with the web server we thought this was an ideal chance to learn something new. Having worked with SQL databases such as PostgreSQL and MySQL before we wondered how a NoSQL database such as MongoDB compares to them.

### Temporal Storage

While developing our back-end we realised the need for fast-access temporal storage. This is where we decided to use Redis. Redis serves as a key-value cache that is stored fully in main memory. Access to data is then limited by network speed between the web server and the Redis server rather than by disk I/O.

There is a free tier Redis add-on for Heroku provided by Redis Cloud [^rediscloud] that provided us with 25MB of storage (in main memory) which turned out to be more than enough for our purposes.

## Front-end Application

We developed a single-page front-end application using Backbone.js [^backbonejs] and several other libraries that made things much easier for us.

### Data Bindings

We used Backbone.js to communicate with the back-end API. JSON data returned by the API was wrapped in Backbone collections and models. This allowed easy modification on client side which automatically fired off requests to the back-end.

### UI Framework

None of the members of our team had much experience with web design. This is why we decided to use Bootstrap [^bootstrap] to style our application with CSS. It is very easy to get started with Bootstrap and its basic components got us quite far so that the amount of web design we had to do ourselves was minimal.

### Build System

The modules for the front-end were developed based on the CommonJS [^commonjs] module specification. This means that each module was defined in its own file and was imported by other modules as needed. This allowed us to develop each component of the front-end application separately and reduced coupling.

However, instead of deploying all the modules to the web server in separate files which would mean that the web client would have to make a separate request to download each file they were bundled into one file by Browserify [^browserify]. They were then furthermore minimised using UglifyJS [^uglifyjs]. This not only reduced the strain on the web server but improved the experience for users.

The whole build process was automatic and we could build the whole bundled minimised application with just one command thanks to a build system called Gulp [^gulp].

Moreover, during development we made use of a plugin called Livereload [^livereload]. Livereload allows you to see changes in source code rendered in browser in real-time. It does this by rebuilding the application whenever it records a changes in source code. This greatly simplified our work-flow and minimised feature-testing time.

# Implementation Details

## Back-end Service

### API

We built an application program interface (API) that the Android application as well as the web client use to create, update or delete objects in the database. For example, these are the API endpoints for actions concerning users:

`POST <host>/api/user`

:   Creates a new user.

`GET <host>/api/user`

:   Retrieves all users.

`GET <host>/api/user/:id`

:   Retrieves user with a specific id.

`DELETE <host>/user/:id`

:   Deletes user with a specific id.

To perform the actions that correspond to different requests the user needs to be authorised.

### Authorisation

To ensure that only authorised users used the API we made use of the Google OAuth 2.0 protocol. In our prototype we assumed that once a user is authenticated she is also authorised to perform all the actions available from the API. There are two ways we use this protocol:

1. The user signs in through the web application.

:   Assuming she is an authorized user (her email is already in the database) a session id is created and temporarily stored in the Redis cache and in the cookies of her browser. This cookie is then attached to all the requests of the user. Most of the hard work is handled by a library called Passport.js [^passportjs] as we know that writing security software is hard. The flow can be seen in the image below (steps after "Authorization code" can be ignored):

![Web Server Authentication with Google OAuth 2.0](img/google_auth.png "Web Server Authentication with Google OAuth 2.0")

2. The user signs in through the Android application.

:   The user then receives a JWT token which she sends along with her requests. When the server receives the token it verifies that it was signed by Google's private key. To do this the server requires Google's public key which it periodically retrieves using the OAuth library in Google's googleapis [^googleapis] package in npm. After the server verifies the token was signed by Google it can extract user information such as email from the token. The server then confirms that the request was sent by an authorised user by checking the database of users. The flow can be seen in the image below:

![Cross-client Identity Authentication with Google OAuth 2.0](img/auth.png "Cross-client Identity Authentication with Google OAuth 2.0")

### Logging

## Front-end Application

The front-end is a single-page application that allows the user to ...

# Testing

# Evaluation

# Future work

If given more time there are certain things we would have liked to implement:

## Back-end Service

### Live streaming of measurements

This would work in conjunction with the Android app. The app would get data from WindSol and pass it along to the web server which would again pass it along to the web client using socket.io WebSockets, [3] all in real-time. This would allow improved demonstration and testing as the user could see the measurement charts rendered in real-time without having to upload only a "chunk" of data and refreshing his browser.

### geolocation stuff I mentioned in design

Bla blah blah.

## Front-end Application

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
[^rediscloud]: Redis Cloud, [https://redislabs.com](https://redislabs.com)
[^compose]: Compose, [http://compose.io](http://compose.io)
[^bootstrap]: Bootstrap, [http://getbootstrap.com](http://getbootstrap.com)
[^commonjs]: CommonJS: [http://wiki.commonjs.org/wiki/CommonJS](http://wiki.commonjs.org/wiki/CommonJS)
[^browserify]: Browserify, [http://browserify.org](http://browserify.org)
[^uglifyjs]: UglifyJS, [https://github.com/mishoo/UglifyJS](https://github.com/mishoo/UglifyJS)
[^gulp]: Gulp, [http://gulpjs.com](http://gulpjs.com)
[^googleapis]: googleapis, [https://www.npmjs.com/package/googleapis](https://www.npmjs.com/package/googleapis)
