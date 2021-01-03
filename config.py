config = {
        "key_list_url": "http://example.org/authorized_keys",
        "key_sig_url": None, #uses key_list_url + ".sig"
        "key_path": "/home/user/your_gpg_key.asc", #path to your PGP pub key
        "github_token": "TOKEN_HERE" # a github personal access token with read/write ssh key privs
}