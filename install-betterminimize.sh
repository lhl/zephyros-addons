#!/bin/bash

# http://stackoverflow.com/questions/8620605/applescript-to-minimize-all-visible-windows-is-very-slow-how-to-speed-it-up
# http://stackoverflow.com/questions/14551419/listing-all-windows-of-all-applications

# Faster Animations
defaults write com.apple.dock mineffect -string scale
defaults write NSGlobalDomain NSWindowResizeTime .001 

# Restart
killall Finder
