Stanford parser Python Chniese Interface
====================

This is a Python Interface for [Stanford Parser](http://nlp.stanford.edu/software/lex-parser.shtml)

Changed based on http://projects.csail.mit.edu/spatial/Stanford_Parser. 

How to use
=====

Two environment values should be setted. For example:

	#Java classpath of Stanford Parser
	export STANFORD_PARSER_CLASSPATH = "/usr/stanford-parser/stanford-parser.jar:/usr/stanford-parser/stanford-parser-3.5.2-models.jar"

	# Java 8 JVM path
	export JAVA8_JVM = "/Library/Java/JavaVirtualMachines/jdk1.8.0_05.jdk/Contents/Home/jre/lib/server/libjvm.dylib"

Then use as blow

	from parser import Parser

	# No input value is fine. The default input value is this one
	my_parser = Parser("edu/stanford/nlp/models/lexparser/chinesePCFG.ser.gz")

	# tree and dep are refered from java class. Check the type with type(tree)
	# http://nlp.stanford.edu/nlp/javadoc/javanlp/edu/stanford/nlp/trees/package-tree.html
	(tree, dep) = my_parser.parseToStanfordDependencies(u"过于 追求 完美 太 过于 关注 自己")