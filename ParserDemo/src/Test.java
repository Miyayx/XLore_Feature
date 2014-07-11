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

		String filename = "wiki-article-category-1v1.dat";
		FileManager fm = new FileManager();
		List<Set<String>> sents = fm.readFileToSets(filename);
		// List<Set> sents = new FileManager().readFileToOneSet(filename);
		//fm.writeSetToFile(sents.get(0), "article.dat");
	//	fm.writeSetToFile(sents.get(1), "category.dat");

		Set<String> sents1 = sents.get(0);

		EnglishParser mparser = new EnglishParser();

		File file = new File("article-taggedword-typeddependency7.dat");
		OutputStreamWriter writer = null;
		BufferedWriter bw = null;
		try {
			OutputStream os = new FileOutputStream(file);
			writer = new OutputStreamWriter(os, "UTF-8");
			bw = new BufferedWriter(writer);

			Iterator<String> it = sents1.iterator();
			int supclassLen = sents1.size();
			System.out.println("superclass's length: " + supclassLen);
			int count = 0;
			Set<String> tags = new LinkedHashSet<String>();
			Set<String> dependencies = new LinkedHashSet<String>();
			Boolean handled = true;
			while (it.hasNext() && (!it.next().equals("ⱺ"))) ;

			while (it.hasNext()) {
				// long start = System.currentTimeMillis();
				String sent = it.next();
System.out.println(sent);
				count++;
				bw.write(sent + "\t\t");
				Tree parser = mparser.getParserTree(sent);
				// List<TaggedWord> taggedwords = mparser.getTaggedWord(parser);
				// for (int i = 0; i < taggedwords.size(); i++)
				// tags.add(taggedwords.get(i).tag());
				//
				// List<TypedDependency> typedDependencies = mparser
				// .getTypedDependency(parser);
				// for (int i = 0; i < typedDependencies.size(); i++)
				// dependencies.add(typedDependencies.get(i).reln()
				// .getShortName());

				bw.write(mparser.getTaggedWord(parser).toString() + "\t\t");
				bw.write(mparser.getTypedDependency(parser).toString() + "\n");
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

				bw.flush();
			}
			System.out.println("finish the first column");

		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				bw.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}

//		Set<String> sents2 = sents.get(1);
//
//		File file2 = new File("category-taggedword-typeddependency.dat");
//		OutputStreamWriter writer2 = null;
//		BufferedWriter bw2 = null;
//		try {
//			OutputStream os = new FileOutputStream(file2);
//			writer2 = new OutputStreamWriter(os, "UTF-8");
//			bw2 = new BufferedWriter(writer2);
//
//			Iterator<String> it = sents2.iterator();
//			int supclassLen = sents2.size();
//			System.out.println("superclass's length: " + supclassLen);
//			Set<String> tags = new LinkedHashSet<String>();
//			Set<String> dependencies = new LinkedHashSet<String>();
//			while (it.hasNext()) {
//
//				String sent = it.next();
//				bw2.write(sent + "\t\t");
//				Tree parser = mparser.getParserTree(sent);
//
//				bw2.write(mparser.getTaggedWord(parser).toString() + "\t\t");
//				bw2.write(mparser.getTypedDependency(parser).toString() + "\n");
//
//				bw2.flush();
//			}
//			System.out.println("finish the second column");
//			System.out.println("end");
//		} catch (FileNotFoundException e) {
//			e.printStackTrace();
//		} catch (IOException e) {
//			e.printStackTrace();
//		} finally {
//			try {
//				bw2.close();
//			} catch (IOException e) {
//				e.printStackTrace();
//			}
//		}

	}
}
