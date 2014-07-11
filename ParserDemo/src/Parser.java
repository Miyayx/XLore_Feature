import java.util.List;

import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TypedDependency;

public interface Parser {

	public Tree getParserTree(String sent);

	public List<TypedDependency> getTypedDependency(Tree parse);

	public List<TaggedWord> getTaggedWord(Tree parse);

}
