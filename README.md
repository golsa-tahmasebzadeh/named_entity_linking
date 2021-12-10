Please specify the task, ner_docs_path and nel_docs_path in configs/Input_config.
Manually download https://tib.eu/cloud/s/Erp95gENRrKE79Z and put the content inside "models" folder.
 
1.  python -m venv venv
2.  source venv/bin/activate
3.  pip install -r requirements.txt
* python
* import nltk
* nltk.download('averaged_perceptron_tagger')
* nltk.download('maxent_ne_chunker')
* nltk.download('words')

6.  python annotate.py


