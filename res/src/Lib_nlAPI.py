# -*- coding: utf-8 -*-
"""
Created on Tue May  9 09:35:53 2017

@author: m.leclech
"""

# Imports the Google Cloud client library
from google.cloud import language

# Instantiates a client
language_client = language.Client()

# The text to analyze
text = "This page documents production updates to Natural Language API."
document = language_client.document_from_text(text)
annotations = document.annotate_text()


# *** SAVE DANS UN FICHIER ***
savefile = open("savefile.txt",'w')
## Sentences
#savefile.write("Sentences")
#for i in range(len(annotations.sentences)):
#    savefile.write(annotations.sentences[i])
# Tokens present if include_syntax=True
savefile.write("***TOKENS***\n")
for token in annotations.tokens:
     savefile.write('%s: %s\n' % (token.part_of_speech, token.text_content))
     savefile.write('edge index %s\n' % (token.edge_index))
     savefile.write('edge label %s\n' % (token.edge_label))
     savefile.write('lemma %s\n' % (token.lemma))
     savefile.write("---\n")
# Sentiment present if include_sentiment=True
#savefile.write("***SENTIMENT***\n")
#savefile.write('score: %s\n' % (annotations.sentiment.score))
#savefile.write('magnitude: %s\n' % (annotations.sentiment.magnitude))
# Entities present if include_entities=True
savefile.write("***ENTITIES***\n")
for entity in annotations.entities:
    savefile.write('name: %s\n' % (entity.name,))
    savefile.write('type: %s\n' % (entity.entity_type,))
    savefile.write('metadata: %s\n' % (entity.metadata,))
    savefile.write('salience: %s\n' % (entity.salience,))
    savefile.write("---\n")
savefile.close()
print("ok")
# ***FIN***


