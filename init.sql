CREATE TABLE stem (rule integer, prefix text);
CREATE TABLE form (rule integer, suffix text);
.separator ":"
.import stems stem
.import forms form
