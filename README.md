#Inspiration
We want to make the job of keeping our world clean a collaborative effort. Giving the power to the people instead of the government

#What it does
The basic idea is to detect trash in images. There are so many live streams and media sources today from street light traffic cams to people's cellphones. We wanted to create a network where people could post places that had trash and needed clean up. These points are placed on a map so that people can see local areas that need people to pick up trash right now. In addition, we add whether or not there is recyclable material in the trash.

#How We built it
The project is built with mongodb as the database, python on the backend, microsoft vision api for the machine learning, Flask as the web framework and angularjs in the front end.

#Challenges We ran into
Backend: initially we started with node js in the back end with flask. But we soon realized the cognitive api only provides support for images that are already hosted on the web. We first approached the problem by using clouderina but that api wasnt consistent so we switched languages

issues with mongodb -issues with flask -issues with front end implementation
Accomplishments that I'm proud of
We were able to classify most images containing trash correctly and use microsoft's api to our use case. We were able to click a picture using our device and then upload it to Scoop whose location was shared using facebook. Representing set of locations containing trash on map in frontend.

#What we learn
How to access Google Map API How to write Express.js How to use Microsoft's computer vision API

#What's next for Scoop
We want to extend our solution to further classify trash as recyclable/non-recyclable. We want to extract hashtags from image and location, so that the same can be used to post to facebook.
