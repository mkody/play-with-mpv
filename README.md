# Play with MPV
WebExtension and python server that allows you to play videos in webpages with MPV instead.  
Works on [hundreds of sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) thanks to yt-dlp,
and even torrents if you install [peerflix](https://github.com/mafintosh/peerflix).

## Installation
1. Install [MPV](https://mpv.io/installation/)
2. Install [Python 3.10+](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installing/)
3. Install the [chrome](https://chrome.google.com/webstore/detail/play-with-mpv/hahklcmnfgffdlchjigehabfbiigleji) or [firefox](https://addons.mozilla.org/firefox/addon/play-with-mpv/) extension
4. Run `pip install git+git://github.com/mkody/play-with-mpv --user`
5. Start server by running `play-with-mpv`

(optional) Install [fair-use](https://chrome.google.com/webstore/detail/fair-use-download/fhokdginneihphnneihijgbhbdoehjaj) extension.  
(optional) Install [peerflix](https://github.com/mafintosh/peerflix) to stream torrents.  
(optional) Install [mkchromecast](http://mkchromecast.com/) `pip install git+git://github.com/muammar/mkchromecast --user`
and [this extension](https://chrome.google.com/webstore/detail/edeepcccaejnnodlpmcoackkdgaijakg).  
(recommended) Install `yt-dlp` through your package manager for frequent updates.  

## Usage
Right-click [this link](https://www.youtube.com/watch?v=dQw4w9WgXcQ) and select "Play with MPV".
MPV should popup and start playing the video. (Ctrl+Space also works)

![screenshot](https://github.com/mkody/play-with-mpv/raw/master/screenshot.png)

## Autostart
- ~~Linux: `cp {/usr,~/.local}/share/applications/mkody.play-with-mpv.desktop ~/.config/autostart`~~
- MacOS: [instructions](https://stackoverflow.com/questions/29338066/mac-osx-execute-a-python-script-at-startup)
- Windows [instructions](https://stackoverflow.com/questions/4438020/how-to-start-a-python-file-while-windows-starts)

## Protips
MPV is [highly configurable](https://mpv.io/manual/stable/), this is just how I like to use it.

To start in the corner, have no border, and stay on top: edit `~/.config/mpv/mpv.conf`
```
ontop=yes
border=no
window-scale=0.4
geometry=100%:100%
```

In order to resize the window without borders, add keybinds: edit `~/.config/mpv/input.conf`
```
` cycle border
ALT+UP add window-scale 0.05
ALT+DOWN add window-scale -0.05
```
