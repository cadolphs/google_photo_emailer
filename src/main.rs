mod infrastructure;

use infrastructure::{google_photo_login::get_login_token, google_photo_client::get_albums};



fn main() {
    let token = get_login_token().expect("Something went wrong with the token");
    
    let albums = get_albums(token);

    for album in &albums {
        println!("{}", album.title);
    }
}