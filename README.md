# LGWebOSRemote (@ouija fork)
Command line webOS remote for LGTVs. This tool uses a connection via websockets to port 3000 on newer LG TVs, there are other tools which use a restful connection to port 8080 however that port is closed on newer firmware versions.

## ouija fork changes: 

This version saves the configuration file under the same folder path as the script itself; Not under the user home directory.
<br><br>
**NEW:** *notificationWithURL* command, allows *any* media URL (image, rtsp video, etc) to be passed and displayed as thumbnail with notification message.<br>
 _(note that this requires both **ffmpeg v4.2.2>** and **base64 [coreutils-base64]** packages installed to work correctly!)_

## Supported models

### Tested with

UF830V, UJ6570, [please add more!]

Updated to work with **Python 3.8.3** on Linux (QNAP w/Entware), your milage may vary.

### Likely supports

All devices with firmware major version 4, product name "webOSTV 2.0"

Also tested by @ouija with "webOSTV 3.5"

## Available Commands
    scan
    auth                  Hostname/IP     Authenticate and exit, creates initial config ~/.lgtv.json
    audioStatus           
    audioVolume           
    closeApp              appid
    getTVChannel          
    input3DOff            
    input3DOn             
    inputChannelDown      
    inputChannelUp        
    inputMediaFastForward  
    inputMediaPause       
    inputMediaPlay        
    inputMediaRewind      
    inputMediaStop        
    listApps              
    listChannels          
    listInputs            
    listServices          
    mute                  muted
    notification          message
    nofificationWithURL   message  url
    off                   
    on                    
    openAppWithPayload    payload
    openBrowserAt         url
    openYoutubeId         videoid
    openYoutubeURL        url
    setInput              input_id
    setTVChannel          channel
    setVolume             level
    startApp              appid
    swInfo                
    volumeDown            
    volumeUp

## Install

Requires wakeonlan, websocket for python and arp (in Debian/Ubuntu: apt-get install net-tools)

There's a requirements.txt included

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Example usage

    $ python lgtv.py on
    $ python lgtv.py off

    # If you have the youtube plugin
    $ python lgtv.py openYoutubeURL https://www.youtube.com/watch?v=dQw4w9WgXcQ

    # Otherwise, this works reasonably well
    $ python lgtv.py openBrowserAt https://www.youtube.com/tv#/watch?v=dQw4w9WgXcQ

## Caveats

You need to auth with the TV before being able to use the on command as it requires the mac address.

## Bugs

YouTube doesn't appear to work via the openYoutubeURL or openYoutubeId command with "webOSTV 3.5"
I believe it is because YouTube needs to be paired with the device and this script currently doesn't support that.

I found some examples of this 'pairing' method in other sources:

- https://github.com/ConnectSDK/Connect-SDK-iOS-Core/blob/master/Services/WebOSTVService.m
- https://github.com/ConnectSDK/Connect-SDK-Android-Core/blob/master/src/com/connectsdk/service/WebOSTVService.java
- https://github.com/ConnectSDK/Connect-SDK-Android-Core/pull/93/files?diff=split&short_path=04c6e90&unchanged=expanded
- https://www.programcreek.com/java-api-examples/index.php?api=com.connectsdk.core.AppInfo

I also found the "mute" command does not work unless invoked with the command `python lgtv.py mute muted` and then a volumeUp or volumeDown command will unmute.
