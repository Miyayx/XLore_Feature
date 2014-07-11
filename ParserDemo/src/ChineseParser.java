import java.io.StringReader;
import java.util.Collection;
import java.util.List;

import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.objectbank.TokenizerFactory;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;
import edu.stanford.nlp.process.CoreLabelTokenFactory;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.process.PTBTokenizer;
import edu.stanford.nlp.trees.GrammaticalStructure;
import edu.stanford.nlp.trees.GrammaticalStructureFactory;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreePrint;
import edu.stanford.nlp.trees.TreebankLanguagePack;
import edu.stanford.nlp.trees.TypedDependency;
import edu.stanford.nlp.trees.international.pennchinese.ChineseGrammaticalStructure;
import edu.stanford.nlp.trees.international.pennchinese.ChineseGrammaticalStructureFactory;
import edu.stanford.nlp.trees.international.pennchinese.ChineseTreebankLanguagePack;


public class ChineseParser {
	private LexicalizedParser lp;
	private TreebankLanguagePack tlp;
	private GrammaticalStructureFactory gsf;

	public ChineseParser() {
		lp = LexicalizedParser
		// .loadModel("edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz");
				.loadModel("edu/stanford/nlp/models/lexparser/xinhuaFactoredSegmenting.ser.gz");
		tlp = new ChineseTreebankLanguagePack();
		gsf = tlp.grammaticalStructureFactory();
	}

	public Tree getParserTree(String sent) {
		Tree parse = lp.apply(sent);

		return parse;
	}

	public void analyzeFile(String filename) {

		for (List<HasWord> sentence : new DocumentPreprocessor(filename)) {
			Tree parse = lp.apply(sentence);
			System.out.println(parse.taggedYield());
			System.out.println();

			ChineseGrammaticalStructure gs = (ChineseGrammaticalStructure) gsf.newGrammaticalStructure(parse);
			List<TypedDependency> tdl = gs.typedDependenciesCCprocessed(true);
			System.out.println(tdl);
			System.out.println();

			TreePrint tp = new TreePrint("penn,typedDependenciesCollapsed");
			tp.printTree(parse);
		}

	}

	public void analyzeOneSentence(String sent) {

		System.out.println("\nSentence: " + sent);
		System.out.println();
		TokenizerFactory<CoreLabel> tokenizerFactory = PTBTokenizer.factory(
				new CoreLabelTokenFactory(), "");
		List<CoreLabel> rawWords = tokenizerFactory.getTokenizer(
				new StringReader(sent)).tokenize();
		Tree parse = lp.apply(rawWords);

		System.out.println(parse.taggedYield());
		System.out.println();

		GrammaticalStructure gs = gsf.newGrammaticalStructure(parse);
		List<TypedDependency> tdl = gs.typedDependenciesCCprocessed();
		System.out.println(tdl);
		System.out.println();

		TreePrint tp = new TreePrint("penn,typedDependenciesCollapsed");
		tp.printTree(parse);
	}

	public List<TaggedWord> getTaggedWord(Tree parse) {

		return parse.taggedYield();
	}

	public Collection getTypedDependency(Tree parse) {

		GrammaticalStructure gs = gsf.newGrammaticalStructure(parse);
		Collection tdl = gs.typedDependenciesCollapsed();

		return tdl;
	}
}
