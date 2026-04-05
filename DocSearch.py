import math

def read_lines(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]

def build_dictionary_and_index(documents):
    dictionary_set = set()
    inverted_index = {}
    document_word_counts = []

    for doc_id, document in enumerate(documents, start=1):
        words = document.split()
        word_counts = {}

        for word in words:
            dictionary_set.add(word)
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1
        
        document_word_counts.append(word_counts)

        for word in word_counts:
            if word not in inverted_index:
                inverted_index[word] = []
            inverted_index[word].append(doc_id)
    
    dictionary = sorted(dictionary_set)
    return dictionary, inverted_index, document_word_counts

def query_relevant_documents(query_words, inverted_index):
    valid_words = []
    seen = set()

    for word in query_words:
        if word in inverted_index and word not in seen:
            valid_words.append(word)
            seen.add(word)

    if not valid_words:
        return [], []
    
    relevant_docs = set(inverted_index[valid_words[0]])
    for word in valid_words[1:]:
        relevant_docs = relevant_docs.intersection(set(inverted_index[word]))

    return valid_words, sorted(relevant_docs)

def compute_angle(valid_words, document_word_counts):
    query_length = math.sqrt(len(valid_words))

    dot_product = 0
    doc_length_squared = 0

    for count in document_word_counts.values():
        doc_length_squared += count * count
    
    for word in valid_words:
        if word in document_word_counts:
            dot_product += document_word_counts[word]
        
    doc_length = math.sqrt(doc_length_squared)

    if query_length == 0 or doc_length == 0:
        return 90.0
    
    cos_theta = dot_product / (query_length * doc_length)

    if cos_theta > 1:
        cos_theta = 1
    elif cos_theta < -1:
        cos_theta = -1

    return math.degrees(math.acos(cos_theta))

def main():
    documents = read_lines("docs.txt")
    queries = read_lines("queries.txt")

    dictionary, inverted_index, document_word_counts_list = build_dictionary_and_index(documents)

    print("Words in dictionary:", len(dictionary))

    for query in queries:
        print("Query:", query)

        query_words = query.split()
        valid_words, relevant_docs = query_relevant_documents(query_words, inverted_index)

        print("Relevant documents:", end="")
        if relevant_docs:
            print(" " + " ".join(str(doc_id) for doc_id in relevant_docs))
        else:
            print()

        if not relevant_docs:
            continue

        results = []
        for doc_id in relevant_docs:
            angle = compute_angle(valid_words, document_word_counts_list[doc_id - 1])
            results.append((doc_id, angle))

        results.sort(key=lambda item: item[1])

        for doc_id, angle in results:
            print(doc_id, "{:.2f}".format(angle))

main()