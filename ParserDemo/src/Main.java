import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.util.Iterator;
import java.util.List;
import java.util.Set;
import java.util.HashSet;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

import edu.stanford.nlp.trees.Tree;

public class Main {

	static Parser mparser = null;
	static String delimiter = "\t\t";
	static int minThread = 10;
	static int maxThread = 20;

	public static void parseOneSet(Set<String> sents, String outFile) {

		OutputStreamWriter writer = null;
		BufferedWriter bw = null;
		try {
			OutputStream os = new FileOutputStream(new File(outFile), true);
			writer = new OutputStreamWriter(os, "UTF-8");
			bw = new BufferedWriter(writer);

			Iterator<String> it = sents.iterator();

			ThreadPoolExecutor threadPool = new ThreadPoolExecutor(minThread,
					maxThread, 60, TimeUnit.SECONDS,
					new LinkedBlockingQueue<Runnable>(10),
					new ThreadPoolExecutor.CallerRunsPolicy());

			int count = 0;

			while (it.hasNext()) {
				count++;
				String sent = it.next();
				threadPool.execute(new ParserThread(count, sent, mparser, bw));
			}

			System.out.println("end");
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
		}
	}

	public static Set<String> getRecordSents(String outFile) {
		Set<String> recordSents = new HashSet<String>();
		try {
			recordSents = new FileManager(delimiter).readFileToSets(outFile)
					.get(0);
		} catch (Exception e) {
			e.printStackTrace();
		}

		return recordSents;
	}

	public static void main(String[] args) {
		// String inPath = "/home/lsj/data/enwiki/";
		// String inPath = "/home/lsj/data/zhwiki/";
		// String inPath = "/home/lsj/data/baidu/";
		// String inPath = "/home/lsj/data/hudong/";
		String inPath = "/home/lmy/data/origin/";

		String outPath = "/home/lmy/data/parser/";
		// String inPath = "etc/";
		// String outPath = "etc/";
		// String inFile = "enwiki-instance-concept-1v1.dat";
		// String inFile = "enwiki-concept-sub-all-1v1.dat";
		// String inFile = "hudong-instance-concept-1v1.dat";
		String outFile = "";

		for (String s : args) {
			System.out.println(s);
		}

		if (args.length < 2 || args.length > 4) {
			System.err.println("Wrong number of auguments");
			System.err.println("Need 2 or 3 or 4 auguments");
			System.err.println("1. Language");
			System.err.println("2. Input file name");
			System.err.println("3. Input file path");
			System.err.println("4. Output file path");
			System.exit(1);
		}

		if (args[0].equals("en"))
			mparser = new EnglishParser();
		else if (args[0].equals("zh"))
			mparser = new ChineseParser();
		else {
			System.err.println("Wrong Language " + args[0]);
			System.exit(1);
		}

		String inFile = args[1];

		if (args.length >= 3)
			inPath = args[2];
		if (args.length == 4)
			outPath = args[3];

		System.out.println("Reading InputFile:" + inFile);
		List<Set<String>> sentSet = new FileManager(delimiter)
				.readFileToSets(inPath + inFile);
		for (int k = 0; k < 2; k++) {

			outFile = inFile.split("\\.")[0] + "-" + k + "column" + ".dat";
			System.out.println("OutputFile:" + outPath + outFile);
			Set<String> sents = sentSet.get(k);// get sentence
			System.out.println("All sentences: " + sents.size());
			Set<String> recordSents = getRecordSents(outPath + outFile);
			System.out.println("Record sentences: " + recordSents.size());
			for (String s : recordSents)
				sents.remove(s);
			System.out.println("Left sentences: " + sents.size());
			parseOneSet(sents, outPath + outFile);
		}

	}

	static class ParserThread extends Thread {
		private int count;
		private String sent;
		private Parser mparser;
		private BufferedWriter bw;

		public ParserThread(int count, String sent, Parser mparser,
				BufferedWriter bw) {

			this.count = count;
			this.sent = sent;
			this.mparser = mparser;
			this.bw = bw;
		}

		@Override
		public void run() {
			String s = null;
			s = sent;
			if (sent.contains("(") && sent.contains(")") && sent.endsWith(")")) {
				s = sent.substring(sent.indexOf("(") + 1, sent.indexOf(")"));
				if (s.length() == 0)
					s = sent;
				//s = s.replace('(', ' ').replace(')', ' ');
			}

			if (s.contains("》") || s.contains("《") || s.contains("【")
					|| s.contains("】") || s.contains("：")) {
				s = s.replace('》', ' ').replace('《', ' ').replace('【', ' ')
						.replace('】', ' ').replace('：', ' ');
			}
			// System.out.println("Sentence-->" + s);
			String tw = "[]";
			String td = "[]";
			try {
				Tree parser = mparser.getParserTree(s);
				tw = mparser.getTaggedWord(parser).toString();
				td = mparser.getTypedDependency(parser).toString();
			} catch (Exception e) {
				System.out.println("Special Sentence:" + s);
				System.out.println(s + delimiter + tw + delimiter + td);
			}

			if (count % 1000 == 0)
				System.out.println(">>>" + count);

			synchronized (bw) {
				try {
					bw.write(sent + delimiter + tw + delimiter + td + "\n");
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
