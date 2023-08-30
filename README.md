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

Quick reminder from James Shore's post: Logic classes aren't allowed to talk to infrastructure classes. They have to go through the Application layer.

Before dealing with the refresh logic, I should then probably try to authenticate? Well, that doesn't work because the google api stuff expects the credentials to have an `authorize` method. So again, it's mixing 
logic with infrastructure.

I also already know that my token would need to be refreshed. So maybe let's do that logic first.

One thing I can do is work with a login client and expect that the login client logs us in. That client should then wrap the interaction with Google's credentials.

Hmmm. But really. There's the google third party API that should help me have a straightforward way with all this. But it's messy. I'll want to test-drive my way to a logged-in service. But not outside-in. Plus, I shouldn't be testing these libraries themselves, 
so I shouldn't really have to bother with using my own http client in anything!

## More thoughts
Okay, I'm overthinking and going slow, because I'm trying to follow the article exactly so that I can learn this technique. It's no surprise that it feels awkward at first.

Maybe I should start with "legacy" code and then "descend" or "climb" the ladder to see where I can get to?

One thing: This is a script that's supposed to run end-to-end, so really all these app tests are maybe a bit overkill? Or maybe not.

Instead, I guess, the tests would go step after step of running the full thing.

Right now, we read the credentials from a file. Next step: Build a mail service with these credentials.

# 2023-08-29
Okay, maybe going "top down" at the start is easier when you're not that familiar yet with the overall process and outcomes. There are many patterns to learn about and use. A-Frame architecture, the infrastructure patterns, etc.

So. I built a LoginClient that has dependencies on being able to build a credentials class and on being able to build a service.
Maybe those should be instances instead of classes.

----

Great. So, for the refresh logic part I now have a `LoginClient` that's nullable. The thing it depends on is a class that turns my logic credentials into the GoogleCredentials, and we need that to be nullable, too. Similarly, now I'd need the service builder as a dependency. 

Big progress. Added a nullable version of the google service builder, and added output tracking for that as well. Now the thing is 
that, technically, I should do a focused integration test for these things, but I really don't want my tests to hit the google service all the time, _and_ I don't think setting up my own server and mocking around there makes sense. Instead, I can be 
content that the overall logic seems to work and move on.

----

So, now that I can create a `LoginClient` and log in and build a service, I'll need to be able to send emails. Because the 
email will be sent from Google, that's a third party infrastructure dependency that I don't want to deal with personally, and 
I don't want to build some service that would listen to the test email, right?

Oh wait. Before moving on, I'll need to integrate the login stuff into the app.

----

Great. Now I'll want to write a super simple email client. The app will then use that email client.

How to go about it? What sort of test would I add in the app? Again, don't go outside in. We _choose_ that we want the 
app to send an email. We'll need an infrastructure wrapper for this, so let's go ahead with that.

"But what about using TDD to decide the interface of the infrastructure wrapper?" 
Meh, that would be outside-in testing again.

So. There's the email sender and the email builder. Let's first create the infrastructure wrapper for the sender.

----
Thinking through the dependencies here. So. The LoginClient eventually spits out a _service_, which is what the 
`EmailSender` depends on to actually send the email. 

For parameterless instantiation and all that, this doesn't work! 

What about providing it after the fact? Yeah. "Don't connect to external systems in the constructor". Of course _passing in_ the 
created service wouldn't count as connecting in the constructor. But it's still something awkward. That's where the connect comes in.

Anyway. That all seems to more or less work. The only problem now is that at some point I do have to test that google 
actually likes that format.

Now, trying that, we run into the issue that the token cannot be refreshed, so we need to run the browser authentication...

Okay, feeling more comfortable with these thin wrappers. It seems like a lot of effort to wrap a single function call, but 
it leads to a massive decoupling of our code from the underlying infrastructure.

Next would be questions on how to _test_ these things. If it's really just a thin wrapper, it doesn't need tests.

----
So. Where to put the browser logic? In the login client! Let's write some tests. But when does it happen? If the refresh fails.

----
Not so sure about the whole credentials stuff. I find it hard to inject the behavior of a failed server response.

Maybe I'm putting too much logic into `LoginClient` when that should be the app. It also means the `LoginClient` needs complicated "factory" logic. How would it look like if it was just all in the app?

Also, `LoginClient` doesn't have nicely visible behavior, with all that code stuff. There isnn't really a login process there anyway, there's just the job of procuring new credentials.

Now, how can I refactor this to get rid of login client? By inlining the class?

The real infrastructure wrappers usually don't have much logic in them.

----
Okay, so let's try a new thing. From a different angle?

----
Liking the new auth flow a bit better! Should be making nice 
step by step progress now. Next step, storing the credentials 
after getting new ones.

# 2023-08-30
