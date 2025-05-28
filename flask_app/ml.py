import pickle

def find_patterns(readout_words, focus_index):
    patterns = []

    #go through every word up to the focus index
    for anchor in range(focus_index):
        pattern = ""
        #set weight based on distance between anchor and focus index
        weight = 10 / (focus_index - anchor)

        #for each word, go through each preceding word in reverse order
        for subtractor in range(anchor + 1):
            pattern = readout_words[anchor - subtractor] + " " + pattern #add to back of pattern
            #increase weight based on length of pattern
            weight *= 2
        
            if pattern != "":
                patterns.append({"pattern": pattern, "weight": weight})

    return patterns

def merge_pattern_sets(pattern_set_a, pattern_set_b):
    final_pattern_set = []

    for pat_a in range(len(pattern_set_a)):
        final_pattern_set.append(pattern_set_a[pat_a])

        pat_b = 0
        while pat_b < len(pattern_set_b):
            if (pattern_set_a[pat_a]["pattern"] == pattern_set_b[pat_b]["pattern"]):
                if (final_pattern_set[pat_a]["weight"] > pattern_set_b[pat_b]["weight"]):
                    final_pattern_set[pat_a]["weight"] += pattern_set_b[pat_b]["weight"] / (final_pattern_set[pat_a]["weight"] / 10)
                else:
                    final_pattern_set[pat_a]["weight"] /= pattern_set_b[pat_b]["weight"] / 10
                    final_pattern_set[pat_a]["weight"] += pattern_set_b[pat_b]["weight"]
                
                pattern_set_b.pop(pat_b)
                pat_b -= 1
            
            pat_b += 1

    for pat_b in range(len(pattern_set_b)):
        final_pattern_set.append(pattern_set_b[pat_b])

    return final_pattern_set

def process(readout_words):
    # 
    # process readout to add new data to ML dataset
    #

    if not readout_words:
        return

    with open("flask_app/ml_data.pkl", "rb") as f:
        dataset = pickle.load(f)

    #decay
    for word in dataset:
        for pattern in dataset[word]:
            pattern["weight"] *= 0.99

    for i in range(len(readout_words)):
        #find all patterns that come before the focus word
        pattern_set = find_patterns(readout_words, i)
        if readout_words[i] in dataset:
            dataset[readout_words[i]] = merge_pattern_sets(dataset[readout_words[i]], pattern_set)
        else:
            dataset[readout_words[i]] = pattern_set
    
    with open("flask_app/ml_data.pkl", "wb") as f:
        pickle.dump(dataset, f)

    #first word
    with open("flask_app/fw_data.pkl", "rb") as f:
        dataset = pickle.load(f)

    first_word = readout_words[0]

    if first_word in dataset:
        dataset[first_word] += 1
    else:
        dataset[first_word] = 1

    #first word decay
    for word in dataset:
        dataset[word] *= 0.99

    with open("flask_app/fw_data.pkl", "wb") as f:
        pickle.dump(dataset, f)

def generate(readout_words):
    #
    #generate ML word set from current state of readout, using ML dataset
    #
    
    generated_words = ["", "", "", "", "", "", "", "", "", ""]

    #first word
    if not readout_words:
        with open("flask_app/fw_data.pkl", "rb") as f:
            dataset = pickle.load(f)
        
        #sort words and keep first ten
        sorted_words = list({k: v for k, v in sorted(dataset.items(), key=lambda item: item[1], reverse=True)}.keys())
        for i in range(len(sorted_words)):
            generated_words[i] = sorted_words[i]
            if i == 9:
                break

    #not first word
    else:
        readout_patterns = find_patterns(readout_words, len(readout_words))

        with open("flask_app/ml_data.pkl", "rb") as f:
            dataset = pickle.load(f)

        found_words = {}

        for key in dataset: #for each word in the dataset
            for dataset_pat in dataset[key]: #for each pattern under the word
                for readout_pat in readout_patterns: #for each pattern in the readout
                    if dataset_pat["pattern"] == readout_pat["pattern"]:
                        if key in found_words:
                            found_words[key] += dataset_pat["weight"] * readout_pat["weight"]
                        else:
                            found_words[key] = dataset_pat["weight"] * readout_pat["weight"]

        #sort found words and keep first ten
        sorted_words = list({k: v for k, v in sorted(found_words.items(), key=lambda item: item[1], reverse=True)}.keys())
        for i in range(len(sorted_words)):
            generated_words[i] = sorted_words[i]
            if i == 9:
                break

    output = ""
    for word in generated_words:
        output += word + "|"
    output = output[:-1]
    
    return output