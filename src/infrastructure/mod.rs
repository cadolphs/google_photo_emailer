pub mod google_photo_login;

#[cfg(test)]
mod tests {
    #[test]
    fn smoke_test() {
        let res = super::google_photo_login::foo();
        assert_eq!(res, 42);
    }
}