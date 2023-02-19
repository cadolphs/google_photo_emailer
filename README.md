# google_photo_emailer
I need a tool to automatically forward photos added to a particular Google Photo Album to a particular email address. I'll develop it in this repo and hope that parts of it might be useful for others. 

From what I gather, popular automation tools like IFTTT or Zapier don't have Google Photos integrations, so I'll need to do something custom.

This will take some time as it's not urgent and I'm learning about a number of web things as I go (e.g. authenticating with Google via oauth2 in an application).

# Thoughts and brainstorms so far
## 2023-02-17
So, what now? Was thinking a bit about right way to do testing for this; but do I even _want_ to run integration tests against a rest api? Definitely not against the real Google API because even getting the authorization 
right is a pain. 

First, let's move all that log-in token stuff into its own module and worry about refactoring later. :)

## 2023-01-17
Great success. Figured out how to take the token and use it to build a proper request against the 
endpoint _and_ how to parse that stuff into a struct. The current version, when run, prints a list 
of my album titles. Yay.

## 2023-01-14
Let's see how far we get with the example from that rust oauth2 crate for a desktop application. 

Actually, that worked really well. Just needed to figure out a few pieces about setting things up properly with the gitpod workspace. There's a gitpod local companion that allows 
port forwarding from localhost; that way, when I open the authorization URL and it wants to send the token to my actual localhost, that thing gets forwarded to the 
server listening on the gitpod site. That's fantastic! So. It looks like authorization works. Next, I'll have to figure out how to then actually make requests with that token.

## 2023-01-13
Let's do a bit of initial spiking, getting some familiarity with the parts I need to deal with. I'll need to be able to authenticate with Google Photos. So the first thing I'll try and manage is to just get a list of albums from a 
Google Photos account, as a simple command line app in rust. First I'l do the Google Photo API stuff. Clicking around their documentation, I'll need to make a project and enable the Google Photo API for it.

So, I created a project and added an oauth2 setting specifically for Google Photo as read-only. Now to figure out how to access things. For now, to keep things simple, I do the "Desktop App" workflow; then I don't have to run a webserver to listen for Google's token being sent back. So, secret and client id get added as (secret) environment variables to my gitpod account.

Great. Next, the whole oauth authorization protocol is complicated, so I'll have to find a library to do that for me. That'll have to wait for next time.

## 2023-01-08
As of 2023-01-08. My idea is to use Rust because a) why not and b) it's small and lightweight and fun...
