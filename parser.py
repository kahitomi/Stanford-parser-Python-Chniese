# Changed based on http://projects.csail.mit.edu/spatial/Stanford_Parser. Made by Wei Jia https://github.com/kahitomi/Stanford-parser-Python-Chniese

import jpype

class ParserError(Exception):
    def __init__(self, *args, **margs):
        Exception.__init__(self, *args,**margs)

stanford_parser_classpath = None

def startJvm():
    import os
    os.environ.setdefault("STANFORD_PARSER_CLASSPATH", "/usr/stanford-parser/stanford-parser.jar:/usr/stanford-parser/stanford-parser-3.5.2-models.jar")
    global stanford_parser_classpath
    stanford_parser_home = os.environ["STANFORD_PARSER_HOME"]
    stanford_parser_classpath = os.environ["STANFORD_PARSER_CLASSPATH"]
    JVMPath_8 = os.environ["JAVA8_JVM"]
    jpype.startJVM(JVMPath_8,
                   "-ea"
                   ,("-Djava.class.path=%s" % stanford_parser_classpath))
startJvm() # one jvm per python instance.

class Parser:

    def __init__(self, pcfg_model_fname=None):
        if pcfg_model_fname == None:
            self.pcfg_model_fname = "edu/stanford/nlp/models/lexparser/chinesePCFG.ser.gz"
        else:
            self.pcfg_model_fname = pcfg_model_fname


        self.package_lexparser = jpype.JPackage("edu.stanford.nlp.parser.lexparser")
        LexicalizedParser = jpype.JClass("edu.stanford.nlp.parser.lexparser.LexicalizedParser")
        self.parser = LexicalizedParser.loadModel(self.pcfg_model_fname, ["-maxLength", "80"])

        self.package = jpype.JPackage("edu.stanford.nlp")

        tokenizerFactoryClass = self.package.process.__getattribute__("PTBTokenizer$PTBTokenizerFactory")
        self.tokenizerFactory = tokenizerFactoryClass.newPTBTokenizerFactory(True, True)

        self.tlp = self.parser.getOp().langpack(); 
        self.gsf = self.tlp.grammaticalStructureFactory()




    def printInfo(self):

        Numberer = self.package.util.Numberer
        print ("Grammar\t" +
               `Numberer.getGlobalNumberer("states").total()` + '\t' +
               `Numberer.getGlobalNumberer("tags").total()` + '\t' +
               `Numberer.getGlobalNumberer("words").total()` + '\t' +
               `self.parser.pparser.ug.numRules()` + '\t' +
               `self.parser.pparser.bg.numRules()` + '\t' +
               `self.parser.pparser.lex.numRules()`)

        print "ParserPack is ", self.parser.op.tlpParams.getClass()
        print "Lexicon is ", self.parser.pd.lex.getClass()        
        print "Tags are: ", Numberer.getGlobalNumberer("tags")
        self.parser.op.display()
        print "Test parameters"
        self.parser.op.tlpParams.display()
        self.package_lexparser.Test.display()
    
    def parseToStanfordDependencies(self, sentence):
        tree = self.parser.parse(sentence)
        dep = self.gsf.newGrammaticalStructure(tree);  
        
        returnList = []
        for dependency in dep.typedDependenciesCCprocessed():
            print dependency.toString()
        
        return (tree, dep)
                              
