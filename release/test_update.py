from unittest import mock
from .update import read_version


def test_read_version_happy_case():
    mock_data = {
        "ios": {
            "upload_date": "2021-09-10",
            "version": "2020.0.0.0",
            "url": ""
        },
        "android": {
            "upload_date": "2020-09-10",
            "version": "2020.0.0.0",
            "url": ""
        }
    }

    mock_assets = [
        {

            "name": "ETD-1.1.0-signed.ipa",
            "download_count": 1,
            "created_at": "2021-09-15T03:11:52Z",
            "updated_at": "2021-09-15T03:11:57Z",
            "browser_download_url": "https://github.com/etherdata-blockchain/etherdata-website/releases/download/1.1.0/ETD-1.1.0-signed.ipa"
        },
        {
            "name": "ETD-1.1.0.apk",
            "created_at": "2021-09-15T03:12:00Z",
            "updated_at": "2021-09-15T03:12:03Z",
            "browser_download_url": "https://github.com/etherdata-blockchain/etherdata-website/releases/download/1.1.0/ETD-1.1.0.apk"
        }
    ]

    ios, android = read_version(old_version=mock_data,
                                assets=mock_assets, tag="2020.0.0.1")

    assert ios['version'] == "2020.0.0.1"
    assert android['version'] == "2020.0.0.1"
    assert ios['upload_date'] == "2021-09-15"
    assert android['upload_date'] == "2021-09-15"


def test_read_version_happy_case_2():
    mock_data = {
        "ios": {
            "upload_date": "2021-09-10",
            "version": "2020.0.0.0",
            "url": ""
        },
        "android": {
            "upload_date": "2020-09-10",
            "version": "2020.0.0.0",
            "url": ""
        }
    }

    mock_assets = [
        {
            "name": "ETD-1.1.0.apk",
            "created_at": "2021-09-15T03:12:00Z",
            "updated_at": "2021-09-15T03:12:03Z",
            "browser_download_url": "https://github.com/etherdata-blockchain/etherdata-website/releases/download/1.1.0/ETD-1.1.0.apk"
        }
    ]

    ios, android = read_version(old_version=mock_data,
                                assets=mock_assets, tag="2020.0.0.1")

    assert ios['version'] == "2020.0.0.0"
    assert android['version'] == "2020.0.0.1"
    assert ios['upload_date'] == "2021-09-10"
    assert android['upload_date'] == "2021-09-15"
