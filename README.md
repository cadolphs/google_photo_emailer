# google_photo_emailer
I need a tool to automatically forward photos added to a particular Google Photo Album to a particular email address. I'll develop it in this repo and hope that parts of it might be useful for others. 

From what I gather, popular automation tools like IFTTT or Zapier don't have Google Photos integrations, so I'll need to do something custom.

This will take some time as it's not urgent and I'm learning about a number of web things as I go (e.g. authenticating with Google via oauth2 in an application).

# Thoughts and brainstorms so far
## 2023-01-13
Let's do a bit of initial spiking, getting some familiarity with the parts I need to deal with. I'll need to be able to authenticate with Google Photos. So the first thing I'll try and manage is to just get a list of albums from a 
Google Photos account, as a simple command line app in rust. First I'l do the Google Photo API stuff. Clicking around their documentation, I'll need to make a project and enable the Google Photo API for it.

So, I created a project and added an oauth2 setting specifically for Google Photo as read-only. Now to figure out how to access things. For now, to keep things simple, I do the "Desktop App" workflow; then I don't have to run a webserver to listen for Google's token being sent back. So, secret and client id get added as (secret) environment variables to my gitpod account.

Great. Next, the whole oauth authorization protocol is complicated, so I'll have to find a library to do that for me. That'll have to wait for next time.

## 2023-01-08
As of 2023-01-08. My idea is to use Rust because a) why not and b) it's small and lightweight and fun...
