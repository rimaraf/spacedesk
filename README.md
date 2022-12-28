# SpaceDesk - a daily dosage of desktop space

I've written a small script that automatically downloads and changes your desktop background to the latest and greatest ["Astronomy Picture of the Day"](https://apod.nasa.gov/apod/astropix.html) from NASA. The script also supports updating a secondary display, which will get yesterdays picture.

It has only been testet in MacOS on an Apple M1 machine, and I expect that the current version at least won't support secondary displays on Intel-Mac platforms at the moment.

I myself call this code from a simple zsh script placed in the Login item list under my user profile. Sometimes I’ve had trouble running it alongside the other startup applications, so I’ve added some seconds of sleep in my zsh-script before this script is executed.

Have fun!