#!/usr/bin/env python

from pprint import pprint
import os
import urllib
import sys
import zipfile
import tempfile

ANDROID_SDK_PATH = '/Users/max/work/android-sdk-mac'

BASE_DEPENDENCIES ={
'android-support-v13': {'url': os.path.join(ANDROID_SDK_PATH, 'extras/android/m2repository/com/android/support/support-v13/21.0.3/support-v13-21.0.3.aar')},
'android-support-v4': {'url': os.path.join(ANDROID_SDK_PATH, 'extras/android/m2repository/com/android/support/support-v4/21.0.3/support-v4-21.0.3.aar')},
'annotations': {'url': 'https://repo1.maven.org/maven2/com/google/code/findbugs/annotations/2.0.0/annotations-2.0.0.jar'},
'support-annotations': {'url': os.path.join(ANDROID_SDK_PATH, 'extras/android/m2repository/com/android/support/support-annotations/21.0.3/support-annotations-21.0.3.jar')},
'appcompat-v7': {'url': os.path.join(ANDROID_SDK_PATH, 'extras/android/m2repository/com/android/support/appcompat-v7/21.0.3/appcompat-v7-21.0.3.aar')},
'androidasync': {'url': 'https://repo1.maven.org/maven2/com/koushikdutta/async/androidasync/1.4.1/androidasync-1.4.1.jar'},
'androidpinning': {'url': 'https://repo1.maven.org/maven2/org/thoughtcrime/ssl/pinning/AndroidPinning/1.0.0/AndroidPinning-1.0.0.aar'},
'cardview-v7': {'url': os.path.join(ANDROID_SDK_PATH, 'extras/android/m2repository/com/android/support/cardview-v7/21.0.3/cardview-v7-21.0.3.aar')},
'commons-lang': {'url': 'https://repo1.maven.org/maven2/commons-lang/commons-lang/2.6/commons-lang-2.6.jar'},
'crashlytics': {'url': 'https://maven.fabric.io/repo/com/crashlytics/sdk/android/crashlytics/2.2.3/crashlytics-2.2.3.aar'},
'drag-sort-listview': {'url': 'http://wordpress-mobile.github.io/WordPress-Android/org/wordpress/drag-sort-listview/0.6.1/drag-sort-listview-0.6.1.aar'},
'emailchecker': {'url': 'http://wordpress-mobile.github.io/WordPress-Android/org/wordpress/emailchecker/0.3/emailchecker-0.3.aar'},
'eventbus': {'url': 'https://repo1.maven.org/maven2/de/greenrobot/eventbus/2.4.0/eventbus-2.4.0.jar'},
'fabric': {'url': 'https://maven.fabric.io/repo/io/fabric/sdk/android/fabric/1.2.0/fabric-1.2.0.aar'},
'gcm': {'url': 'http://wordpress-mobile.github.io/WordPress-Android/org/wordpress/gcm/1.0.0/gcm-1.0.0.jar'},
'gson': {'url': 'https://repo1.maven.org/maven2/com/google/code/gson/gson/2.2.2/gson-2.2.2.jar'},
'helpshift': {'url': 'https://repo1.maven.org/maven2/com/helpshift/android-aar/3.7.2/android-aar-3.7.2.aar'},
'mediapicker': {'url': 'https://repo1.maven.org/maven2/org/wordpress/mediapicker/1.2.1/mediapicker-1.2.1.aar'},
'mixpanel': {'url': 'https://repo1.maven.org/maven2/com/mixpanel/android/mixpanel-android/4.3.0/mixpanel-android-4.3.0.aar'},
'passcodelock': {'url': 'http://wordpress-mobile.github.io/WordPress-Android/org/wordpress/android-passcodelock/0.0.6/android-passcodelock-0.0.6.aar'},
'photoview': {'url': 'https://repo1.maven.org/maven2/com/github/chrisbanes/photoview/library/1.2.3/library-1.2.3.aar'},
'recyclerview-v7': {'url': os.path.join(ANDROID_SDK_PATH, 'extras/android/m2repository/com/android/support/recyclerview-v7/21.0.3/recyclerview-v7-21.0.3.aar')},
'simperium': {'url': 'https://repo1.maven.org/maven2/com/simperium/android/simperium/0.6.2/simperium-0.6.2.aar'},
'slidinguppanel': {'url': 'http://wordpress-mobile.github.io/WordPress-Android/org/wordpress/slidinguppanel/1.0.0/slidinguppanel-1.0.0.aar'},
'tagsoup': {'url': 'https://repo1.maven.org/maven2/org/ccil/cowan/tagsoup/tagsoup/1.2.1/tagsoup-1.2.1.jar'},
'tracks': {'url': 'https://repo1.maven.org/maven2/com/automattic/tracks/1.0.0/tracks-1.0.0.aar'},
'undobar': {'url': 'https://repo1.maven.org/maven2/com/cocosw/undobar/1.6/undobar-1.6.aar'},
'volley': {'url': 'https://repo1.maven.org/maven2/com/mcxiaoke/volley/library/1.0.15/library-1.0.15.jar'}
}

TEST_DEPENDENCIES = {

}

def download(name, url, outdir):
    dummy, extension = os.path.splitext(url)
    out = os.path.join(outdir, name) + extension
    print("Downloading %s from %s to %s" % (name, url, out))
    urllib.urlretrieve(url, out)
    return out

def copy(name, url, outdir):
    pass

def fetch_dependency(name, dep, outdir):
    out = download(name, dep['url'], outdir)
    if 'extract-jar' in dep and dep['extract-jar']:
        extract_jar(out)

def extract_jar(filename):
    tmpdir = tempfile.mkdtemp()
    zf = zipfile.ZipFile(filename)
    extracted_jars = []
    for name in zf.namelist():
        if name.endswith('.jar'):
            zf.extract(name, tmpdir)
            extracted_jars.append(os.path.join(tmpdir, name))
    for extracted in extracted_jars:
        basename, extension = os.path.splitext(os.path.basename(extracted))
        out = os.path.join(os.path.dirname(filename),
                basename + '-' + os.path.basename(filename).replace('.aar', '.jar'))
        os.rename(extracted, out)
    os.remove(filename)

def fetch_dependencies(outdir):
    for name in BASE_DEPENDENCIES:
        fetch_dependency(name, BASE_DEPENDENCIES[name], outdir)

def main(outdir):
    try:
        os.mkdir(outdir)
    except OSError:
        pass
    fetch_dependencies(outdir)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: %s OUTDIR" % (sys.argv[0], ))
        print("Example: %s extlibs" % (sys.argv[0], ))
        sys.exit(1)
    main(sys.argv[1])
