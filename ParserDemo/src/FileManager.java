import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public class FileManager {

	String delimiter = "\t";

	public FileManager() {
	}

	public FileManager(String delimiter) {
		this.delimiter = delimiter;
	}

	public List<Object> readFileToTwoLists(String fileName) {
		File file = new File(fileName);
		BufferedReader reader = null;
		List<Object> lists = new ArrayList<Object>();
		try {
			reader = new BufferedReader(new FileReader(file));
			String tempString = null;
			List<String> superClass = new ArrayList<String>();
			List<String> subClass = new ArrayList<String>();
			// 一次读入一行，直到读入null为文件结束
			while ((tempString = reader.readLine()) != null) {
				String[] words = tempString.split(delimiter, 2);
				
				superClass.add(words[0]);
				subClass.add(words[1]);
			}
			reader.close();

			lists.add(superClass);
			lists.add(subClass);
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			if (reader != null) {
				try {
					reader.close();
				} catch (IOException e1) {
				}
			}
		}

		return lists;
	}

	public List<Set<String>> readFileToSets(String fileName) {
		File file = new File(fileName);
		BufferedReader reader = null;
		List<Set<String>> sets = new ArrayList<Set<String>>();
		try {
			reader = new BufferedReader(new FileReader(file));
			String tempString = null;
			// 一次读入一行，直到读入null为文件结束
			while ((tempString = reader.readLine()) != null) {
				String[] words = tempString.split(delimiter,-1);
				if (sets.size() == 0){
					for(int k = 0; k < words.length;k++)
						sets.add(new HashSet<String>());
				}
				for(int i = 0;i<words.length;i++){
					if (words[i].length()==0)
						System.out.println(tempString);
					sets.get(i).add(words[i]);
				}
				
			}
			reader.close();

		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			if (reader != null) {
				try {
					reader.close();
				} catch (IOException e1) {
				}
			}
		}
		return sets;
	}

	/**
	 * 4 按字符缓冲写入 BufferedWriter
	 * 
	 * @param count
	 *            写入循环次数
	 * @param str
	 *            写入字符串
	 */
	public void writeSetToFile(Set s, String filename) {
		File f = new File(filename);
		OutputStreamWriter writer = null;
		BufferedWriter bw = null;
		try {
			OutputStream os = new FileOutputStream(f);
			writer = new OutputStreamWriter(os);
			bw = new BufferedWriter(writer);
			Iterator<String> it = s.iterator();
			while (it.hasNext()) {
				bw.write(it.next() + "\n");
			}
			bw.flush();
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
	}

	public List getSetFromFile(String fileName) {
		File file = new File(fileName);
		BufferedReader reader = null;
		List<String> l = new ArrayList<String>();
		try {
			reader = new BufferedReader(new FileReader(file));
			String tempString = null;
			while ((tempString = reader.readLine()) != null) {
				l.add(tempString);
			}
			reader.close();

		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			if (reader != null) {
				try {
					reader.close();
				} catch (IOException e1) {
				}
			}
		}
		return l;
	}

}
