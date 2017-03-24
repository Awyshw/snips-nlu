import numpy as np

from intent_classifier_resources import get_subtitles

def augment_dataset(dataset, language='en'):

	intent_list = dataset['intents'].keys()
	intent_code = dict((intent, i+1) for i,intent in enumerate(intent_list))

	# get size of smaller intent (for noise amount and regularization)
	queries_per_intent = [ len(dataset['intents'][intent]) for intent in intent_list ]
	mean_queries_per_intent = np.mean(queries_per_intent)
	alpha = 1.0/(4*(sum(queries_per_intent)+5*mean_queries_per_intent))

	data_noise_train = get_subtitles("en")
	queries_noise = np.random.choice(data_noise_train, size=5*mean_queries_per_intent, replace=False)

	queries = []
	y = []
	data = {                                                
	'text': [],   
	'intent_val': []
	}
	for intent in intent_list:
		queries += [ ''.join( [ dataset['intents'][intent]['utterances'][i]['data'][j]['text'] for j in range(len(dataset['intents'][intent]['utterances'][i]['data'])) ] ) for i in range(len(dataset['intents'][intent]['utterances'])) ]
		y +=  [ intent_code[intent] for _ in xrange(len(dataset['intents'][intent]['utterances'])) ]

	queries += [ ''.join( [ queries_noise[i]['data'][j]['text'] for j in range(len(queries_noise[i]['data'])) ] ) for i in range(len(queries_noise)) ]
	y += [ 0 for _ in len(queries_noise) ]

	queries = np.array(queries)
	y = np.array(y)

	return (queries, y), alpha, intent_list