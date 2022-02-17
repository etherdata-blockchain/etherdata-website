from jinja2 import Template
import importlib.resources as pkg_resources
import os
import json
from dateutil import parser
from datetime import datetime
from . import templates


def read_version(old_version, assets, tag):
    ios_version_dict = old_version['ios']
    android_version_dict = old_version['android']

    for asset in assets:
        if "ipa" in asset.get('name'):
            ios_version_dict['upload_date'] = parser.parse(
                asset.get('updated_at')).strftime("%Y-%m-%d")

            ios_version_dict['version'] = tag
            ios_version_dict['url'] = asset.get('browser_download_url')

        if "apk" in asset.get('name'):
            android_version_dict['upload_date'] = parser.parse(
                asset.get('updated_at')).strftime("%Y-%m-%d")

            android_version_dict['version'] = tag
            android_version_dict['url'] = asset.get('browser_download_url')

    return ios_version_dict, android_version_dict


def main():
    template = Template(pkg_resources.read_text(templates, "index.html"))

    # read previous version from file
    with open("version.json", "r") as f:
        old_version = json.load(f)

    ios_version_dict, android_version_dict = read_version(
        assets=json.loads(os.environ.get('ASSETS')), tag=os.environ.get('TAG'), old_version=old_version)

    # use android and ios version and url to render html
    html = template.render(android_version=android_version_dict['version'],
                           ios_version=ios_version_dict['version'],
                           android_url=android_version_dict['url'],
                           ios_url=ios_version_dict['url'],
                           ios_date=ios_version_dict['upload_date'],
                           android_date=android_version_dict['upload_date'],)

    # write template to dist folder
    with open("dist/index.html", "w") as f:
        f.write(html)

    # write version to file
    with open("version.json", "w") as f:
        json.dump({
            "ios": ios_version_dict,
            "android": android_version_dict
        }, f)
