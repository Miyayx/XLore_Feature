import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.util.Iterator;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TypedDependency;

public class Test {

	public static void main(String[] args) {

		Parser mparser = new EnglishParser();

		String sent = "Titanic (1943 film)";
		System.out.println(sent);
		Tree parser = mparser.getParserTree(sent);

		System.out.println(mparser.getTaggedWord(parser).toString() + "\t\t");
		System.out
				.println(mparser.getTypedDependency(parser).toString() + "\n");
		// System.out.println((count+1)+": "+sent+"\t");
		// System.out.println(parser.getTaggedWord(sent));

		// System.out.println(count);
		// System.out.println("tags: " + tags.size());
		// System.out.println(tags.toString());
		// System.out.println("typedDependencies: " +
		// dependencies.size());
		// System.out.println(dependencies.toString());
		// if (count > 10000)
		// break;

		// long end = System.currentTimeMillis();
		// System.out.println("time---------" + (start - end));

	}
}
