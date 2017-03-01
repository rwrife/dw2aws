from xml.dom import minidom
import json
config = {}
xmldoc = minidom.parse('search.xml')

mappings = config['mappings'] = {}
product = mappings['product'] = {}
fields = product['properties'] = {}

fs = xmldoc.getElementsByTagName('searchable-attribute')
for f in fs:
    fname = f.getElementsByTagName('attribute-path')[0].firstChild.nodeValue
    fname = fname.replace('product.', '')
    fname = fname.replace('custom.', 'c_')
    fields[fname] = {'type':'string', 'analyzer':'search_analyzer'}

settings = mappings['settings'] = {}
settings['number_of_shards'] = 1
settings['analysis'] = {}
filters = settings['analysis']['filter'] = {}
syns = xmldoc.getElementsByTagName('synonyms')
if len(syns) > 0:
    filters['synonym_filter'] = {}
    filters['synonym_filter']['synonyms'] = []

synonyms = filters['synonym_filter']['synonyms']  
for syn in syns:
    vals = syn.firstChild.nodeValue.split(',')
    synonyms.append(vals)
    
print json.dumps(config, ensure_ascii=True, indent=4)