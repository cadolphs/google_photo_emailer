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

# More testing
2023-08-23
Because this is about learning stuff, let's make this about getting the testing as close to the ideal as possible.

So. Let's start with the first step. The LoginClient. The point of that is that it calls the google api to show a browser window.
The infrastructure here is the library call that opens the browser and the server that listens to the response. Those are all 
encapsulated in the python module.

Let's go with the "grow evolutionary seeds" approach. The article (James Shore on Testing w/o Mocks) describes that this is the way to avoid the usual approach of outside-in testing that requires mocks.

So. The first seed, hardcoding the infrastructure, would just be something that returns my credentials. Done that. Next, we need to 
implement a barbones Infastructure Wrapper for the one infrastructure value we hardcoded. We test-drive it with narrow integration tests 
and code just enough to provide one real result. No need to make it robust or reliable.

In my case then I could use the stored credentials / refresh path. It's not robust or reliable because, if things are expired or don't work out, I'd have to do the browser flow. But it's _something_.

So. We need to _test-drive_ the _Infrastructure Wrapper_ with _Narrow Integration Tests_.
Now that this is done, we need to add a nullable version.

If I wanted to be _super_ clear, then loading the credentials from a file should be its own class with its own nullable wrapper. That can have some nice benefits for my tests: For example, I _should_ test-drive the "check if token is expired, then use the refresh token" logic.

Still left to do: Use the infrastructure wrapper in the app.

# 2023-08-25
Actually, let's start over because I was going too fast: There's so many infrastructures layered into all of this. To deal with the credentials, we need to load them from a file, then pass that into the 
`Credentials` class which is _kind of_ an infrastructure class because it's part of the google API. 

It's a class with an infrastructure dependence that I don't control. So to me that seems like I do want to wrap it, and then use delegates?

Maybe the thread here is: First step, load credentials from a file and return a dictionary.

# 2023-08-28
Okay, so writing a credential's loader that really just opens a json file might seem overkill. Remember that rant "don't use classes so much". The benefit is in the ability to isolate the logic of loading credentials from a file from the actual file system 
infrastructure, which makes the tests more easy to write. NOw with our nullable `CredentialsLoader` we can integrate it into the 
test for the app.

When writing the test for the actual app, we can already see benefits of this decoupling: We know that the loader reads files properly because of the focused integration test we wrote for it. So when writing tests for the app, we don't need to be testing that reading from files works properly. Instead, we use the nulled version, which _simulates_ the loading.

Let's stop and think for a second if we're not doing a mistake similar to what happens when overusing mocks: That all we're testing is the test itself. Because we're still at the very simple app seed stage, let's not worry that the logic we're testing is too simple. But we are indeed using a real class... Let's see how that plays out once we have more complicated logic.

Our next desired behavior is that the dictionary credentials get loaded into a proper `Credentials` class. The question here is, 
where do I test-drive that? Do I start with what I want to see in the app class? That would be another "outside in" approach. Instead, we'll test-drive a narrow infrastructure wrapper for the credentials class. We need that because that class has some 
features around talking to the auth service.

But actually, maybe I don't even want to accept the muddling of what should be a pure value class with that should be infrastructure. I can just code my own "pure" value object for the credentials, and then implement the refreshing in some other way. 
Which, really, just means I'll want to refactor away from the dictionary credentials to an encapsulated credentials.

Okay, so with that under way, I can use my own data class. I wonder if those things actually work with the google API. But we'll see. Next up would be the expiration and refresh logic.