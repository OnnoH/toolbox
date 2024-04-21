# Catch 22

https://www.merriam-webster.com/dictionary/catch-22

> no space left on device => remove files to free up space => no space left on device

## What happened?

I wanted to start an adventure with machine learning. For that I had my eye on Meta's Llama 3 model. Without doing any reading upfront I wanted those LLMs downloaded to my MacBook.

Easy as pie. Just sign up and you get an e-mail message with the appropriate links. Use a `download.sh` script from the specified GitHub repo and run it.

When on 1GB fiber, this runs very smooth. Just paste the URL and press enter (the default will trigger the download of all available models). A mistake as it turns out. Little did I know about the size :-(.

E.g. `du -h -d 2` gives you an idea about it.

```text
132G	./llama3/Meta-Llama-3-70B
 15G	./llama3/Meta-Llama-3-8B-Instruct
132G	./llama3/Meta-Llama-3-70B-Instruct
 15G	./llama3/Meta-Llama-3-8B
724K	./llama3/.git
 44K	./llama3/llama
293G	./llama3
636K	./PurpleLlama/Llama-Guard
8.0K	./PurpleLlama/.github
 52M	./PurpleLlama/CybersecurityBenchmarks
 12M	./PurpleLlama/.git
 15G	./PurpleLlama/Llama-Guard2
1.2M	./PurpleLlama/CodeShield
 15G	./PurpleLlama
308G	.
```

So downloading all Meta AI models is not a good idea if you lack storage capacity. I ran the downloads in parallel and left them unattended. But when I looked at the result I saw some errors. Luckily those download scripts are resilient, so you can pick up where you left off.

But the damage was already done. Within minutes my 1TB disk was swamped by huge files. Just delete them, you would say. I thought the same:

```shell
$ rm -rf llama2

no space left on device
```

So I rebooted and wanted to log back in. Alas! The progress bar starts, but stops just as fast. I stopped breathing for a few seconds...

## ???

No sweat. Just boot in *Recovery Mode*. On a Silicon Mac with Sonoma, you press the power button and hold it until the screen says 'Loading options'

Selecting the 'startup' disk with the shift-key pressed to continue to safe mode didn't work for me, so I selected 'options'.

![Screenshot MacOS Recovery Screen](../images/Catch22/macos-recovery-mode-startup-options.jpg)

After a couple of retries, I hadn't made any progress. Lot's of articles on the web made suggestions, but to no avail. Everything I tried within the *Terminal* failed. The *Disk Utility* has an option to show *APFS Snapshots*, but deleting them also fails.

Until I stumbled on this [page](https://eduardo-pinheiro.medium.com/your-mac-doesnt-restart-due-to-no-space-left-on-device-27adf777619d).

It covered an earlier version of MacOS, but the aforementioned *Disk Utility* and *Terminal* were available. With the first one you check if the `Data` disk is unmounted. Then open up a terminal window and execute the following commands:

```shell
diskutil list
```

look for the `APFS Volume VM`. This volume is unencrypted and is used by macOS for storing encrypted swap files.

![Screenshot Terminal Window](../images/Catch22/diskutil-output.png)

then

```shell
diskutil apfs deleteVolume disk3s6
```

Deleting the *swap volume* in recovery mode doesn't do any harm and it's recreated on reboot. After deletion, there was enough free space, so the system finally allowed me to remove files. After a restart, I could login again. Phew! :-)

#### APFS explained

* https://en.wikipedia.org/wiki/Apple_File_System
* https://support.apple.com/en-gb/guide/security/seca6147599e/web