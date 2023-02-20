use std::fmt::Display;
use std::str::FromStr;

use reqwest::blocking::Client;
use serde::{Deserialize, Deserializer};

#[derive(Deserialize)]
struct Albums {
    albums: Vec<Album>,
    next_page_token: Option<String>
}

#[derive(Default, Deserialize)]
#[serde(default)]
pub struct Album {
    pub id: String,
    pub title: String,
    pub productUrl: String,
    pub coverPhotoBaseUrl: String,
    pub coverPhotoMediaItemId: String,
    pub isWriteable: Option<String>,
    #[serde(default, deserialize_with= "from_str")]
    pub mediaItemsCount: usize
}


fn from_str<'de, T, D>(deserializer: D) -> Result<T, D::Error>
    where T: FromStr,
          T::Err: Display,
          D: Deserializer<'de>
{
    let s = String::deserialize(deserializer)?;
    T::from_str(&s).map_err(serde::de::Error::custom)
}

pub fn get_albums(token: oauth2::AccessToken) -> Vec<Album> {
    let client = Client::new();
    let res = client.get("https://photoslibrary.googleapis.com/v1/albums")
        .bearer_auth(token.secret()).send().unwrap();
            
    println!("Calling the http get requests returned: {:?}", res);
            
    let albums: Albums = res.json().expect("Failed to parse response into Albums struct");
    // TODO this doesn't yet parse the next_page_token!
    albums.albums
}