###########################################################################
#  Automatic build script for libopenh264
#
# Johan Lantz, June 2015
###########################################################################
import os
import subprocess
import argparse
import shutil

###########################################################################
#  Helper functions													      #
###########################################################################
def checkGit():
	try:
	    res = subprocess.Popen(['git', '--version'],
	                           stderr=subprocess.STDOUT,
	                           stdout=subprocess.PIPE).communicate()[0]
	    print res
	except:
	    print ("git not found. Please install git in order to be able to checkout the openh264 project ")
	    quit()

def checkoutLibOpenH264():
	if os.path.exists("openh264"):
		shutil.rmtree("openh264")
	print("Cloning libopenh264")
	os.system("git clone https://github.com/cisco/openh264.git")

###########################################################################################
#  Build functions 																		  #
#  Completely fresh builds for each arch to avoid cleaning issues. 						  #
###########################################################################################
def buildForiOS():
	#If you get build errors for the i386 versions, update nasm to 2.11.06. Check version with nasm -v
	archList = ["armv7", "armv7s", "arm64", "i386", "x86_64"]
   	if os.path.exists("libs"):
		shutil.rmtree("libs")

	os.makedirs("libs")
	os.makedirs("libs/xcrun")
	
	for arch in archList:
		print("Starting " + arch + " build.")
		targetDir = ""

		checkoutLibOpenH264()

		print("Entering openh26h folder.")
		os.chdir("openh264")
		commandLine = "make OS=ios ARCH=" + arch
		os.system(commandLine)

		print("Build for " + arch + " completed. Stepping out to working dir.")
		os.chdir("..")

		os.makedirs("libs/" + arch)
		shutil.copy("openh264/libopenh264.a", "libs/" + arch)
		
		print("Copied " + arch + " libraries to " + "libs/" + arch)

	print("All combinations built. Create fat binaries.")
	xcrunCommandLine = "xcrun -sdk iphoneos lipo"
	for arch in archList:
		xcrunCommandLine += " libs/" + arch + "/libopenh264.a"

	xcrunCommandLine += " -create -output libs/xcrun/libopenh264.a"
	os.system(xcrunCommandLine)

	print("All done. The final binary can be found in libs/xcrun/")
	
        

###########################################################################
#  Main script 														      #
###########################################################################
checkGit()

parser = argparse.ArgumentParser()

parser.add_argument("-platform",
                    help="The OS to build for",
                    choices=['Win32', 'iOS', 'android', 'WP8', 'unix'],
                    required=True)
args = parser.parse_args()

if args.platform == "iOS":
	buildForiOS()
else:
	print("Unsupported platform " + args.platform)
