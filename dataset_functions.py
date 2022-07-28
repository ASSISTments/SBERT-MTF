import re
import number_handling

operators = ['+', '-', '*', '/', '=', 'x']

regex = r'^[+-]?(?:\d*\.*\,*\/*)?\d+$'

words = r'[A-Z]*[a-z]+\w+'

def find_math_terms(string):
    math_terms = []
    math_terms_pop = []
    m_terms = []
    terms_without_comma_lists = []
    string = number_handling.replace_numbers_numerical(string)
    terms = string.split()
    for term in terms:
        # Separate comma-separated lists of terms without spaces between each term
        if not (term[0] != '(' and ',' in term):
            terms_without_comma_lists.append(term)
            continue
        while ',' in term and term[0] != '(':
            for i in range(len(term)):
                if (term[i] == ','):
                    terms_without_comma_lists.append(term[:i])
                    term = term[i+1:]
                    break
        terms_without_comma_lists.append(term)
    for term in terms_without_comma_lists:
        # Strip uncommon punctuation from the end of terms
        while (len(term) > 0 and (term[-1] == '.' or term[-1] == ';' or term[-1] == "\""
        or term[-1] == "?" or (term[-1] == ',' and term[0] != '('))):
            term = term[:-1]
            # Take out quotations and dollar signs
        if (len(term) > 0 and (term[0] == "\"" or term[0] == "$")):
            term = term[1:]
            # Take out contractions
        if (re.match('([A-Za-z]+)[\'`]([A-Za-z]+)$', term) is not None and term != "y\'x" and "x\'y" != term
                and term != "p\'q" and term != "q\'p" and term != "f\'g" and term != "g\'f"):
            term = re.sub('([A-Za-z]+)[\'`]([A-Za-z]+)', r'\1'r'\2', term)
        if not term.isalpha() and len(term) > 0:
            m_terms.append(term)
    for term in m_terms:
        # Fix terms that are a word followed by number
        if re.match(r'[A-Z|a-z]+([0-9]|\-\.|\-[0-9])', term) is not None:
            term = re.sub(r'[A-Z|a-z]+', "", term, count=1)
            math_terms.append(term)
            math_terms.append(" ")
        elif re.match(words, term) is None:
            math_terms.append(term)
            math_terms.append(" ")
    for x in range(1, len(math_terms)):
        # Combine equations separated by spaces
        if ((math_terms[x] == "+" or math_terms[x] == "-" or math_terms[x] == "*" or math_terms[x] == "/" or math_terms[
            x] == "^" or math_terms[x] == "=") and re.match(words, math_terms[x-1]) is None):
            math_terms_pop.append(x - 1)
            math_terms_pop.append(x+1)
        elif (math_terms[x] == "+" or math_terms[x] == "-" or math_terms[x] == "*" or math_terms[x] == "/" or math_terms[
            x] == "^" or math_terms[x] == "=") and re.match(words, math_terms[x-1]) is not None:
            math_terms_pop.append(x+1)
    for i in range(len(math_terms_pop)):
        math_terms.pop(math_terms_pop[i]-i)

    terms = "".join(math_terms)
    terms = terms.split()
    final_terms = []
    for i in range(len(terms)):
        # Combine coordinates together and keep terms showing the distributive property
        if (i < len(terms) - 1 and terms[i][0] == "(" and terms[i][-1] == "," and terms[i + 1][-1] == ")"):
            final_terms.append(terms[i])
            final_terms.append(terms[i + 1])
            i += 1
        elif (terms[i][0] == "(" and terms[i][-1] == ")" and ("," in terms[i])):
            final_terms.append(terms[i])
        elif ("(" in terms[i] and ")" in terms[i] and ('+' in terms[i] or '-' in terms[i] or '*' in terms[i]
        or '/' in terms[i] or '^' in terms[i])):
            final_terms.append(terms[i])
        elif (not ("(" in terms[i])):
            final_terms.append(terms[i])
    for i in range(len(final_terms)):
        # Round off any decimals to at most two places
        if (re.match(r'[-]?[0-9]*\.[0-9]+$', final_terms[i]) is not None):
            for j in range(len(final_terms[i])):
                if (final_terms[i][j] == '.'):
                    if (len(final_terms[i]) > j+2):
                        final_terms.insert(i, final_terms[i][:j+3])
                        final_terms.pop(i+1)
                        break
    for term in final_terms:
        if term == '':
            final_terms.remove(term)
    return final_terms


def label_terms(terms):
    labeled_terms = []
    for term in terms:
        operator = False
        variable = False
        equation = False
        if term.isalpha() is False:
            if '+' in term or '-' in term or '/' in term or '*' in term:
                operator = True
            if 'x' in term:
                variable = True
            if '=' in term:
                equation = True
            new_dict = {'word': term, 'operator': operator, 'variable': variable, 'equation': equation}
            labeled_terms.append(new_dict)
    return labeled_terms


def word_list_to_freq_dict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(list(zip(wordlist, wordfreq)))


def sort_freq_dict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux
