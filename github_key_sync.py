#!/usr/bin/env python3
from ghapi.all import GhApi
import requests, tempfile, subprocess, base64, hashlib
import pgpy
from config import config

KEY_LIST_URL = config["key_list_url"]
KEY_SIG_URL = config["key_sig_url"] or KEY_LIST_URL + ".sig"
KEY_PATH = config["key_path"]

def get_key(key_line):
        split = key_line.split(' ')
        if len(split) == 3:
                return (split[0] + ' ' + split[1], split[2])
        pubkey_bytes = base64.b64decode(split[1])
        m = hashlib.sha256()
        m.update(pubkey_bytes)
        return (split[0] + ' ' + split[1], "SHA256:" + base64.b64encode(m.digest()).decode().strip('='))

api = GhApi(token=config["github_token"])

github_keys = dict()
for key in api.users.list_public_ssh_keys_for_authenticated_user():
        github_keys[key.key] = key["title"]

tempdir = tempfile.TemporaryDirectory()
authorized_keys_file = requests.get(KEY_LIST_URL).text
authorized_keys_sig = requests.get(KEY_SIG_URL).content
key, _ = pgpy.PGPKey.from_file(KEY_PATH)
sig = pgpy.PGPSignature.from_blob(authorized_keys_sig)
if not sig:
        raise RuntimeError("BAD SIGNATURE!")
authorized_keys_keys = [get_key(l) for l in authorized_keys_file.split('\n') if l.strip() != '' and not l[0] == '#']
authorized_keys = {key:name for key, name in authorized_keys_keys}

add_keys = list()
remove_keys = list()
for key in authorized_keys:
        if key not in github_keys: add_keys.append(key)
for key in github_keys:
        if key not in authorized_keys: remove_keys.append(key)

for key in api.users.list_public_ssh_keys_for_authenticated_user():
        if key["key"] in remove_keys: 
                api.users.delete_public_ssh_key_for_authenticated_user(id=key["id"])
for key in add_keys:
        api.users.create_public_ssh_key_for_authenticated_user(key=key, title=authorized_keys[key])

username = api.users.get_authenticated()["login"]
existing_signing_keys = {key["key"]:key["title"] for key in api.users.list_ssh_signing_keys_for_user(username)}
for key, title in authorized_keys.items():
        if key not in existing_signing_keys:
                api.users.create_ssh_signing_key_for_authenticated_user(title=title, key=key)