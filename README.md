# My attempt at a Google Photo emailer
Because there's no easy automation for emailing Google Photo pictures to someone, I'll try and make my own.

In my previous attempt (see earlier commits) I tried too many new things at once:
- Developing in a cloud dev environment (GitPod)
- Developing in Rust
- Working with OAuth2
- Working with REST APIs
- Trying James Shore's "testing without mocks" techniques.

That made for slow development for a product I can't spend that much time on. So now, let's do it a bit easier:
- Develop locally
- Develop in Python. I know Python inside out **and** it has lots of well-developed packages. (Rust is still awesome!)
- Skip the OAuth2 and Google Photo rest stuff for now and JUST email photos from a folder!
- Still try and use James Shore's "testing without mocks" techniques

# First milestone
The splitting of a project into milestones shouldn't just be based on the characteristics of the project itself; it should also take into account 
the skills and knowledge of the developers. So, for me right now, a first milestone would just be to write a python script that sends an email on my behalf. 

## Steps taken:
- Set up virtual environment with Python 3.11.
- Google "How to send emails on Google's behalf" or whatever. Get some advice using their REST API, getting client secrets and packages to install.
- Install required packages and use the example script to send a simple test email ✅.

## Next steps
- Can I store the auth token so I don't have to go through those steps every time?
- How to attach a file to it?
- Using the testing concepts?

# First test
2023-08-21

So. I have a very simple script that just authenticates with Google and sends a test email to myself. That's some sort of infrastructure, so I should put it into an infrastructure wrapper, and also provide something nullable.

For now, I'll provide two methods, `authenticate` and `send_email`. Those go into the high-level class `EmailClient` which is 
just a wrapper around the Google API methods used to authenticate and send email. Then, I also write a stubbed-out version of 
that class which lets me turn off the "actually talking to Google" part while still having a class that behaves _like_ the 
emailer.

One thing to note: We're not actually running any unittests yet. I think that is premature anyway. The code right now is just 
passing on calls from one source to the other with no logic. I don't want to run tests on the actual Auth flow because that would 
require steering the browser with Selenium or whatever and would just be super annoying.

# Reloading and refreshing credentials
2023-08-22

So let's see what I can do next: Reload stored credentials. How would I _test-drive_ such a feature? Right now I just have to _spike_ it because I'm unsure on what to do...

Actually, it might be that my classes are too big! Right now, `GmailAPI` is responsible for both the authentication and the 
sending of email. We can split that up.

So. Now we have one class for sending email and one for authenticating. That class should then handle storing and loading from 
config, and it should really be the default behavior. And that didn't turn out so hard after all. The API handles the 
storing, loading, and refreshing quite nicely.

How have I followed the testing? Not so well. I think to completely follow that approach, I would have had to write even lower level wrappers. The `GoogleAuthAPI` class relies on some lower infrastructure, and that is what I would have had to stub out.

But now what does that mean for the `GmailSendClient`? I don't want to duplicate my logic in the stub and the actual class. The 
actual composing of the message is _application_ and _logic_. Only the sending of it is infrastructure. So next, we'll see if we can 
stub that out.

Great. Instead of an `EmailClient` with a complicated embedded stub, the `EmailClient` now has an injectable dependency on the 
actual `sender`. The email client will compose the message and the sender will send it off; and because that is an infrastructure 
dependency, it's nice to be able to turn that off.