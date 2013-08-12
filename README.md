# Sublime Text 2 plugin - Cypher

A plugin for working with [Neo4j](http://www.neo4j.org)'s [Cypher](http://docs.neo4j.org/chunked/milestone/cypher-query-lang.html) query language in [SublimeText](http://www.sublimetext.com).


# Installation

* If you don't have it already install [Sublime Package Control](http://wbond.net/sublime_packages/package_control)
* See [Package Control usage](http://wbond.net/sublime_packages/package_control/usage)
* Open the Command Pallete (cmd+shift+p)
* Select "Install Package"
* Select "Cyper"

The plugin will detect files ending in `.cql` or `.cyp` as Cypher, optionally just select Cypher from the Syntax menu. 


# Usage

* Type a Cypher query into your editor
* Run it by selecting the query and hitting (cmd+shift+r on OSX, ctrl+shift+r on Windows)
* The results or error will be shown in the console, which can be opened by (ctrl+`)
* If no text is selected, all the text in the file is run as a single query


# Future Plans

* Auto selecting the query under the cursor
* Auto completion for Cypher keywords and functions, etc
* Auto completion based on data in the DB
* Cypher 2 support

