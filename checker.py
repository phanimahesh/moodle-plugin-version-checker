#! /usr/bin/env python3

# imports
import urllib.request
from bs4 import BeautifulSoup as soup
from pprint import pprint


with open('./plugins.txt') as f:
    plugins = f.read().split()

def get_versions_for_plugin(plugin):
    print("Checking plugin: {}".format(plugin))
    plugin_page = soup(urllib.request.urlopen("https://moodle.org/plugins/pluginversions.php?plugin={}".format(plugin)).read(), "html.parser")
    versionstrings = [v.string.replace('Moodle ','') for v in plugin_page.select(".versions-list.current .moodleversions")]
    versions = list(set([float(v) for versionstring in versionstrings for v in versionstring.split(', ')]))
    versions.sort()
    print("{}:{}".format(plugin,versions))
    return versions
    
pluginsWithVersions = { plugin: get_versions_for_plugin(plugin) for plugin in plugins}

versionsWithplugins = {}
for plugin,versions in pluginsWithVersions.items():
    for version in versions:
        versionsWithplugins.setdefault(version,[]).append(plugin)

print("\n\n\nSupported versions by plugin:")
pprint(pluginsWithVersions)

print("\n\n\nSupported plugins by version type:")
pprint(versionsWithplugins)

print("\n\n\nUnsupported plugins by version type:")
unsupported = lambda ps: [p for p in plugins if p not in ps]
pprint({v:unsupported(ps) for v,ps in versionsWithplugins.items()})
