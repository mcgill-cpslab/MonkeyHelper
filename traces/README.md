This folder contains several example traces that could be used to test the toolchain. We collect traces from a Samsung Galaxy S phone with 4.1.2 Android, an Asus Transformer TF201 with the same Android and the Android emulator. All traces are collected with `getevent -lt /dev/input/event1` (`getevent` is the standard Android Linux-layer tool to capture user inputs); `/dev/input/event1` is the multi-touch screen descriptor file. You can get it by typing `getvent -lp` and find the touchscreen one.

For the descriptions and demos of these traces, check out the wiki page.
