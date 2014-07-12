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

	static Parser mparser = null;
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

		OutputStreamWriter writer = null;
		BufferedWriter bw = null;
		try {
			OutputStream os = new FileOutputStream(new File(outFile), true);
			writer = new OutputStreamWriter(os, "UTF-8");
			bw = new BufferedWriter(writer);

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

				String sent = it.next();
				if (recordSents.contains(sent))
					continue;
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

	public static void main(String[] args) {
		String inPath = "/home/lsj/data/enwiki/";
		//String inPath = "/home/lsj/data/zhwiki/";
		//String inPath = "/home/lsj/data/baidu/";
		//String inPath = "/home/lsj/data/hudong/";

		String outPath = "/home/lmy/data/parser/";
		//String inPath = "etc/";
		//String outPath = "etc/";
		//String inFile = "enwiki-instance-concept-1v1.dat";
		String inFile = "enwiki-concept-sub-1v1.dat";
		String outFile = "";

		mparser = new EnglishParser();

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
