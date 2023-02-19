use oauth2::{basic::BasicClient, TokenResponse};
// Alternatively, this can be oauth2::curl::http_client or a custom.
use oauth2::reqwest::http_client;
use oauth2::{
    AccessToken, AuthUrl, AuthorizationCode, ClientId, ClientSecret, CsrfToken, PkceCodeChallenge,
    RedirectUrl, Scope, TokenUrl,
};

use std::env;
use std::io::{BufRead, BufReader, Write};
use std::net::TcpListener;
use url::Url;

pub struct LoginClient {
    google_client_id: Option<ClientId>,
    google_client_secret: Option<ClientSecret>,

    auth_url: AuthUrl,
    token_url: TokenUrl,
}

impl LoginClient {
    pub fn new() -> Self {
        let google_client_id = match env::var("google_photo_client_id") {
            Ok(client_id) => Some(ClientId::new(client_id)),
            Err(_) => None,
        };

        let google_client_secret = match env::var("google_photo_client_secret") {
            Ok(client_secret) => Some(ClientSecret::new(client_secret)),
            Err(_) => None,
        };

        let auth_url =
            AuthUrl::new("https://accounts.google.com/o/oauth2/v2/auth".to_string()).unwrap();
        let token_url =
            TokenUrl::new("https://www.googleapis.com/oauth2/v3/token".to_string()).unwrap();

        LoginClient {
            google_client_id,
            google_client_secret,
            auth_url,
            token_url,
        }
    }

    pub fn get_login_token(self) -> Result<AccessToken, String> {
        
        let client = BasicClient::new(
            self.google_client_id.expect("Must provide a client id"),
            Some(self.google_client_secret.expect("Most provide a client secret")),
            self.auth_url,
            Some(self.token_url),
        )
        .set_redirect_uri(
            RedirectUrl::new("http://localhost:8080".to_string()).expect("Invalid redirect url"),
        );

        let (pkce_code_challenge, pkce_code_verifier) = PkceCodeChallenge::new_random_sha256();

        let (auth_url, csrf_state) = client
            .authorize_url(CsrfToken::new_random)
            // Set the desired scopes.
            .add_scope(Scope::new(
                "https://www.googleapis.com/auth/photoslibrary.readonly".to_string(),
            ))
            // Set the PKCE code challenge.
            .set_pkce_challenge(pkce_code_challenge)
            .url();

        println!("Browser to: {}", auth_url);

        // A very naive implementation of the redirect server.
        let listener = TcpListener::bind("127.0.0.1:8080").unwrap();
        for stream in listener.incoming() {
            if let Ok(mut stream) = stream {
                let code;
                let state;
                {
                    let mut reader = BufReader::new(&stream);

                    let mut request_line = String::new();
                    reader.read_line(&mut request_line).unwrap();

                    let redirect_url = request_line.split_whitespace().nth(1).unwrap();
                    let url = Url::parse(&("http://localhost".to_string() + redirect_url)).unwrap();

                    let code_pair = url
                        .query_pairs()
                        .find(|pair| {
                            let &(ref key, _) = pair;
                            key == "code"
                        })
                        .unwrap();

                    let (_, value) = code_pair;
                    code = AuthorizationCode::new(value.into_owned());

                    let state_pair = url
                        .query_pairs()
                        .find(|pair| {
                            let &(ref key, _) = pair;
                            key == "state"
                        })
                        .unwrap();

                    let (_, value) = state_pair;
                    state = CsrfToken::new(value.into_owned());
                }

                let message = "Go back to your terminal :)";
                let response = format!(
                    "HTTP/1.1 200 OK\r\ncontent-length: {}\r\n\r\n{}",
                    message.len(),
                    message
                );
                stream.write_all(response.as_bytes()).unwrap();

                println!("Google returned the following code:\n{}\n", code.secret());
                println!(
                    "Google returned the following state:\n{} (expected `{}`)\n",
                    state.secret(),
                    csrf_state.secret()
                );

                // Exchange the code with a token.
                let token_response = client
                    .exchange_code(code)
                    .set_pkce_verifier(pkce_code_verifier)
                    .request(http_client)
                    .expect("Something went wrong in fetching the access token");

                let token = token_response.access_token().to_owned();
                return Ok(token);
            }
        }

        Err("Error 👻".to_string())
    }
}

pub fn get_login_token() -> Result<AccessToken, String> {
    LoginClient::new().get_login_token()
}
