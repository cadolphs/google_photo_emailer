use reqwest::blocking::Client;
use serde::{Deserialize, Deserializer};

mod infrastructure;

use infrastructure::google_photo_login::get_login_token;

#[derive(Deserialize)]
struct Albums {
    albums: Vec<Album>,
    next_page_token: Option<String>
}

#[derive(Default, Deserialize)]
#[serde(default)]
struct Album {
    id: String,
    title: String,
    productUrl: String,
    coverPhotoBaseUrl: String,
    coverPhotoMediaItemId: String,
    isWriteable: Option<String>,
    #[serde(default, deserialize_with= "from_str")]
    mediaItemsCount: usize
}

use std::fmt::Display;
use std::str::FromStr;
fn from_str<'de, T, D>(deserializer: D) -> Result<T, D::Error>
    where T: FromStr,
          T::Err: Display,
          D: Deserializer<'de>
{
    let s = String::deserialize(deserializer)?;
    T::from_str(&s).map_err(serde::de::Error::custom)
}

fn main() {
    let token = get_login_token().expect("Something went wrong with the token");
    
    let client = Client::new();
    let res = client.get("https://photoslibrary.googleapis.com/v1/albums")
        .bearer_auth(token.secret()).send().unwrap();
            
    println!("Calling the http get requests returned: {:?}", res);
            
    let albums: Albums = res.json().expect("Failed to parse response into Albums struct");

    for album in &albums.albums {
        println!("{}", album.title);
    }
}
