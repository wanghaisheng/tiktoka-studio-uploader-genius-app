
pip install requirements.txt

由于i18n_json==0.0.6最新的修改并未打包发布，需要手动安装


python main.py



## Thumbnail Generation

* 1. Randomly select keyframes as the base for thumbnails [X]
* 2. Extract the first frame of the video as the base for thumbnails [X]
* 3. Read images from a specified folder to use as the base for thumbnails
* 4. Read thumbnail templates and render thumbnails

## Proxy Management
* 0. Batch import proxy lists
* 1. Import proxy lists and automatically group them by geographical location [X]
* 2. Proxy query to obtain geographical location and time zone, supports IP location and IPAPI [X]
* 3. Proxy validation, check if they can access Google, Facebook, and several fingerprint technology provider websites [X]
* 4. Proxy scoring, evaluating native IPs, anonymity, and more [X]

## Account Management
* 1. Add accounts, enter usernames and passwords, and generate cookies automatically
* 2. Bind accounts to proxies, select at least one, and have the option to choose multiple proxies from the same geographical location as candidates. Defaults to switching to a candidate proxy in case of connection failure [X]

## Upload Configuration and Metadata Management
* 0. Metadata format, please refer to [meta file docs](meta-json-docs.md)
* 1. Manually edit video metadata, prepare video and thumbnail information manually in advance, and use an editor such as [jsoncrack.com/editor](https://jsoncrack.com/editor)
* 2. Automatically generate metadata and export JSON files, which can be edited by users after export
* Create upload configurations, enter account and proxy information, description prefixes, suffixes, tags, and publishing strategies. By default, load the configuration file used in the previous session
* Select a video folder to generate video metadata base files
* 2.0 Video pre-processing [X]
* 2.0.1 Remove background music
* 2.0.2 Use copyright-free music
* 2.0.3 Embed invisible watermarks
* 2.1 If there are images with the same name in the video folder, consider them as thumbnails
* 2.2 If there are no images with the same name in the video folder, execute thumbnail generation tasks
* 2.3 If there is a .des file with the same name in the video folder, consider it as video description
* 2.3 If there is a .title file with the same name in the video folder, consider it as video title
* 2.3 If there is a .srt file with the same name in the video folder, consider it as video subtitle

default language is en,如果找不到不带后缀的文件，则使用后缀为en的文件，如果找到带en的，则随机用一个找到的文件



we store other meta in otherDes,otherTitles,otherSubtitles

for multiple language des, use suffix such as zh-cn, xxxx-zh-cn.des

for multiple language title, use suffix such as zh-cn, xxxx-zh-cn.title

for multiple language srt, use suffix such as zh-cn, xxxx-zh-cn.srt


* 2.4 Plan the scheduled publication date for each video based on the timing publication strategy, the number of videos in the folder, and the daily public quantity limit
* 2.4.1 Strategy: Daily One Release
  - Daily public quantity is 1
  - If a publication time slot is not selected, use the default time of 10:15
  - If only one publication time slot is provided, e.g., 9:00, use that time slot.
  - If multiple time slots are provided, choose one randomly as the video's public time slot
* 2.4.2 Strategy: Daily Two Releases
  - Daily public quantity is 2
  - If a publication time slot is not selected, use the default time of 10:15
  - If only one publication time slot is provided, e.g., 9:00, all videos will use that time slot.
  - If two publication time slots are provided, e.g., 9:00 and 14:00, each video will use one of these time slots.
  - If multiple time slots are provided, choose two randomly as the video's public time slots
* 2.4.3 Strategy: Daily Four Releases
  - If a publication time slot is not selected, use the default time of 10:15
  - If only one, two, or three publication time slots are provided, choose one or two time slots randomly.
  - If four time slots are provided, use them as video's public time slots
  - The same pattern continues for Daily Six Releases and so on

## Upload Task Management
* 0. Edit task data
  - Select video metadata and analyze the number of videos
  - Choose upload strategies: single account publishing, primary-secondary account publishing, multi-account random publishing, multi-account average publishing
  - Choose account names, import pre-configured proxy information. If no proxies are available, you can manually add proxy information related to the account.
  - Generate and export upload task files for later import into the system
* 1. Import prepared video metadata, which can be single account single video, single account multiple videos, multiple accounts single video, or multiple accounts multiple videos. Refer to the metadata format. Each group of videos corresponds to an upload configuration item (the proxies and accounts used to upload the video). After importing, the system will automatically create upload tasks
* 2. View the list of pending upload tasks, edit corresponding fields, and set priority order
* 3. Click "Upload" to automatically pull the pending upload queue, execute the upload action, and return the video ID upon completion. Update the video upload status [X]
* 3.1 If there are top comments, continue with the comment posting action after video upload is completed, and record the status [X]
* 4. View the list of uploaded tasks
* 5. View the list of failed upload tasks and set up automatic retries [X]

Issue:

1. Thumbnail Tab
   - Select the format first, then select the folder; it does not trigger the automatic generation of metadata. Manual clicking on "check" is required.