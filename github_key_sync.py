#!/usr/bin/env python3
from github import Github
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

g = Github(config["github_token"])
github_keys = dict()
user = g.get_user()
for key in user.get_keys():
        github_keys[key.key] = key.title

tempdir = tempfile.TemporaryDirectory()
authorized_keys_file = requests.get(KEY_LIST_URL).text
authorized_keys_sig = requests.get(KEY_SIG_URL).content
key, _ = pgpy.PGPKey.from_file(KEY_PATH)
sig = pgpy.PGPSignature.from_blob(authorized_keys_sig)
if not sig:
        raise Error("BAD SIGNATURE!")
authorized_keys_keys = [get_key(l) for l in authorized_keys_file.split('\n') if l.strip() != '' and not l[0] == '#']
authorized_keys = {key:name for key, name in authorized_keys_keys}

add_keys = list()
remove_keys = list()
for key in authorized_keys:
        if key not in github_keys: add_keys.append(key)
for key in github_keys:
        if key not in authorized_keys: remove_keys.append(key)

for key in user.get_keys():
        if key.key in remove_keys: key.delete()
for key in add_keys:
        user.create_key(authorized_keys[key], key)