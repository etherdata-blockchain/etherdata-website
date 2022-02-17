import fs from "fs";
import * as core from "@actions/core";
import * as github from "@actions/github";
import moment from "moment";
import nunjucks from "nunjucks";

interface Version {
  upload_date: string;
  version: string;
  url: string;
}

interface VersionList {
  ios: Version;
  android: Version;
}

interface Asset {
  name: string;
  updated_at: string;
  browser_download_url: string;
}

function readVersion(
  assets: Asset[],
  versionList: VersionList,
  version: string
) {
  for (let asset of assets) {
    if (asset.name.includes("ipa")) {
      versionList.ios.url = asset.browser_download_url;
      versionList.ios.version = version;
      versionList.ios.upload_date = moment(asset.updated_at).format(
        "YYYY-MM-DD"
      );
    }

    if (asset.name.includes("apk")) {
      versionList.android.url = asset.browser_download_url;
      versionList.android.version = version;
      versionList.android.upload_date = moment(asset.updated_at).format(
        "YYYY-MM-DD"
      );
    }
  }
}

const versionList: VersionList = JSON.parse(
  fs.readFileSync("./version.json", "utf-8")
);
const assets = github.context.payload.release.assets;
const version = github.context.payload.release.tag_name;

readVersion(assets, versionList, version);
// read template
const templateFile = fs.readFileSync("./templates/index.html", "utf-8");
const template = nunjucks.compile(templateFile);
const html = template.render({
  ios: versionList.ios,
  android: versionList.android,
});
// write html
fs.writeFileSync("./dist/index.html", html);
// write version.json
fs.writeFileSync("./version.json", JSON.stringify(versionList));
core.notice(`Successfully generated index.html and version.json`);
