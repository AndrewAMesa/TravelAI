import copy
from collections import defaultdict

from Backend.Models.LLaMaTravelAI import *


def is_in(elt, seq):
    """Similar to (elt in seq), but compares with 'is', not '=='."""
    return any(x is elt for x in seq)

class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError


class TextParsingProblem(Problem):
    def __init__(self, initial, grammar, goal='S'):
        """
        :param initial: the initial state of words in a list.
        :param grammar: a grammar object
        :param goal: the goal state, usually S
        """
        super(TextParsingProblem, self).__init__(initial, goal)
        self.grammar = grammar
        self.combinations = defaultdict(list)  # article combinations
        # backward lookup of rules
        for rule in grammar.rules:
            for comb in grammar.rules[rule]:
                self.combinations[' '.join(comb)].append(rule)

    def actions(self, state):
        actions = []
        categories = self.grammar.categories
        # first change each word to the article of its category
        for i in range(len(state)):
            word = state[i]
            if word in categories:
                for X in categories[word]:
                    state[i] = X
                    actions.append(copy.copy(state))
                    state[i] = word
        # if all words are replaced by articles, replace combinations of articles by inferring rules.
        if not actions:
            for start in range(len(state)):
                for end in range(start, len(state) + 1):
                    # try combinations between (start, end)
                    articles = ' '.join(state[start:end])
                    for c in self.combinations[articles]:
                        actions.append(state[:start] + [c] + state[end:])
        return actions

    def result(self, state, action):
        return action

    def h(self, state):
        # heuristic function
        return len(state)


def Rules(**rules):
    """Create a dictionary mapping symbols to alternative sequences.
    >>> Rules(A = "B C | D E")
    {'A': [['B', 'C'], ['D', 'E']]}
    """
    for (lhs, rhs) in rules.items():
        rules[lhs] = [alt.strip().split() for alt in rhs.split('|')]
    return rules


def Lexicon(**rules):
    """Create a dictionary mapping symbols to alternative words.
    >>> Lexicon(Article = "the | a | an")
    {'Article': ['the', 'a', 'an']}
    """
    for (lhs, rhs) in rules.items():
        rules[lhs] = [word.strip() for word in rhs.split('|')]
    return rules


class Grammar:

    def __init__(self, name, rules, lexicon):
        """A grammar has a set of rules and a lexicon."""
        self.name = name
        self.rules = rules
        self.lexicon = lexicon
        self.categories = defaultdict(list)
        for lhs in lexicon:
            for word in lexicon[lhs]:
                self.categories[word].append(lhs)

    def rewrites_for(self, cat):
        """Return a sequence of possible rhs's that cat can be rewritten as."""
        return self.rules.get(cat, ())

    def isa(self, word, cat):
        """Return True iff word is of category cat"""
        return cat in self.categories[word]

    def cnf_rules(self):
        """Returns the tuple (X, Y, Z) for rules in the form:
        X -> Y Z"""
        cnf = []
        for X, rules in self.rules.items():
            for (Y, Z) in rules:
                cnf.append((X, Y, Z))

        return cnf

    def generate_random(self, S='S'):
        """Replace each token in S by a random entry in grammar (recursively)."""
        import random

        def rewrite(tokens, into):
            for token in tokens:
                if token in self.rules:
                    rewrite(random.choice(self.rules[token]), into)
                elif token in self.lexicon:
                    into.append(random.choice(self.lexicon[token]))
                else:
                    into.append(token)
            return into

        return ' '.join(rewrite(S.split(), []))

    def __repr__(self):
        return '<Grammar {}>'.format(self.name)

greeting_rules = Rules(Greeting="hello | hi | hey | greetings | salutations | welcome | howdy | what's up | good morning | good afternoon | good evening | hello! | hi! | hey! | greetings! | salutations! | welcome! | howdy! | what's up? | good morning! | good afternoon! | good evening!")

greeting_lexicon = Lexicon()

greeting_grammer = Grammar("Greeting", rules=greeting_rules, lexicon=greeting_lexicon)

def greeting_check(problem):
    state = problem.initial
    greetings = []
    actions = problem.actions(state)
    if not actions:
        return False
    elif "Greeting" in actions[0]:
        return True
    return False


def generateGreeting(text):
    prompt = f"""
    Respond to this text: {text} as if you were a travel agent trying to help a customer plan a trip using your services.
    Provide them with a friendly greeting and then ask if they want any help with planning a future trip. Suggest that they
    could ask about different locations and timeframes"""

    return llm_client.text_generation(prompt, max_new_tokens=5000, stream=True)