# XLore_Feature

------

Code for feature part for paper:
** **

## Step 
 * Use Stanford parser for tagging and typed dependencies (**ParserDemo**)
 * Calculate features (**feature**)

ParserDemo
------
* For English File
>* ant main -Dargs='en input_file_name'
>* ant main -Dargs='en input_file_name input_path'
>* ant main -Dargs='en input_file_name input_path output_path'

* For Chinese File
>* ant main -Dargs='zh input_file_name'
>* ant main -Dargs='zh input_file_name input_path'
>* ant main -Dargs='zh input_file_name input_path output_path'

* Default Input Path: /home/lmy/data/
* Default Output Path: /home/lmy/data/parser/

Note:
There may be mistakes when parsing. You can rerun the program. Unless you remove the parser result file, it wont reparse the sentence which has already been parsed.

Feature 
------
####1. Get headword

####2. Get feature

