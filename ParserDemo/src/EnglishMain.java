import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.HashSet;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

import edu.stanford.nlp.trees.Tree;

public class EnglishMain {

	static String delimiter = "\t\t";
	static int minThread = 10;
	static int maxThread = 20;

	public static void parseOneSet(Set<String> sents, String outFile) {

		Set<String> recordSents = new HashSet<String>();
		try {
			recordSents = new FileManager(delimiter).readFileToSets(outFile)
					.get(0);
			for (String s : recordSents)
				System.out.println(s);

			System.out.println(recordSents.size());
		} catch (Exception e) {
		}

		EnglishParser mparser = new EnglishParser();

		OutputStreamWriter writer = null;
		BufferedWriter bw = null;
		try {
			OutputStream os = new FileOutputStream(new File(outFile), true);
			writer = new OutputStreamWriter(os, "UTF-8");
			bw = new BufferedWriter(writer);

			// Iterator<String> it = sents1.iterator();
			// int classLen = sents1.size();
			Iterator<String> it = sents.iterator();
			int classLen = sents.size();
			System.out.println("length: " + classLen);

			ThreadPoolExecutor threadPool = new ThreadPoolExecutor(minThread,
					maxThread, 60, TimeUnit.SECONDS,
					new LinkedBlockingQueue<Runnable>(10),
					new ThreadPoolExecutor.CallerRunsPolicy());

			int count = 0;

			while (it.hasNext()) {
				count++;

				// long start = System.currentTimeMillis();

				String sent = it.next();
				if (recordSents.contains(sent))
					continue;

				// bw.write(sent + "\t\t");

				// Tree parser = mparser.getParserTree(sent);

				// bw.write(mparser.getTaggedWord(parser).toString() +
				// "\t\t");
				// bw.write(mparser.getTypedDependency(parser).toString() +
				// "\n");
				// System.out.println(parser.getTaggedWord(sent));

				// System.out.println(mparser.getTaggedWord(parser).toString()
				// + "\t\t");
				// System.out.println(mparser.getTypedDependency(parser)
				// .toString() + "\n");

				// System.out.println(count);
				// System.out.println("tags: " + tags.size());
				// System.out.println(tags.toString());
				// System.out.println("typedDependencies: " +
				// dependencies.size());
				// System.out.println(dependencies.toString());

				// long end = System.currentTimeMillis();
				// System.out.println("time---------" + (start - end));

				// bw.flush();
				System.out.println();
				threadPool.execute(new ParserThread(count, sent, mparser, bw));

				// tags = new HashMap<String, String>();
				// dependencies = new HashMap<String, String>();
				// threadList = new ArrayList<Thread>();
				// sentList = new LinkedHashSet<String>();

			}

			System.out.println("end");
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {

		}
	}

	public static void main(String[] args) {
		String inPath = "/home/lsj/data/enwiki/";
		String outPath = "/home/lmy/data/parser/";
		// String inPath = "etc/";
		// String outPath = "etc/";
		String inFile = "enwiki-instance-concept-1v1.dat";
		String outFile = "";

		System.out.println("Reading InputFile:" + inFile);
		List<Set<String>> sentSet = new FileManager(delimiter)
				.readFileToSets(inPath + inFile);
		for (int k = 0; k < sentSet.size(); k++) {

			outFile = inFile.split("\\.")[0] + "-" + k + "column" + ".dat";
			System.out.println("OutputFile:" + outFile);
			Set<String> sents = sentSet.get(k);// get sentence
			parseOneSet(sents, outPath + outFile);
		}

	}

	static class ParserThread extends Thread {
		private int count;
		private String sent;
		private EnglishParser mparser;
		private BufferedWriter bw;

		public ParserThread(int count, String sent, EnglishParser mparser,
				BufferedWriter bw) {

			this.count = count;
			this.sent = sent;
			this.mparser = mparser;
			this.bw = bw;
		}

		@Override
		public void run() {
			String s = null;
			if (sent.contains("(") && sent.contains(")") && sent.endsWith(")")) {
				s = sent.substring(sent.indexOf("(") + 1, sent.indexOf(")"));
				if (s.length() == 0)
					s = sent;
			} else
				s = sent;

			if (s.contains("》") || s.contains("《") || s.contains("【")
					|| s.contains("】") || s.contains("：")) {
				s = s.replace('》', ' ').replace('《', ' ').replace('【', ' ')
						.replace('】', ' ').replace('：', ' ');
			}
			//System.out.println("Sentence-->" + s);
			Tree parser = mparser.getParserTree(s);
			String tw = mparser.getTaggedWord(parser).toString();
			String td = mparser.getTypedDependency(parser).toString();

			if (count % 1000 == 0)
				System.out.println(">>>" + count);

			synchronized (bw) {
				try {
					bw.write(s + delimiter + tw + delimiter + td + "\n");
					bw.flush();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}

			}
		}

		public String getSent() {
			return this.sent;
		}

		public int getCount() {
			return this.count;
		}

	}
}
