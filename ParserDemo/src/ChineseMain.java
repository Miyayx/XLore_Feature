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
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.HashSet;
import java.util.concurrent.locks.ReentrantLock;

import edu.stanford.nlp.trees.Tree;

public class ChineseMain{

	public static void main(String[] args) {
    String delimiter = "\t\t";
    String path = "/home/lmy/data/parser/";
		String filename = "/home/zigo/SemantifyWiki/etc/dataset/ha-id-title.dat";
		String recordfile = path+"ha-title-taggedword-typeddependency.dat";

		List<Set<String>> sents = new FileManager(delimiter).readFileToSets(filename);
		//Set<String> sents1 = sents.get(0);// get category(superclass)
		Set<String> sents2 = sents.get(1);// get sub
		Set<String> recordSents = new HashSet<String>();
		try{
			recordSents = new FileManager().readFileToSets(recordfile).get(0);
      //for(String s:recordSents){
       //  System.out.println(s);
     // }
    System.out.println(recordSents.size());
		}catch(Exception e){
		}

		ChineseParser mparser = new ChineseParser();

		File file = new File(recordfile);
		OutputStreamWriter writer = null;
		BufferedWriter bw = null;
		try {
			OutputStream os = new FileOutputStream(file,true);
			writer = new OutputStreamWriter(os, "UTF-8");
			bw = new BufferedWriter(writer);

			//Iterator<String> it = sents1.iterator();
			//int classLen = sents1.size();
			Iterator<String> it = sents2.iterator();
			int classLen = sents2.size();
			int progressSlice = classLen / 100;
			System.out.println("length: " + classLen);
			int count = 0;
			Map<String,String> tags = new HashMap<String, String>();
			Map<String,String> dependencies = new HashMap<String, String>();
			List<ParserThread> threadList = new ArrayList<ParserThread>();
			Set<String> sentList = new LinkedHashSet<String>();
			while (it.hasNext()) {
				count++;

				// long start = System.currentTimeMillis();

				String sent = it.next();
				if(recordSents.contains(sent))
					continue;

				//bw.write(sent + "\t\t");

				//Tree parser = mparser.getParserTree(sent);

				//				bw.write(mparser.getTaggedWord(parser).toString() + "\t\t");
				//				bw.write(mparser.getTypedDependency(parser).toString() + "\n");
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

				//bw.flush();

				threadList.add(new ParserThread(count,tags, dependencies, sent, mparser));

				//				tags = new HashMap<String, String>();
				//				dependencies = new HashMap<String, String>();
				//				threadList = new ArrayList<Thread>();
				//				sentList = new LinkedHashSet<String>();

			}

			int threadLen = threadList.size();
			int increment = 5000;
			System.out.println("Thread Len-->"+threadLen);
			for(int i = 0;i <threadLen;i+=increment){
				System.out.println("Start --> "+i*100/(float)threadLen+"%");
				for (ParserThread t:threadList.subList(i,Math.min(i+increment,threadLen))){
					//for (ParserThread t:threadList){
					t.start();
				}

				System.out.println("Join ID-->"+i*100/(float)threadLen+"%");
				for (ParserThread t:threadList.subList(i,Math.min(i+increment,threadLen))){
					//for (ParserThread t:threadList){
					try {
						t.join();
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
				}
				for (ParserThread t:threadList.subList(i,Math.min(i+increment,threadLen))){
					//		for (ParserThread t:threadList){
					String s = t.getSent();
					try{
						bw.write(s+delimiter+tags.get(s).toString()+delimiter+dependencies.get(s).toString()+"\n");
						bw.flush();
					}catch(Exception e){
						System.out.println("Error String: "+s);
            System.out.println("Line num:"+t.getCount());
					}
				}
				}
				System.out.println("end");
				} catch (FileNotFoundException e) {
					e.printStackTrace();
				} catch (IOException e) {
					e.printStackTrace();
				} finally {

				}

				}

				static class ParserThread extends Thread {
					private int count;
					private Map<String, String> tags;
					private Map<String, String> dependencies;
					private String sent;
					private ChineseParser mparser;

					public ParserThread(int count,Map<String, String> tags,
							Map<String, String> dependencies, String sent,
							ChineseParser mparser) {
						this.count = count;
						this.tags = tags;
						this.dependencies = dependencies;
						this.sent = sent;
						this.mparser = mparser;
					}

					@Override
						public void run() {
							String s = null;
							if (sent.contains("(") && sent.contains(")") && sent.endsWith(")")){
								s = sent.substring(sent.indexOf("(")+1, sent.indexOf(")"));
                if (s.length() == 0)
                    s = sent;
}
							else s = sent;

              if(s.contains("》") || s.contains("《") || s.contains("【") || s.contains("】") || s.contains("：")){
              s = s.replace('》',' ').replace('《',' ').replace('【',' ').replace('】',' ').replace('：',' ');
}
							Tree parser = mparser.getParserTree(s);
							tags.put(sent, mparser.getTaggedWord(parser).toString());
							dependencies.put(sent, mparser.getTypedDependency(parser)
									.toString());

							if (count % 1000 == 0)
								System.out.println(">>>" + count );

						}
					public String getSent(){
						return this.sent;
					}
					public int getCount(){
						return this.count;
					}

				}
			}
