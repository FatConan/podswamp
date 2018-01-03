#Podswamp

##Project
**Podswamp**: extracts guest information and builds a site from a provided public Libsyn RSS and configuration JSON file. The minimum requirement for a configuration file is the URL of a Libsyn RSS feed.  This information should be placed in a file named ```project.json```

```json
{
    "rss": "<libsyn rss url>"
} 
```

This will generate a site using the default templates and styles without any guest-based pages.  In order to parse guest information from the podcast titles additional information will need to be provided including regular expressions and terms to exclude. 
 
##Installation
Installation of podswamp requires Python 3 and setuputils.  

A copy of podswamp should be downloaded and unpacked, or cloned. From within the unpacked/cloned podswamp run:
```
python3 setup.py install
```
to install.

Once installed podswamp can be run using:
```
podswamp <target podswamp project folder>
```

##Usage
The basic usage of **Podswamp** involves creating a project folder and a ```project.json``` configuration file within it. 

From within the project folder run 
```
podswamp .
```
To process the configuration and builds the HTML of the site in a folder called, fittingly enough, html.

##Examples
Examples of Podswamp's configuration can be found for:
* [Stop Podcasting Yourself](https://bitbucket.org/fatconan/spy-db)
* [Dead Author's Podcast](https://bitbucket.org/fatconan/deadauthors-db)

Examples of the output of Podswamp can be found at:
* [Stop Podcasting Yourself](http://spydb.themonstrouscavalca.de/) 
 

