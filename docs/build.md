> python 3.10

## macos

python3 -m venv .venv

source .venv/bin/activate


pip install -r requirements.txt

python setup.py bdist_dmg




## windows


python -m venv .venv

source .venv/Scripts/activate


pip install -r requirements.txt

python setup.py bdist_msi


rm -rf build dist




python3.9

fastapi==0.103.2



https://github.com/tiangolo/fastapi/discussions/9808



https://github.com/tiangolo/fastapi/discussions/10476




python3.10 you dont worry fastapi version to cause





https://py2app.readthedocs.io/en/latest/tutorial.html#create-a-setup-py-file




## package to dmg  exe  msi


Running your application
During development, it’s often useful to have your application attached to the Terminal. This allows you to better debug it, e.g. by inserting import pdb; pdb.set_trace() into your code to inspect it interactively at runtime.

To run your application directly from the Terminal:

$ ./dist/MyApplication.app/Contents/MacOS/MyApplication
To start your application normally with LaunchServices, you can use the open tool:

$ open -a dist/MyApplication.app
If you want to specify “open document” events, to simulate dropping files on your application, just specify them as additional arguments to open.

You may of course also double-click your application from Finder.

When run normally, your application’s stdout and stderr output will go to the Console logs. To see them, open the Console application:

$ open -a Console



Building for deployment
After you’ve got your application working smoothly in alias mode, it’s time to start building a redistributable version. Since we’re switching from alias mode to normal mode, you should remove your build and dist folders as above.

Building a redistributable application consists of simply running the py2app command:

$ python setup.py py2app
This will assemble your application as dist/MyApplication.app. Since this application is self-contained, you will have to run the py2app command again any time you change any source code, data files, options, etc.

The easiest way to wrap your application up for distribution at this point is simply to right-click the application from Finder and choose “Create Archive”.



病毒检测

https://www.virustotal.com/gui/home/upload