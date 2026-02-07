# AirPlay

Select AirPlay device on a Mac.

Found here: https://github.com/bpetrynski/airplay-cli

Create an audio file from a message (text2speech)

```shell
say -o welcome.aiff welcome home
```

Or in a different language (e.g. Dutch) see voices.txt

```shell
say -o welkom.aiff --voice=Xander welkom thuis
```

And playback the file

```shell
afplay path/to/file.aiff
```
